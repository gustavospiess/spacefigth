import pytest  # type: ignore
from .. import space


def set_up_match():
    match_builer = space.MatchBuilder()
    player_a = match_builer.addPlayer()
    player_b = match_builer.addPlayer()
    match = match_builer.start()
    return (player_a, player_b, match)


def test_new_player_is_in_game():
    (player_a, player_b, match) = set_up_match()
    assert player_a in match.players
    assert player_b in match.players


def test_new_player_has_no_events():
    match_builer = space.MatchBuilder()
    player = match_builer.addPlayer()
    assert len(player.onSensor) == 0
    assert len(player.onAction) == 0


def test_player_keeps_events():
    (player_a, player_b, match) = set_up_match()

    def sensor(state):
        return None

    def action():
        pass

    player_a.appendOnSensor(sensor)
    player_a.appendOnAction(action)

    assert sensor in player_a.onSensor
    assert action in player_a.onAction


def test_match_cant_start_with_less_than_two_players():
    match_builer = space.MatchBuilder()

    with (pytest.raises(space.NotEnouthPlayers)):
        match_builer.start()

    match_builer.addPlayer()
    with (pytest.raises(space.NotEnouthPlayers)):
        match_builer.start()

    match_builer.addPlayer()
    match_builer.start()


def test_before_start_match_players_have_no_position():
    match_builer = space.MatchBuilder()
    player_a = match_builer.addPlayer()
    player_b = match_builer.addPlayer()
    assert player_a.position is None
    assert player_b.position is None


def test_after_start_match_players_have_diferente_positions():
    (player_a, player_b, match) = set_up_match()
    assert player_a.position != player_b.position


def test_started_match_inreases_time_by_one_after_tic():
    (player_a, player_b, match) = set_up_match()
    time_pre_tic = match.time
    match.ticTimer()
    time_pos_tic = match.time
    assert time_pre_tic + 1 == time_pos_tic


def test_execute_action_event_on_tic():
    (player_a, player_b, match) = set_up_match()

    called = {'on_sensor': False, 'on_action': False}

    def on_sensor_call_back(state: space.SensorState):
        called['on_sensor'] = True

    def on_action_call_back() -> space.ActionSet:
        called['on_action'] = True
        return space.ActionSet()

    player_a.appendOnSensor(on_sensor_call_back)
    player_a.appendOnAction(on_action_call_back)

    assert not called['on_sensor']
    assert not called['on_action']

    match.ticTimer()

    assert called['on_sensor']
    assert called['on_action']


def test_on_sensor_informs_current_fuel():
    (player_a, player_b, match) = set_up_match()

    f = 10.5

    def on_sensor_call_back(state: space.SensorState):
        assert state.fuel == f
    player_a.appendOnSensor(on_sensor_call_back)
    player_a._fuel = f
    match.ticTimer()


def test_on_sensor_informs_current_position():
    (player_a, player_b, match) = set_up_match()

    position_p = space.randomPosition()

    def on_sensor_call_back(state: space.SensorState):
        assert state.position == position_p
    player_a.appendOnSensor(on_sensor_call_back)
    player_a._position = position_p
    match.ticTimer()


def test_on_action_allow_moving():
    (player_a, player_b, match) = set_up_match()
    player_a._fuel = 50

    move_one = space.Position(0, 0, 1).add
    pos_list = [player_a.position]

    def on_action_call_back() -> space.ActionSet:
        new_pos = move_one(player_a.position)
        pos_list.append(new_pos)
        return space.ActionSet(move_to=new_pos)

    player_a.appendOnAction(on_action_call_back)
    for i in range(10):
        match.ticTimer()
        assert pos_list[i+1] == move_one(pos_list[i])


def test_movement_is_limited_by_fuel():
    (player_a, player_b, match) = set_up_match()
    player_a._fuel = 5

    move_one = space.Position(0, 0, 1).add

    pos_list = [player_a.position]

    def on_action_call_back() -> space.ActionSet:
        new_pos = move_one(player_a.position)
        pos_list.append(new_pos)
        return space.ActionSet(move_to=new_pos)

    player_a.appendOnAction(on_action_call_back)
    for i in range(10):
        match.ticTimer()
    for i in range(4):
        print(i, pos_list[i+1], move_one(pos_list[i]))
        assert pos_list[i+1] == move_one(pos_list[i])
    for i in range(5, 10):
        print(i, pos_list[i+1], move_one(pos_list[i]))


def test_movement_distance_is_limited_by_fuel():
    (player_a, player_b, match) = set_up_match()
    player_a._fuel = 10

    move_two = space.Position(0, 0, 2).add

    pos_list = [player_a.position]

    def on_action_call_back() -> space.ActionSet:
        new_pos = move_two(player_a.position)
        pos_list.append(new_pos)
        return space.ActionSet(move_to=new_pos)

    player_a.appendOnAction(on_action_call_back)
    for i in range(10):
        match.ticTimer()
    for i in range(5):
        assert pos_list[i+1] == move_two(pos_list[i])
    for i in range(6, 10):
        assert pos_list[i+1] == pos_list[i]


def test_partial_movement_limited_by_fuel():
    (player_a, player_b, match) = set_up_match()
    player_a._fuel = 1

    move_two = space.Position(0, 0, 2).add
    move_one = space.Position(0, 0, 1).add

    old_pos = player_a.position
    player_a.appendOnAction(
            lambda: space.ActionSet(move_to=move_two(player_a.position)))
    match.ticTimer()
    assert player_a.position == move_one(old_pos)
