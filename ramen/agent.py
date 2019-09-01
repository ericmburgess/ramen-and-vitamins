"""ramen.agent -- Base class for Agents."""

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from vitamins.match.match import Match


class Agent(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.controls = SimpleControllerState()
        self.tick: int = 0

    def clear_controls(self):
        self.controls.yaw = 0
        self.controls.roll = 0
        self.controls.pitch = 0
        self.controls.steer = 0
        self.controls.throttle = 0
        self.controls.boost = False
        self.controls.handbrake = False
        self.controls.jump = False
        self.controls.use_item = False

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.renderer.begin_rendering()

        if self.tick == 0:
            # First tick setup:
            Match.initialize(self, packet)
            self.first_tick()

        Match.update(packet)

        self.every_tick()

        self.tick += 1
        self.renderer.end_rendering()
        return self.controls

    def every_tick(self, match:type):
        raise NotImplemented

    def first_tick(self):
        raise NotImplemented
