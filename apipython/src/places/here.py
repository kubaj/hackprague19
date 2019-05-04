import logging
import typing

import requests

from .coordinates import GeocodingResponse
from .places import (
    PLACES_CATEGORIES_EDUCATION,
    PLACES_CATEGORIES_FOOD,
    PLACES_CATEGORIES_HEALTH,
    PLACES_CATEGORIES_SHOP,
    PLACES_CATEGORIES_TRANSPORTATION,
    Place,
)


class HereAPIWrapper(object):
    """Wraps HERE API request creation and provides simple interface for purposes of our project"""

    # API credentials
    APP_ID = 'cX0pmZoChwYNwtKbn0sI'
    APP_CD = 'Oss4iaUO-TjnLVjMddhqjQ'

    # Geocoding
    GEOCODER_BASE_URL = 'https://geocoder.api.here.com'

    # Places
    PLACES_BASE_URL = 'https://places.cit.api.here.com'

    @property
    def auth_params(self) -> dict:
        return dict(
            app_id=HereAPIWrapper.APP_ID,
            app_code=HereAPIWrapper.APP_CD,
        )

    def get(self, url: str, url_params: dict) -> requests.models.Response:
        """Performs HTTP GET to Here API

        :param url: url
        :param url_params: non credentials parameters
        :return: response
        """
        return requests.get(
            url=url,
            params=dict(
                **self.auth_params,
                **url_params
            )
        )

    @staticmethod
    def comma_separate_list(l: typing.List[str]) -> str:
        """Turns list into a comma separated string.

        Used by places api methods

        :param l: list of strings
        :return: comma separated string
        """
        result = ''
        for i in l[:-1]:
            result += '{},'.format(i)
        if l:
            result += l[-1]
        return result

    def geocode(self, address: str) -> GeocodingResponse:
        """Uses Here geocoding API to obtain coordinates

        :param address: address in string format
        :return: coordinates named tuple
        """
        return GeocodingResponse(self.get(
            url='{}/{}'.format(self.GEOCODER_BASE_URL, '6.2/geocode.json'),
            url_params=dict(
                searchtext=address,
                gen=9
            )
        ))

    def get_transportation(self, latitude: float, longitude: float) -> typing.Generator[Place, None, None]:
        """Retrieves nearby public transport options

        :param latitude: place latitude
        :param longitude: place longitude
        :return: transportation options
        """
        return self.get_places(latitude, longitude, PLACES_CATEGORIES_TRANSPORTATION, radius=500)

    def get_services(self, latitude: float, longitude: float) -> typing.Generator[Place, None, None]:
        """Retrieves nearby public transport options

        :param latitude: place latitude
        :param longitude: place longitude
        :return: transportation options
        """
        return self.get_places(
            latitude,
            longitude,
            PLACES_CATEGORIES_EDUCATION + PLACES_CATEGORIES_FOOD + PLACES_CATEGORIES_SHOP + PLACES_CATEGORIES_HEALTH,
            radius=1000
        )

    def get_places(self,
                   latitude: float,
                   longitude: float,
                   categories: typing.List[str] = None,
                   radius: int = None) -> typing.Generator[Place, None, None]:
        """Retrieves nearby public transport options

        :param latitude: place latitude
        :param longitude: place longitude
        :param categories: list of category ids
        :param radius: radius of searching
        :return: transportation options
        """
        if not radius:
            radius = 1000

        response: requests.models.Response = self.get(
            url='{}/{}'.format(self.PLACES_BASE_URL, 'places/v1/discover/around'),
            url_params={
                "in": "{lat},{lng};r={radius}".format(
                    lat=latitude,
                    lng=longitude,
                    radius=radius,
                ),
                "cat": self.comma_separate_list(categories)
            }
        )
        if response.status_code != 200:
            logging.exception('Failed to retrieve transportation data from Here API')
        else:
            for item in response.json().get('results', {}).get('items', []):
                yield Place(item)
