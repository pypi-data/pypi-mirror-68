from .distance_wtext import Distance_wText
from .shape import Shape
from .point import Point
from .text import Text
from .triangle import Triangle
from .rectangle import Rectangle


class SimplySupportedBeam(Shape):
    _position: Point
    _size: float

    def __init__(self, position: Point, size: float):
        super().__init__()
        p0 = Point(position.x - size / 2., position.y - size)
        p1 = Point(position.x + size / 2., position.y - size)
        triangle = Triangle(p0, p1, position)
        gap = size / 5.
        h = size / 4.  # height of rectangle
        p2 = Point(p0.x, p0.y - gap - h)
        rectangle = Rectangle(p2, size, h).set_fill_pattern('/')
        self.shapes = {'triangle': triangle, 'rectangle': rectangle}

        self.dimensions = {'position': Text('position', position),
                           'size': Distance_wText(Point(p2.x, p2.y - size),
                                                  Point(p2.x + size, p2.y - size),
                                                  'size')}

    def geometric_features(self):
        t = self.shapes['triangle']
        r = self.shapes['rectangle']
        d = {'pos': t.geometric_features()['p2'],
             'mid_support': r.geometric_features()['lower_mid']}
        return d

