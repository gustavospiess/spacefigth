import typing as tp
import dataclasses
import random as rd


class Position(tp.NamedTuple):
    x: int
    y: int
    z: int

    @classmethod
    def randomPosition(cls, bounds = 100):
        """Generates a new position inside the bounds"""
        return cls(*[rd.randint(-1*bounds, bounds) for _ in range(3)])


@dataclasses.dataclass
class SensorState():
    """TODO"""
    fuel:float = dataclasses.field(default=0.0, compare=True, init=True)


@dataclasses.dataclass
class ActionSet():
    """TODO"""
    pass


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

class Match(object):
    """A handler for a single match"""
    def __init__(self, player_set: tp.Set[_Player]):
        self._players = player_set
        self._time = 0

        self._init_player_pos()

    def _init_player_pos(self):
        position_set = set()
        while len(position_set) < len(self.players):
            pos = Position.randomPosition()
            position_set.add(pos)
        for player in self.players:
            player._position = position_set.pop()

    def ticTimer(self):
        for player in self._players:
            sensor_state = SensorState(fuel = player.fuel);
            for sensor in player.onSensor:
                sensor(sensor_state)
            actionSet = None
            for action in player.onAction:
                actionSet = action()
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
