"""vitamins.match.base -- base objects."""

from vitamins.geometry import Vec3, Orientation
from vitamins import math


class Location(Vec3):
    """Objects that have a location."""

    modified: bool = False

    @property
    def position(self) -> Vec3:
        return Vec3(self.x, self.y, self.z)

    @position.setter
    def position(self, value: Vec3):
        self.x, self.y, self.z = value
        self.modified = True


class MovingLocation(Location):
    """Location that has a velocity."""

    def __init__(self, position: Vec3, velocity: Vec3):
        super().__init__(position)
        self.velocity = velocity

    @property
    def speed(self):
        return self.velocity.length()

    @property
    def direction(self):
        return self.velocity.normalized()

    def relative_velocity(self, other: Vec3) -> Vec3:
        if hasattr(other, "velocity"):
            return self.velocity - other.velocity
        else:
            return self.velocity

    def speed_toward(self, other) -> float:
        """Closing speed (positive=approaching, negative=away)."""
        return self.relative_velocity(other).dot(self.to(other).normalized())


class OrientedObject(Location):
    """GameObjects that also have velocity, angular velocity, and orientation."""

    def __init__(
        self,
        position: Vec3 = 0,
        velocity: Vec3 = 0,
        angular_velocity: Vec3 = 0,
        orientation: Orientation = None,
    ):
        super().__init__(position)
        self.velocity = Vec3(velocity)
        self.angular_velocity = Vec3(angular_velocity)
        if orientation is None:
            orientation = Orientation(Vec3())
        self.orientation = orientation

    @property
    def up(self)->Vec3:
        return self.orientation.up

    @property
    def down(self)->Vec3:
        return -self.orientation.up

    @property
    def left(self)->Vec3:
        return -self.orientation.right

    @property
    def right(self)->Vec3:
        return self.orientation.right

    @property
    def forward(self)->Vec3:
        return self.orientation.forward

    @property
    def backward(self)->Vec3:
        return -self.orientation.forward

    @property
    def yaw(self)->float:
        return self.orientation.yaw

    @property
    def pitch(self)->float:
        return self.orientation.pitch

    @property
    def roll(self)->float:
        return self.orientation.roll

    @property
    def yaw_rate(self)->float:
        return self.angular_velocity.dot(self.orientation.up)

    @property
    def pitch_rate(self)->float:
        return self.angular_velocity.dot(-self.orientation.right)

    @property
    def roll_rate(self)->float:
        return self.angular_velocity.dot(-self.orientation.forward)

    def yaw_to(self, other: Vec3)->float:
        """Returns the yaw angle from the object's forward vector to the given location
        (projected onto the object's horizontal plane).
        """
        ovec = self.to(other)
        ox = ovec.dot(self.left)
        oy = ovec.dot(self.forward)
        return -math.atan2(ox, oy)
