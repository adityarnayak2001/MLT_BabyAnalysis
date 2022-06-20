import urllib.request as ur
import json
# url = "https://thingspeak.com/channels/1347725/field/1.json"
# response = ur.urlopen(url)
# data =json.loads(response.read())
# data = data["feeds"]
# print(data)
# def sort_by_key(list):
#     return list['entry_id']

# # Print the sorted JSON list based on the name key
# print("\nArray of JSON objects after sorting:")
# data=sorted(data, key=sort_by_key)
# for x in data:
#     print(x["field1"])

def get_json():
            res=[]
            url = "https://thingspeak.com/channels/1347725/field/1.json"
            response = ur.urlopen(url)
            data =json.loads(response.read())
            data = data["feeds"]
            def sort_by_key(list):
                return list['entry_id']
            print("\nArray of JSON objects after sorting:")
            data=sorted(data, key=sort_by_key)
            for x in data:
                res.append(x["field1"])
            return list(range(len(res))),res
x,y=get_json()
print(x)
print("hgello",len(y))
print(y)