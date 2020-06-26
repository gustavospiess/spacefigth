"""
Test the game creation and its properties
"""


import pytest  # type: ignore
from .. import game


def set_up_match():
    match_builer = game.MatchBuilder()
    player_a = match_builer.addPlayer()
    player_b = match_builer.addPlayer()
    match = match_builer.start()
    return (player_a, player_b, match)


def test_new_player_is_in_game():
    (player_a, player_b, match) = set_up_match()
    assert player_a in match.players
    assert player_b in match.players


def test_new_player_has_no_events():
    match_builer = game.MatchBuilder()
    player = match_builer.addPlayer()
    assert player.onSensor is None
    assert player.onAction is None


def test_player_keeps_events():
    (player_a, player_b, match) = set_up_match()

    def sensor(state):
        return None

    def action():
        pass

    player_a.setOnSensor(sensor)
    player_a.setOnAction(action)

    assert sensor == player_a.onSensor
    assert action == player_a.onAction


def test_match_cant_start_with_less_than_two_players():
    match_builer = game.MatchBuilder()

    with (pytest.raises(game.NotEnouthPlayers)):
        match_builer.start()

    match_builer.addPlayer()
    with (pytest.raises(game.NotEnouthPlayers)):
        match_builer.start()

    match_builer.addPlayer()
    match_builer.start()


def test_before_start_match_players_have_no_position():
    match_builer = game.MatchBuilder()
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

    def on_sensor_call_back(state: game.Sensor):
        called['on_sensor'] = True

    def on_action_call_back() -> game.Action:
        called['on_action'] = True
        return game.Action()

    player_a.setOnSensor(on_sensor_call_back)
    player_a.setOnAction(on_action_call_back)

    assert not called['on_sensor']
    assert not called['on_action']

    match.ticTimer()

    assert called['on_sensor']
    assert called['on_action']
