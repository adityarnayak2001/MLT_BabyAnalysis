import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
config = {'apiKey':"AIzaSyB9eMHhNxSrGvwI6NZ2hFUqA8rc0zbkwC4",
'authDomain':"pltmlbabyanalysis.firebaseapp.com",
'projectId':"pltmlbabyanalysis",
'storageBucket':"pltmlbabyanalysis.appspot.com",
'messagingSenderId':"283761884299",
'appId':"1:283761884299:web:0c804922739d061c4be88e",
'measurementId':"G-YPQSFGV2F8",
'databaseURL':""
}
# Setup
cred = credentials.Certificate("pltmlbabyanalysis.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
# Pass the user's idToken to the push method
results = db.collection("users").get()
print(results)
