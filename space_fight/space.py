import functools
import random as rd
import typing as tp
from math import sqrt


float_it = tp.Iterable[float]


class Position(tp.NamedTuple):
    x: float
    y: float
    z: float

    @functools.lru_cache(maxsize=32)
    def add(self, other: 'Position') -> 'Position':
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)


class LineSegment(tp.NamedTuple):
    origin: Position
    destin: Position

    @property
    def distance(self) -> float:
        return _distance(self.origin, self.destin)

    @property
    def delta(self) -> float_it:
        return _delta(self.destin, self.origin)

    @property
    def direction(self) -> float_it:
        for d in self.delta:
            yield d/self.distance

    @functools.lru_cache(maxsize=32)
    def resize(self, length: float) -> 'LineSegment':
        """Calculates the line with same origin and and diretction,
        with the length equals to `length`"""
        axis = (d * length + o for d, o in zip(self.direction, self.origin))
        return LineSegment(self.origin, Position(*axis))

    @functools.lru_cache(maxsize=32)
    def distance_to(self, point: Position) -> float:
        """Calculates the minimum distance from point to any point in the line
        """
        from_origin = LineSegment(self.origin, point)
        mag = self.distance*from_origin.distance
        cos = _dot_product(self.delta, from_origin.delta)/mag
        tang = self.resize(cos * from_origin.distance).destin
        return _distance(point, tang)


def _delta(m: float_it, n: float_it) -> float_it:
    """Generate for the in place substractions:
        `_delta((1, 2, 3), (4, 5, 6)) = (1-4, 2-5, 3-6)`"""
    for _m, _n in zip(m, n):
        yield _m - _n


def _square(m: float_it) -> float_it:
    for _m in m:
        yield _m ** 2


@functools.lru_cache(maxsize=32)
def _distance(m: float_it, n: float_it) -> float:
    return sqrt(sum(_square(_delta(m, n))))


@functools.lru_cache(maxsize=32)
def _dot_product(m: float_it, n: float_it) -> float:
    return sum(_m * _n for _m, _n in zip(m, n))


def randomPosition(bounds: float = 100.0) -> 'Position':
    """Generates a new position inside the bounds"""
    def _in_bounds():
        # return rd.random() * bounds * rd.choice((-1, 1))
        return rd.randint(0, bounds) * rd.choice((-1, 1))

    return Position(*[_in_bounds() for _ in range(3)])
