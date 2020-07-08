import random as rd
import typing as tp
from math import sqrt


FloatIter = tp.Iterable[float]


class Position3D(tp.NamedTuple):
    x: float
    y: float
    z: float

    def add(self, other: 'Position3D') -> 'Position3D':
        return Position3D(*add(self, other))


class LineSegment(tp.NamedTuple):
    origin: Position3D
    destin: Position3D

    @property
    def distance(self) -> float:
        return distance(self.origin, self.destin)

    @property
    def delta(self) -> FloatIter:
        return deltas(self.destin, self.origin)

    @property
    def direction(self) -> FloatIter:
        return scale(self.delta, 1/self.distance)

    def resize(self, length: float) -> 'LineSegment':
        """Calculates the line with same origin and direction,
        with the length equals to `length`"""
        axis = add(self.origin, scale(self.direction, length))
        return LineSegment(self.origin, Position3D(*axis))

    def closest_point_inline(self, a: Position3D) -> Position3D:
        """Returns de closest position to a point `a` that is in this line
        segment
        """
        origin_to_a = LineSegment(self.origin, a)
        cosine = dot_product(self.delta, origin_to_a.delta) / self.distance
        return Position3D(*add(self.origin, scale(self.direction, cosine)))

    def distance_to(self, point: Position3D) -> float:
        """Calculates the minimum distance from point to any point in the line
        """
        return distance(point, self.closest_point_inline(point))


def squares(m: FloatIter) -> FloatIter:
    """Generate the squares of a float iterable
    >>> tuple(squares((1, 2, 3)))  # (1*1, 2*2, 3*3)
    (1, 4, 9)"""
    for _m in m:
        yield _m ** 2


def deltas(m: FloatIter, n: FloatIter) -> FloatIter:
    """Generate for the in place substractions:
    >>> tuple(deltas((1, 2, 3), (4, 5, 6)))  # (1-4, 2-5, 3-6)
    (-3, -3, -3)"""
    for _m, _n in zip(m, n):
        yield _m - _n


def add(m: FloatIter, n: FloatIter) -> FloatIter:
    """Generate for the in place addition:
    >>> tuple(add((1, 2, 3), (4, 5, 6)))  # (1+4, 2+5, 3+6)
    (5, 7, 9)"""
    for _m, _n in zip(m, n):
        yield _m + _n


def scale(m: FloatIter, s: float) -> FloatIter:
    """scale evenly by a constante
    >>> tuple(add((1, 2, 3), 2))  # (1*2, 2*2, 3*2)
    (2, 4, 6)"""
    for _m in m:
        yield _m * s


def dot_product(m: FloatIter, n: FloatIter) -> float:
    """Calculate the dot product of two float iterators
    >>> dot_product((1, 2, 3), (4, 5, 6))  # (1*4 + 2*5 + 3*6)
    34"""
    return sum(_m * _n for _m, _n in zip(m, n))


def distance(m: FloatIter, n: FloatIter) -> float:
    """Calculate the distance of two float iterators
    >>> distance((1, 1), (4, 5))  # sqrt((1-4)**2 + (1-5)**2)
    5"""
    return sqrt(square_distance(m, n))


def square_distance(m: FloatIter, n: FloatIter) -> float:
    """Calculate the square of the distance of two float iterators
    it's to be used to sortings as it is more performatic and keeps the sorting
    properties.

    >>> distance((1, 1), (4, 5))  # (1-4)**2 + (1-5)**2
    25"""
    return sum(squares(deltas(m, n)))


def random_position(bounds: float = 100.0) -> 'Position3D':
    """Generates a new position inside the bounds"""
    def _in_bounds():
        # return rd.random() * bounds * rd.choice((-1, 1))
        return rd.randint(0, bounds) * rd.choice((-1, 1))

    return Position3D(*[_in_bounds() for _ in range(3)])
