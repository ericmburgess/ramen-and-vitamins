"""vitamins.match.match -- Class for representing the current match."""
from typing import List

from rlbot.agents.base_agent import BaseAgent
from rlbot.utils.structures.game_data_struct import GameTickPacket

from vitamins.match.ball import Ball
from vitamins.match.car import Car
from vitamins.match.field import Field
from vitamins.match.prediction import BallPredictor


class Match:
    agent: BaseAgent = None
    time: float = 0
    current_prediction: BallPredictor = None
    next_prediction: BallPredictor = None
    max_prediction_age = 0.5
    agent_car: Car = None
    field: Field = None
    ball: Ball = None
    cars: List[Car] = []
    teammates: List[Car] = []
    opponents: List[Car] = []

    @classmethod
    def initialize(cls, agent: BaseAgent, packet: GameTickPacket):
        cls.agent = agent
        cls.field = Field(agent.team, agent.get_field_info())
        cls.cars = [Car(index=i, packet=packet) for i in range(packet.num_cars)]
        cls.agent_car = cls.cars[cls.agent.index]
        cls.teammates = [car for car in cls.cars if car.team == cls.agent.team]
        cls.opponents = [car for car in cls.cars if car.team != cls.agent.team]
        cls.ball = Ball(packet=packet)
        cls.current_prediction = BallPredictor(cls.agent.get_ball_prediction_struct())
        cls.update(packet)

    @classmethod
    def update(cls, packet: GameTickPacket):
        cls.packet = packet
        cls.time = packet.game_info.seconds_elapsed
        for car in cls.cars:
            car.update(packet=packet)
        cls.ball.update(packet=packet)
        cls.field.update(packet=packet)
        cls.update_ball_prediction(packet=packet)

    @classmethod
    def update_ball_prediction(cls, packet):
        if (
            cls.current_prediction.valid
            and cls.current_prediction.age < cls.max_prediction_age
        ):
            cls.current_prediction.update(packet)
        else:
            if cls.next_prediction is None:
                cls.next_prediction = BallPredictor(
                    cls.agent.get_ball_prediction_struct()
                )
            elif cls.next_prediction.ready:
                cls.current_prediction = cls.next_prediction
                cls.next_prediction = None

    @classmethod
    def predict_ball(cls, dt: float = 0) -> Ball:
        if cls.current_prediction is None:
            return cls.ball
        else:
            return cls.current_prediction.predict(dt)

    @classmethod
    def refs_1v1(cls):
        return cls.agent_car, cls.opponents[0], cls.ball, cls.field, cls.predict_ball
