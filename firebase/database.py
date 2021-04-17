import json
from firebase_admin import firestore
from firebase_admin import storage


def set_user_info(uid, user):
    firestore_db = firestore.client()

    ref_document = firestore_db.collection(
        'users').document(uid)

    ref_document.set(user, merge=True)


def get_user_info(uid):
    firestore_db = firestore.client()

    ref_document = firestore_db.collection(
        'users').document(uid)

    user = ref_document.get()

    return user.to_dict()


def create_pattern(uid, pattern_id, pattern):
    firestore_db = firestore.client()

    ref_document = firestore_db.collection(
        'users').document(uid).collection('patterns').document(pattern_id)

    ref_document.set(pattern, merge=True)


def get_patterns(uid):
    firestore_db = firestore.client()

    docs = firestore_db.collection(
        'users').document(uid).collection('patterns').stream()

    patterns = []
    for doc in docs:
        dict_pattern = doc.to_dict()
        dict_pattern['id'] = doc.id
        patterns.append(dict_pattern)

    return patterns


def get_pattern_answers(uid, pattern_id):
    firestore_db = firestore.client()

    ref_document = firestore_db.collection(
        'users').document(uid).collection('patterns').document(pattern_id)

    pattern_dict = ref_document.get().to_dict()

    return pattern_dict['data']


def save_photo(photo_path, photo_name):
    bucket = storage.bucket()
    blob = bucket.blob(photo_name)
    blob.upload_from_filename(photo_path + photo_name)
    return blob.public_url
