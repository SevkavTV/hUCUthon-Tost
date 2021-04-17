import firebase_admin as admin
from firebase_admin import credentials


def firebase_init():
    # initialize firebase admin sdk
    if not admin._apps:
        cred = credentials.Certificate('firebase/firebase_service_key.json')
        admin.initialize_app(cred, {
            'storageBucket': 'tost-a3df4.appspot.com'
        })
