from os import getenv

from flask import (
    Flask,
    jsonify,
    request,
)

from places import HereAPIWrapper

app = Flask(__name__)
here_api_wrapper = HereAPIWrapper()


@app.route('/')
def hello_world():
    return 'Hello world from Python'


@app.route('/geocode', methods=['GET'])
def geocoding():
    address = request.args.get('address', None)
    if not address:
        return jsonify({})

    return jsonify(
        here_api_wrapper.geocode(address).json()
    )


if __name__ == '__main__':
    port = getenv('PORT', "8080")

    app.run(host='0.0.0.0', port=int(port))
