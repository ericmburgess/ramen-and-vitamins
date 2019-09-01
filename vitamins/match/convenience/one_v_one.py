"""vitamins.match.convenience.one_v_one.py -- Convenient references to game objects
in 1v1 matches.

Intended use:
    from vitamins.match.convenience.one_v_one import *
"""

from vitamins.match.ball import Ball
from vitamins.match.car import Car
from vitamins.match.field import Field
from vitamins.match.match import Match

car: Car = None
opponent: Car = None
field: Field = None
ball: Ball = None


def convenience_initialize():
    """Needs to be called after Match is initialized."""
    global car, opponent, field, ball
    car = Match.agent_car
    if Match.opponents:
        opponent = Match.opponents[0]
    field = Match.field
    ball = Match.ball


def future_ball(dt: float = 0) -> Ball:
    return Match.predict_ball(dt)
