import functools
import random as rd
import typing as tp
from math import sqrt


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
        return self._distance()

    @functools.lru_cache(maxsize=1)
    def _distance(self) -> float:
        delta_x, delta_y, delta_z = self.delta
        return sqrt(delta_x**2 + delta_y**2 + delta_z**2)

    @property
    def delta(self) -> tp.Tuple[float, float, float]:
        return self._delta()

    @functools.lru_cache(maxsize=1)
    def _delta(self) -> tp.Tuple[float, float, float]:
        """Calculates de diference from both ends `destin-origin`"""
        o = self.origin
        d = self.destin
        return (d.x - o.x, d.y - o.y, d.z - o.z)

    @functools.lru_cache(maxsize=32)
    def scale(self, length: float) -> 'LineSegment':
        """Calculates the line with same origin and and slope, with the length
        equals to `length`"""
        delta = self.delta
        distance = self.distance
        movement = Position(*map(lambda i: i/distance*length, delta))
        return LineSegment(self.origin, self.origin.add(movement))


def randomPosition(bounds: float = 100.0) -> 'Position':
    """Generates a new position inside the bounds"""
    def _in_bounds():
        return rd.random() * bounds * rd.choice((-1, 1))

    return Position(*[_in_bounds() for _ in range(3)])
