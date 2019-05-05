import logging
import typing

import math

from .czech_data import AREAS


class MapaCriminalityAPIWrapper(object):
    """Wraps HERE API request creation and provides simple interface for purposes of our project"""

    @staticmethod
    def inside(lat: float, lng: float, polygon: typing.List[typing.Tuple[float, float]]) -> bool:
        """Determines whether coordinates are inside of a polygon

        :param lat: latitude
        :param lng: longitude
        :param polygon: list of coordinates
        :return: true if coordinates are within the polygon
        """
        n = len(polygon)
        angle = 0.0
        for i, point in enumerate(polygon):
            p_lat = point[0] - lat
            p_lng = point[1] - lng
            next_lat = polygon[(i + 1) % n][0] - lat
            next_lng = polygon[(i + 1) % n][1] - lng
            angle += MapaCriminalityAPIWrapper.angle_2d(p_lat, p_lng, next_lat, next_lng)

        return abs(angle) >= math.pi

    @staticmethod
    def angle_2d(y1: float, x1: float, y2: float, x2: float) -> float:
        theta1 = math.atan2(y1, x1)
        theta2 = math.atan2(y2, x2)
        d = theta2 - theta1
        while d > math.pi:
            d -= math.pi * 2
        while d < -math.pi:
            d += math.pi * 2
        return d

    def get_area(self, lat: float, lng: float) -> typing.Tuple[str, typing.Optional[int]]:
        logging.info(
            'Running area get for lat: `{}`, lng: `{}`'.format(lat, lng)
        )
        self.run_test()
        for area in AREAS:
            outer_polygon = area.get('Geometry', [])
            logging.warning(len(outer_polygon))
            inner_polygons = area.get('Inner', [])
            inside = self.inside(lat, lng, outer_polygon)
            if not inside:
                continue

            logging.warning('input found in outer area: `{}`'.format(area.get('Name', '')))

            in_inner = False
            for polygon in inner_polygons:
                if self.inside(lat, lng, polygon):
                    in_inner = True
                    logging.warning('input found in inner polygon')
                    break

            if not in_inner:
                return area.get('Name', ''), area.get('id', None)

        return '', None

    def run_test(self):
        florida = [
            (31.000213, -87.584839),
            (31.009629, -85.003052),
            (30.726726, -84.838257),
            (30.584962, -82.168579),
            (30.73617, -81.476441),
            (29.002375, -80.795288),
            (26.896598, -79.938355),
            (25.813738, -80.059204),
            (24.93028, -80.454712),
            (24.401135, -81.817017),
            (24.700927, -81.959839),
            (24.950203, -81.124878),
            (26.0015, -82.014771),
            (27.833247, -83.014527),
            (28.8389, -82.871704),
            (29.987293, -84.091187),
            (29.539053, -85.134888),
            (30.272352, -86.47522),
            (30.281839, -87.628784),
        ]

        assert self.inside(
            lat=25.7814014,
            lng=-80.186969,
            polygon=florida
        )
        logging.info('First assert passed')

        assert not self.inside(
            lat=25.831538,
            lng=-1.069338,
            polygon=florida
        )
        logging.info('Second assert passed')
