from rlbot.utils.structures.game_data_struct import GameTickPacket, Touch

from vitamins.geometry import Vec3
from vitamins.match.base import OrientedObject


class Ball(OrientedObject):
    """Represents a ball. Often hypothetical, e.g. the result of asking for a prediction
    of the future ball's position.
    """

    radius: float = 92.75
    latest_touch: Touch

    def __init__(self, packet=None, phys=None, time=0):
        super().__init__()
        self.velocity: Vec3 = Vec3()
        self.angular_velocity = Vec3()
        self.time = time
        self.update(packet, phys)

    def update(self, packet=None, phys=None):
        if packet is not None:
            self.latest_touch = packet.game_ball.latest_touch
            phys = packet.game_ball.physics
        self.position = Vec3(phys.location)
        self.velocity = Vec3(phys.velocity)
        self.angular_velocity = Vec3(phys.angular_velocity)

    def is_rolling(self):
        return self.z < 95 and abs(self.velocity.z) < 1


class TheBall(Ball):
    """The one true ball."""

    coarse: int = 16
    max_bounces = 5
    draw_path = False
    draw_bounces = False
    draw_rolling_transitions = False
    draw_seconds = False
    path_thickness = 1
    bounce_threshold = 300

    def __init__(self):
        self.bounces = []
        self.draw_path = True
        self.draw_bounces = True
        self.draw_step = 8
        self.draw_bounces = True
        self.on_opp_goal = False  # on a path to score!
        self.on_own_goal = False  # on a path to score...
        self.time_to_goal = 0
        self.next_prediction_update = 0
        self.prediction_interval = 1 / 2
        self.current_slice = 0
        self.prediction = None
        self.index_now = 0
        self.roll_time = None

    # todo: resolve signature mismatch.
    def update(self, packet: GameTickPacket):
        super().update(packet=packet)
        self.update_prediction()
        self.analyze_prediction(max_ms=2)
        if self.draw_path:
            self.draw_prediction(step=self.draw_step)

    def score(self, bot, dir=None):
        if dir is None:
            dir = bot.field.fwd
        self.velocity = dir * 2300
        self.position = bot.field.center + 5000 * dir + Vec3(z=500)
        self.reset(bot)

    def get_bounces(self) -> [Ball]:
        bounces = []
        for i, dv in self.bounces:
            b = Ball(
                phys=self.prediction.slices[i].physics,
                time=self.prediction.slices[i].game_seconds,
            )
            b.dv = dv
            bounces.append(b)
        return bounces
