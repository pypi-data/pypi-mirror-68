import numpy as np
from typing import Tuple

from .matplotlibdraw import MatplotlibDraw
from .shape import Shape
from .point import Point
from .curve import Curve


class Line(Shape):
    _start: Point
    _end: Point

    def __init__(self, start: Point, end: Point, arrow=None):
        super().__init__()
        self._start = start
        self._end = end
        self._arrow = arrow
        self._shapes = {'line': Curve([self._start, self._end])}
        self['line'].arrow = self._arrow
        self._a = self._b = self._c = self._d = None
        self._compute_formulas()

    def geometric_features(self):
        return {'start': self._start,
                'end': self._end}

    def interval(self, x_range: Tuple[float, float] = None, y_range: Tuple[float, float] = None):
        """Return part of the line defined either by the x_range or the y_range"""
        if x_range is not None:
            return Line(Point(x_range[0], self(x_range[0])),
                        Point(x_range[1], self(x_range[1])))
        elif y_range is not None:
            return Line(Point(self(y_range[0]), y_range[0]),
                        Point(self(y_range[1]), y_range[1]))

    def _compute_formulas(self):
        # Define equations for line:
        # y = a*x + b,  x = c*y + d
        try:
            self._a = (self._end.y - self._start.y) / (self._end.x - self._start.x)
            self._b = self._start.y - self._a * self._start.x
        except ZeroDivisionError:
            # Vertical line, y is not a function of x
            self._a = None
            self._b = None
        try:
            if self._a is None:
                self._c = 0
            else:
                self._c = 1 / float(self._a)
            if self._b is None:
                self._d = self._end.x
        except ZeroDivisionError:
            # Horizontal line, x is not a function of y
            self._c = None
            self._d = None

    def __call__(self, x=None, y=None):
        """Given x, return y on the line, or given y, return x."""
        self._compute_formulas()
        if x is not None and self._a is not None:
            return self._a * x + self._b
        elif y is not None and self._c is not None:
            return self._c * y + self._d
        else:
            raise ValueError('Line.__call__(x=%s, y=%s) not meaningful' % (x, y))

    def rotate(self, angle: float, center: Point) -> 'Line':
        """
        Rotate all coordinates: `angle` is measured in radians
        center is the "origin" of the rotation.
        """
        print("rotating about %s" % center)
        angle = np.radians(angle)
        x, y = center.x, center.y
        c = np.cos(angle)
        s = np.sin(angle)
        start = Point(x + (self._start.x - x) * c - (self._start.y - y) * s,
                      y + (self._start.x - x) * s - (self._start.y - y) * c)
        end = Point(x + (self._end.x - x) * c - (self._end.y - y) * s,
                      y + (self._end.x - x) * s - (self._end.y - y) * c)
        return Line(start, end)

