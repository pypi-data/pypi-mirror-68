from .matplotlibdraw import MatplotlibDraw
from .shape import Shape
from .point import Point
from .curve import Curve
from .text import Text


class Triangle(Shape):
    """
    Triangle defined by its three vertices p1, p2, and p3.

    Recorded geometric features:

    ==================== =============================================
    Attribute            Description
    ==================== =============================================
    p1, p2, p3           Corners as given to the constructor.
    ==================== =============================================

    """

    def __init__(self, p1: Point, p2: Point, p3: Point):
        super().__init__()
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3
        self._shapes = {'triangle': Curve([p1, p2, p3, p1])}

        # Dimensions
        self.dimensions = {'p1': Text('p1', p1),
                           'p2': Text('p2', p2),
                           'p3': Text('p3', p3)}

    def geometric_features(self):
        return {'p1': self._p1,
                'p2': self._p2,
                'p3': self._p3}
