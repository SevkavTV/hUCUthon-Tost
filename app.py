'''
Root file of a server
'''

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests

from firebase.firebase_init import firebase_init
import firebase.database as db
import photos.recognition as recognition

# initialize Flask
app = Flask(__name__)
CORS(app)

# initialize firebase
firebase_init()


@app.route('/healthcheck')
def health_check():
    '''Health check for a server'''
    return 'OK'


@app.route('/check_test', methods=['POST'])
def check_test():
    '''Check result for a test photo'''
    request_data = request.json

    return request_data


@app.route('/create_pattern', methods=['POST'])
def create_pattern():
    '''Create a pattern for user'''
    request_data = request.json

    db.create_pattern(
        request_data['uid'], request_data['pattern_id'], request_data['pattern'])

    return make_response('OK', 200)


@app.route('/get_patterns', methods=['POST'])
def get_patterns():
    '''Get patterns from a user'''
    request_data = request.json

    patterns = db.get_patterns(request_data['uid'])

    return make_response(jsonify(patterns), 200)


@app.route('/set_user_info', methods=['POST'])
def set_user_info():
    '''Set info about user'''
    request_data = request.json

    db.set_user_info(request_data['uid'], request_data['user'])

    return make_response('OK', 200)


@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    '''Get user info'''
    request_data = request.json

    user = db.get_user_info(request_data['uid'])

    return make_response(jsonify(user), 200)


@app.route('/calculate_results', methods=['POST'])
def calculate_results():
    '''Calculate results for a pattern'''
    files = request.files
    for key in files:
        print(key)
        file = files[key]
        recognition.aaaa(file.read())

    return make_response('OK', 200)


if __name__ == '__main__':
    app.run(debug=True)
