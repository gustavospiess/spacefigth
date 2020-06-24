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


class EnemyPos(tp.NamedTuple):
    pos: Position
    time: int


class EnemyTrace(tp.NamedTuple):
    corse: LineSegment
    time: int


class SensorState(tp.NamedTuple):
    """TODO"""
    fuel: float = 0.0
    position: tp.Union[Position, None] = None
    missile_ready: bool = False
    enemy: tp.Union[tp.Set[EnemyPos], None] = None
    enemy_trace: tp.Union[tp.Set[EnemyTrace], None] = None


class ActionSet(tp.NamedTuple):
    """TODO"""
    move_to: tp.Union[Position, None] = None


onSensorEvent = tp.List[tp.Callable[[SensorState], tp.NoReturn]]
onActionEvent = tp.List[tp.Callable[[], ActionSet]]


class NotEnouthPlayers(Exception):
    pass


class _Player(object):
    """Player interface"""
    def __init__(self):
        self._onSensor: tp.Set[onSensorEvent] = set()
        self._onAction: tp.Set[onActionEvent] = set()
        self._position: 'Position' = None
        self._fuel: float = 0.0

    @property
    def onSensor(self) -> tp.FrozenSet[onSensorEvent]:
        """The onSensor event set."""
        return frozenset(self._onSensor)

    @property
    def onAction(self) -> tp.FrozenSet[onActionEvent]:
        """The onSensor event set."""
        return frozenset(self._onAction)

    @property
    def position(self) -> Position:
        return self._position

    @property
    def fuel(self) -> float:
        return self._fuel

    def appendOnSensor(self, sensor: onSensorEvent) -> None:
        """Add event to on sensor call"""
        self._onSensor.add(sensor)

    def appendOnAction(self, action: onActionEvent) -> None:
        """Add event to on action call"""
        self._onAction.add(action)

    @property
    def baseState(self) -> SensorState:
        return SensorState(fuel=self.fuel, position=self.position)


class Match(object):
    """A handler for a single match"""
    def __init__(self, player_set: tp.Set[_Player]):
        self._players = player_set
        self._time = 0
        self._action_dict: tp.Dict[_Player, ActionSet] = dict()

        self._init_player_pos()

    def _init_player_pos(self):
        position_set = set()
        while len(position_set) < len(self.players):
            pos = randomPosition()
            position_set.add(pos)
        for player in self.players:
            player._position = position_set.pop()

    def _iterate_players_sensor(self):
        for player in self._players:
            sensor_state = player.baseState
            for sensor in player.onSensor:
                sensor(sensor_state)

            action_set = None
            for action in player.onAction:
                action_set = action()
            self._action_dict[player] = action_set

    def _iterate_players_action(self):
        for player in self._players:
            action_set = self._action_dict[player]
            if (action_set is None or action_set.move_to is None):
                break
            if (player.fuel == 0):
                break

            corse = LineSegment(player.position, action_set.move_to)

            if corse.distance > player.fuel:
                corse = corse.scale(player.fuel)

            player._fuel -= corse.distance
            player._position = corse.destin

    def ticTimer(self):
        self._iterate_players_sensor()
        self._iterate_players_action()

        self._time += 1

    @property
    def time(self):
        """global timer to the match"""
        return self._time

    @property
    def players(self) -> tp.Set[_Player]:
        """Return player list of the match"""
        return self._players


class MatchBuilder(object):
    """Builder to preset the Match"""

    def __init__(self):
        self._players = list()

    def addPlayer(self) -> '_Player':
        """Generates new player in the match and return it"""
        new_player = _Player()
        self._players.append(new_player)
        return new_player

    def start(self):
        if len(self._players) < 2:
            raise NotEnouthPlayers()
        return Match(self._players)


def randomPosition(bounds: float = 100.0) -> 'Position':
    """Generates a new position inside the bounds"""
    def _in_bounds():
        return rd.random() * bounds * rd.choice((-1, 1))

    return Position(*[_in_bounds() for _ in range(3)])
