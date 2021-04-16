'''
Root file of a server
'''

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

# initialize Flask
app = Flask(__name__)
CORS(app)


@app.route('/healthcheck')
def health_check():
    '''Health check for a server'''
    return 'OK'


@app.route('/check_test', methods=['POST'])
def check_test():
    '''Check result for a test photo'''
    request_data = request.json

    return request_data


if __name__ == '__main__':
    app.run(debug=True)
