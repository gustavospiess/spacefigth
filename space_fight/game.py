import typing as tp
from .space import LineSegment, randomPosition, Position


class NotEnouthPlayers(Exception):
    pass


class EnemyPos(tp.NamedTuple):
    pos: Position
    time: int


class EnemyTrace(tp.NamedTuple):
    corse: LineSegment
    time: int


class Sensor(tp.NamedTuple):
    """TODO"""
    fuel: float = 0.0
    position: tp.Union[Position, None] = None
    missile_ready: bool = False
    enemy: tp.Union[tp.Set[EnemyPos], None] = None
    enemy_trace: tp.Union[tp.Set[EnemyTrace], None] = None


class Action(tp.NamedTuple):
    """TODO"""
    move_to: tp.Union[Position, None] = None


onActionEvent = tp.List[tp.Callable[[], Action]]
onSensorEvent = tp.List[tp.Callable[[Sensor], tp.NoReturn]]


class _Player(object):
    """Player interface"""
    def __init__(self):
        self._onSensor: onSensorEvent = None
        self._onAction: onActionEvent = None
        self._position: 'Position' = None
        self._fuel: float = 0.0

    @property
    def onSensor(self) -> onSensorEvent:
        """The onSensor event set."""
        return self._onSensor

    @property
    def onAction(self) -> onActionEvent:
        """The onSensor event set."""
        return self._onAction

    @property
    def position(self) -> Position:
        return self._position

    @property
    def fuel(self) -> float:
        return self._fuel

    def setOnSensor(self, sensor: onSensorEvent) -> None:
        """Set event to on sensor call"""
        self._onSensor = sensor

    def setOnAction(self, action: onActionEvent) -> None:
        """Set event to on action call"""
        self._onAction = action

    @property
    def baseState(self) -> Sensor:
        return Sensor(fuel=self.fuel, position=self.position)


class Match(object):
    """A handler for a single match"""
    def __init__(self, player_set: tp.Set[_Player]):
        self._players = player_set
        self._time = 0
        self._action_dict: tp.Dict[_Player, Action] = dict()

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
            if player.onSensor:
                sensor_state = player.baseState
                player.onSensor(sensor_state)

            if player.onAction:
                action_set = player.onAction()
                self._action_dict[player] = action_set

    def _iterate_players_action(self):
        for player in self._action_dict.keys():
            action_set = self._action_dict[player]
            if (action_set is None or action_set.move_to is None):
                break
            if (player.fuel == 0):
                break

            corse = LineSegment(player.position, action_set.move_to)

            if corse.distance > player.fuel:
                corse = corse.resize(player.fuel)

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
