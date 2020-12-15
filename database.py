import pyrebase

config = {
    'apiKey': "AIzaSyC8BmYEtnhegKDgM2RnDs93_nhcLAu9jQU",
    'authDomain': "smux-mms-original.firebaseapp.com",
    'databaseURL': "https://smux-mms-original-default-rtdb.firebaseio.com/",
    'projectId': "smux-mms-original",
    'storageBucket': "gs://smux-mms-original.appspot.com",
    'messagingSenderId': "665151232927",
    'appId': "1:665151232927:web:e67177535cd1b18f53bbaa",
    'measurementId': "G-JXXJ0Y9J5Y"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
