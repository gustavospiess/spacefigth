"""
Test the game creation and its properties
"""


import pytest  # type: ignore
from .. import space
from .. import game


def set_up_match():
    match_builer = game.MatchBuilder()
    player = match_builer.addPlayer()
    match_builer.addPlayer()

    match = match_builer.start()

    return (player, match)


@pytest.mark.parametrize('f', [1, 0, 15.5])
def test_on_sensor_informs_current_fuel(f):
    (player, match) = set_up_match()

    def on_sensor_call_back(state: game.Sensor):
        assert state.fuel == f

    player.appendOnSensor(on_sensor_call_back)
    player._fuel = f
    match.ticTimer()


@pytest.mark.parametrize(
        'position', [space.randomPosition() for _ in range(4)])
def test_on_sensor_informs_current_position(position):
    (player, match) = set_up_match()

    def on_sensor_call_back(state: game.Sensor):
        assert state.position == position
    player.appendOnSensor(on_sensor_call_back)
    player._position = position
    match.ticTimer()


@pytest.mark.parametrize('direction', [(1, 0, 0), (0, 1, 0), (0, 0, 1)])
def test_on_action_allow_moving(direction):
    (player, match) = set_up_match()
    player._fuel = 50

    move_one = space.Position(*direction).add
    pos_list = [player.position]

    def on_action_call_back() -> game.Action:
        new_pos = move_one(player.position)
        pos_list.append(new_pos)
        return game.Action(move_to=new_pos)

    player.appendOnAction(on_action_call_back)
    for i in range(10):
        match.ticTimer()
        assert pos_list[i+1] == move_one(pos_list[i])


@pytest.mark.parametrize('direction', [(1, 0, 0), (0, 1, 0), (0, 0, 1)])
def test_movement_is_limited_by_fuel(direction):
    (player, match) = set_up_match()
    player._fuel = 5

    move_one = space.Position(*direction).add

    pos_list = [player.position]

    def on_action_call_back() -> game.Action:
        new_pos = move_one(player.position)
        pos_list.append(new_pos)
        return game.Action(move_to=new_pos)

    player.appendOnAction(on_action_call_back)
    for i in range(10):
        match.ticTimer()
    for i in range(4):
        print(i, pos_list[i+1], move_one(pos_list[i]))
        assert pos_list[i+1] == move_one(pos_list[i])
    for i in range(5, 10):
        print(i, pos_list[i+1], move_one(pos_list[i]))


@pytest.mark.parametrize('direction', [(2, 0, 0), (0, 2, 0), (0, 0, 2)])
@pytest.mark.parametrize('steps', range(6))
def test_movement_distance_is_limited_by_fuel(direction, steps):
    (player, match) = set_up_match()
    player._fuel = steps * 2

    move_two = space.Position(*direction).add

    pos_list = [player.position]

    def on_action_call_back() -> game.Action:
        new_pos = move_two(player.position)
        pos_list.append(new_pos)
        return game.Action(move_to=new_pos)

    player.appendOnAction(on_action_call_back)
    for i in range(10):
        match.ticTimer()
    for i in range(steps):
        assert pos_list[i+1] == move_two(pos_list[i])
    for i in range(steps + 1, 10):
        assert pos_list[i+1] == pos_list[i]


@pytest.mark.parametrize('desired_distance', range(1, 11, 2))
@pytest.mark.parametrize('fuel_capacity', range(0, 10, 2))
def test_partial_movement_limited_by_fuel(desired_distance, fuel_capacity):
    (player, match) = set_up_match()
    player._fuel = fuel_capacity

    move_desire = space.Position(0, 0, desired_distance).add
    move_fuel = space.Position(0, 0, fuel_capacity).add

    old_pos = player.position
    player.appendOnAction(
            lambda: game.Action(move_to=move_desire(player.position)))
    match.ticTimer()
    if fuel_capacity > desired_distance:
        assert player.position == move_desire(old_pos)
    else:
        assert player.position == move_fuel(old_pos)
