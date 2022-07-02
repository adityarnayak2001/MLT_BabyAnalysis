from numpy import random
import sys
from models.experimental import attempt_load
from utils.general import (check_img_size, non_max_suppression, scale_coords, set_logging)
from utils.torch_utils import select_device, time_sync
import os
import cv2
import torch
from PIL import Image
from torchaudio import transforms
import torchvision.transforms as T
from IPython.display import Audio
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init
import matplotlib.pyplot as plt
from torch.autograd import Variable
import wave
import librosa
import librosa.display
import IPython.display as ipd
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import time

def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True):
    shape = img.shape[:2]  
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  
        r = min(r, 1.0)
    ratio = r, r 
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1] 
    if auto:  
        dw, dh = np.mod(dw, 32), np.mod(dh, 32) 
    elif scaleFill:
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0] 

    dw /= 2  
    dh /= 2

    if shape[::-1] != new_unpad:  
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color) 
    return img, ratio, (dw, dh)

class localizer():
    def __init__(self):
        self.device = ''
        self.imgsz = 640
        self.weights = '0_Person.pt'
        self.device = select_device(self.device)
        self.model = attempt_load(self.weights, map_location=self.device)
        
        self.half = self.device.type != 'cpu'
        self.classes = [0, 1]
        if self.half :
            self.model.half()
        self.min_conf = 30
    
    def detect(self, img) :
        im0 = img.copy()
        img = letterbox(img, new_shape=(640))[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        
        pred = self.model(img, augment=False)[0]
        pred = non_max_suppression(pred, 0.25, 0.45, classes=self.classes, agnostic=False)
        cds = []
        confidences = []
        clss = []
        for i, det in enumerate(pred):  
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                    A = []
                    A.append(c1)
                    A.append(c2)
                    cds.append(A)
                    confidence = ([float(conf)][0]) * 100
                    confidences.append(confidence)
                    clss.append(cls)
        return clss, confidences, cds


# result = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'),20, (854,480))



# ----------------------------
# Audio Classification Model
# ----------------------------
class AudioClassifier (nn.Module):
    # ----------------------------
    # Build the model architecture
    # ----------------------------
    def __init__(self):
        super().__init__()
        conv_layers = []

        # First Convolution Block with Relu and Batch Norm. Use Kaiming Initialization
        self.conv1 = nn.Conv2d(2, 8, kernel_size=(5, 5), stride=(2, 2), padding=(2, 2))
        self.relu1 = nn.ReLU()
        self.bn1 = nn.BatchNorm2d(8)
        init.kaiming_normal_(self.conv1.weight, a=0.1)
        self.conv1.bias.data.zero_()
        conv_layers += [self.conv1, self.relu1, self.bn1]

        # Second Convolution Block
        self.conv2 = nn.Conv2d(8, 16, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
        self.relu2 = nn.ReLU()
        self.bn2 = nn.BatchNorm2d(16)
        init.kaiming_normal_(self.conv2.weight, a=0.1)
        self.conv2.bias.data.zero_()
        conv_layers += [self.conv2, self.relu2, self.bn2]

        # Third Convolution Block
        self.conv3 = nn.Conv2d(16, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
        self.relu3 = nn.ReLU()
        self.bn3 = nn.BatchNorm2d(32)
        init.kaiming_normal_(self.conv3.weight, a=0.1)
        self.conv3.bias.data.zero_()
        conv_layers += [self.conv3, self.relu3, self.bn3]

        # Fourth Convolution Block
        self.conv4 = nn.Conv2d(32, 64, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
        self.relu4 = nn.ReLU()
        self.bn4 = nn.BatchNorm2d(64)
        init.kaiming_normal_(self.conv4.weight, a=0.1)
        self.conv4.bias.data.zero_()
        conv_layers += [self.conv4, self.relu4, self.bn4]

        # Linear Classifier
        self.ap = nn.AdaptiveAvgPool2d(output_size=1)
        self.lin = nn.Linear(in_features=64, out_features=10)

        # Wrap the Convolutional Blocks
        self.conv = nn.Sequential(*conv_layers)
 
    # ----------------------------
    # Forward pass computations
    # ----------------------------
    def forward(self, x):
        # Run the convolutional blocks
        x = self.conv(x)

        # Adaptive pool and flatten for input to linear layer
        x = self.ap(x)
        x = x.view(x.shape[0], -1)

        # Linear layer
        x = self.lin(x)

        # Final output
        return x



myModel = AudioClassifier()
device = torch.device("cpu")
myModel.load_state_dict(torch.load('weight.pth',map_location=device))
myModel.eval()

model = localizer()
input_video = 'video.mp4'
cap = cv2.VideoCapture(input_video)

test_transforms = T.Compose([T.ToTensor()])

def predict_image(model,image):
    image=cv2.imread(image)
    image_tensor = test_transforms(image).float()
    image_tensor = image_tensor.unsqueeze_(0)
    input1 = Variable(image_tensor)
    input1 = input1.to(device)[:,:2,:,:]
    print(input1.shape)
    output = model(input1)
    index = output.data.cpu().numpy().argmax()
    return index

prev_class = -1
counter_Cry = 0
while True:
    
    success, img = cap.read()
    if not success:
        break
    
    clss, confidences, cds = model.detect(img)
    if clss :
        clss_P=int(clss[0].item())
        clss=int(clss[0].item())
        cv2.rectangle(img, cds[0][0], cds[0][1],(255,0,0))
        #print(clss_P)
        if prev_class == clss_P :
            prev_class = clss_P
            if clss_P == 1 :
                counter_Cry += 1
            continue
        prev_class = clss_P
          
        if clss == 1:
            
            print(counter_Cry)
            
                
            cv2.putText(img, 'PAIN',( 50,100), cv2.FONT_HERSHEY_SIMPLEX, 1,( 0, 0,200), 3)
            cv2.rectangle(img, cds[0][0], cds[0][1],(0,0,200))
        
            fs=44100
            duration = 10 # seconds
            if counter_Cry > 20 :
                myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
                print( "Recording Audio")
                sd.wait()
                # sd.play(myrecording)
                # sd.wait()
                print ("Audio recording complete , Play Audio")
                write('output_from_mic.wav', fs, myrecording)
        
                # GETTING THE MEL SPECTOGRAM
        
                scale_file = "output_from_mic.wav"
                ipd.Audio(scale_file)
                scale, sr = librosa.load(scale_file)
                filter_banks = librosa.filters.mel(n_fft=2048, sr=44100, n_mels=10)
                filter_banks.shape
                mel_spectrogram = librosa.feature.melspectrogram(scale, sr=sr, n_fft=2048, hop_length=512, n_mels=10)
                plt.figure(figsize=(25, 10))
                log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
                librosa.display.specshow(log_mel_spectrogram,x_axis="time",y_axis="mel", sr=sr)
                plt.savefig('mel_spectrogram.png')
                print("class is:",predict_image(myModel, 'mel_spectrogram.png'))
                if predict_image(myModel, 'mel_spectrogram.png')==0:
                    cv2.putText(img, 'High Risk',( 100,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255, 0), 3)
            counter_Cry = 0
        if clss == 0:
              cv2.putText(img, 'NO PAIN',( 50,100), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255, 0), 3)    
              cv2.rectangle(img, cds[0][0], cds[0][1],(0,255,0))   
    cv2.waitKey(1)
    cv2.imshow('Output',img)
    # result.write(img)winname, mat

cap.release()
# result.release()
cv2.destroyAllWindows()
