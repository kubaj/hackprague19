from os import getenv

from flask import (
    Flask,
    jsonify,
    request,
)
from werkzeug import exceptions

from places import (
    HereAPIWrapper,
    build_places_response,
)

app = Flask(__name__)
here_api_wrapper = HereAPIWrapper()


@app.route('/')
def hello_world():
    return 'Hello world from Python'


@app.route('/geocode', methods=['GET'])
def geocoding():
    address = request.args.get('address', None)
    if not address:
        raise exceptions.BadRequest('Unspecified address')

    response = here_api_wrapper.geocode(address)
    if not response.view:
        return jsonify({})

    return jsonify(response.json())


@app.route('/places', methods=['GET'])
def places():
    lat = request.args.get('lat', None)
    lng = request.args.get('lng', None)
    if not (lat and lng):
        raise exceptions.BadRequest('Unspecified `lat` and `lng`')

    all_places = list(here_api_wrapper.get_transportation(lat, lng)) + list(here_api_wrapper.get_services(lat, lng))
    return jsonify(build_places_response(all_places))


if __name__ == '__main__':
    port = getenv('PORT', "8080")

    app.run(host='0.0.0.0', port=int(port))
