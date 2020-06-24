import typing as tp
import dataclasses
import random as rd
from math import sqrt


class Position(tp.NamedTuple):
    x: float
    y: float
    z: float

    @classmethod
    def randomPosition(cls, bounds = 100):
        """Generates a new position inside the bounds"""
        return cls(*[rd.randint(-1*bounds, bounds) for _ in range(3)])
    
    def add(self, other: 'Position') -> 'Position':
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)

    def delta_to(self, other: 'Position') -> 'Position':
        return Position(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance(self, other: 'Position') -> float:
        delta_x, delta_y, delta_z = self.delta_to(other)
        return sqrt(delta_x**2 + delta_y**2 +delta_z**2)


class Line(tp.NamedTuple):
    origin: Position
    destin: Position

    def distance(self):
        return self.destin.distance(self.origin)

    def at_length(self, length: float) -> 'Position':
        delta = self.destin.delta_to(self.origin)
        distance = self.distance()
        movement = Position(*map(lambda i: i/distance*length, delta))
        return self.origin.add(movement)


@dataclasses.dataclass
class SensorState():
    """TODO"""
    fuel: float = dataclasses.field(default=0.0)
    position: tp.Union[Position, None] = dataclasses.field(default=None)


@dataclasses.dataclass
class ActionSet():
    """TODO"""
    move_to: tp.Union[Position, None] = dataclasses.field(default=None)


onSensorEvent = tp.List[tp.Callable[[SensorState], tp.NoReturn]];
onActionEvent = tp.List[tp.Callable[[], ActionSet]];


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
            pos = Position.randomPosition()
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
            if (action_set == None): break
            if (action_set.move_to == None): break
            if (player.fuel == 0): break

            destination = action_set.move_to
            distance = destination.distance(player.position)

            if distance > player.fuel:
                line = Line(player.position, destination)
                destination = line.at_length(player.fuel)
                distance = destination.distance(player.position)

            player._fuel -= distance
            player._position = destination

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
