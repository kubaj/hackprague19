from requests.models import Response


class GeocodingResponse(object):
    """Geocoding response wrapper object"""

    def __init__(self, response: Response):
        if response.status_code != 200:
            self.view = None

        json: dict = response.json()['Response']
        if json.get('View', []):
            self.view = json['View'][0]['Result'][0]
        else:
            self.view = None

    @property
    def latitude(self) -> float:
        return self.view.get('Location', {}).get('NavigationPosition', {})[0].get('Latitude', None)

    @property
    def longitude(self) -> float:
        return self.view.get('Location', {}).get('NavigationPosition', {})[0].get('Longitude', None)

    @property
    def address(self) -> float:
        return self.view.get('Location', {}).get('Address', {}).get('Label', None)

    def json(self) -> dict:
        if self.view:
            return dict(
                latitude=self.latitude,
                longitude=self.longitude,
                address=self.address
            )
        return dict(
            error='Failed to obtain coordinates'
        )
