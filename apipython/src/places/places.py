import typing
from enum import Enum

PLACES_CATEGORIES_FOOD = ['snacks-fast-food', 'tea', 'restaurant', 'bar-pub', 'coffee']
PLACES_CATEGORIES_TRANSPORTATION = ['public-transport']
PLACES_CATEGORIES_HEALTH = ['hospital-health-care-facility', 'hospital']
PLACES_CATEGORIES_SHOP = ['mall', 'department-store', 'food-drink', 'pharmacy', 'clothing-accessories-shop', 'shop']
PLACES_CATEGORIES_EDUCATION = ['education-facility']


class PlaceEnum(Enum):
    TRANSPORT = 'transportation'
    FOOD = 'food',
    HEALTH = 'healthcare',
    EDUCATION = 'education'
    SHOPS = 'shopping'


class Place(object):

    def __init__(self, data: dict):
        """Place definition

        :param data: place data dict
        """
        self.latitude = data.get('position', [None, None])[0]
        self.longitude = data.get('position', [None, None])[1]
        self.name = data.get('title', None)
        self.distance = data.get('distance', None)
        group = data.get('category', {}).get('id', None)
        if group in PLACES_CATEGORIES_EDUCATION:
            self.group = PlaceEnum.EDUCATION
        elif group in PLACES_CATEGORIES_FOOD:
            self.group = PlaceEnum.FOOD
        elif group in PLACES_CATEGORIES_HEALTH:
            self.group = PlaceEnum.HEALTH
        elif group in PLACES_CATEGORIES_SHOP:
            self.group = PlaceEnum.SHOPS
        elif group in PLACES_CATEGORIES_TRANSPORTATION:
            self.group = PlaceEnum.TRANSPORT
        else:
            self.group = None

    @property
    def quality(self) -> float:
        if not self.distance:
            return 0.0
        if self.group == PlaceEnum.TRANSPORT:
            return -(1 / (500.0 ** 2)) * self.distance ** 2 + 1
        return -(1 / (1000.0 ** 2)) * self.distance ** 2 + 1

    @property
    def json(self) -> dict:
        return dict(
            latitude=self.latitude,
            longitude=self.longitude,
            distance=self.distance,
            quality=self.quality,
            name=self.name,
        )


def build_places_response(places: typing.List[Place]) -> dict:
    """Builds places response from list of places of different types

    :param places: list of places
    :return: places response
    """
    r = dict(
        name="Places and Services",
        description="Quality of services in the area",
        quality=None,
        details=[]
    )

    shopping_places = []
    transport_places = []
    food_drink_places = []
    education_places = []
    healthcare_places = []

    shopping_quality = 0
    transport_quality = 0
    food_drink_quality = 0
    education_quality = 0
    healthcare_quality = 0

    shopping_comment = 'There are no shopping places closer than 1km'
    transport_comment = 'There are no transport places closer than 500 meters'
    food_drink_comment = 'There are no food or drink places closer than 1km'
    education_comment = 'There are no education places closer than 1km'
    healthcare_comment = 'There are no healthcare places closer than 1km'

    for place in places:
        if place.group == PlaceEnum.SHOPS:
            shopping_comment = None
            shopping_places.append(place.json)
            shopping_quality = max(shopping_quality, place.quality)
        elif place.group == PlaceEnum.TRANSPORT:
            transport_comment = None
            transport_places.append(place.json)
            transport_quality = max(transport_quality, place.quality)
        elif place.group == PlaceEnum.FOOD:
            food_drink_comment = None
            food_drink_places.append(place.json)
            food_drink_quality = max(food_drink_quality, place.quality)
        elif place.group == PlaceEnum.EDUCATION:
            education_comment = None
            education_places.append(place.json)
            education_quality = max(education_quality, place.quality)
        elif place.group == PlaceEnum.HEALTH:
            healthcare_comment = None
            healthcare_places.append(place.json)
            healthcare_quality = max(healthcare_quality, place.quality)

    r['details'].append(dict(
        name="Shopping",
        description="Shopping places in 1km radius",
        quality=shopping_quality,
        comment=shopping_comment,
        places=shopping_places
    ))

    r['details'].append(dict(
        name="Transport",
        description="Public transportation in 500m radius",
        quality=transport_quality,
        comment=transport_comment,
        places=transport_places
    ))

    r['details'].append(dict(
        name="Food and Drinks",
        description="Food, drink, and coffee places in radius 1km",
        quality=food_drink_quality,
        comment=food_drink_comment,
        places=food_drink_places
    ))

    r['details'].append(dict(
        name="Education",
        description="Educational facilities in 1km radius",
        quality=education_quality,
        comment=education_comment,
        places=education_places
    ))

    r['details'].append(dict(
        name="Healthcare",
        description="Hospitals and other medical facilities in 1km radius",
        quality=healthcare_quality,
        comment=healthcare_comment,
        places=healthcare_places
    ))

    # average quality
    r['quality'] = sum([detail['quality'] for detail in r['details']]) / 5.0

    return r
