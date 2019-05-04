import requests

from .coordinates import GeocodingResponse


class HereAPIWrapper(object):
    """Wraps HERE API request creation and provides simple interface for purposes of our project"""

    # API credentials
    APP_ID = 'cX0pmZoChwYNwtKbn0sI'
    APP_CD = 'Oss4iaUO-TjnLVjMddhqjQ'
    GEOCODER_BASE_URL = 'https://geocoder.api.here.com'

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
