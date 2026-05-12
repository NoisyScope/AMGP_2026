"""Movement module — drive the wheels and steering servo.

This module wraps the low-level `picarx` calls so the rest of the codebase
talks to friendly method names (`drive_forward`, `turn`, `stop`) instead
of remembering which method belongs to which library.

Extending this module:
    Add new behaviours (e.g. `spin_in_place`, `arc_left`) as new methods
    on the `Movement` class. Keep them small — one motion per method —
    and reuse the existing primitives below.
"""

from .config import (
    DEFAULT_SPEED,
    MAX_SPEED,
    MAX_STEERING_ANGLE,
    MIN_SPEED,
    MIN_STEERING_ANGLE,
)


def _clamp(value, lo, hi):
    """Return `value` clipped to the inclusive range [lo, hi]."""
    return max(lo, min(hi, value))


class Movement:
    """High-level driving controls for the PiCar-X.

    Parameters
    ----------
    px : picarx.Picarx
        An already-constructed Picarx hardware object. Passing it in
        (instead of creating one inside) lets several modules share
        the same hardware handle.
    """

    def __init__(self, px):
        self._px = px

    # -- Forward / backward -----------------------------------------------

    def drive_forward(self, speed=DEFAULT_SPEED):
        """Drive the car forward.

        `speed` is a number from 0 (stopped) to 100 (full speed). Values
        outside that range are clipped automatically so a typo cannot
        damage the motors.
        """
        speed = _clamp(speed, MIN_SPEED, MAX_SPEED)
        self._px.forward(speed)

    def drive_backward(self, speed=DEFAULT_SPEED):
        """Drive the car backward at the given speed (0–100)."""
        speed = _clamp(speed, MIN_SPEED, MAX_SPEED)
        self._px.backward(speed)

    def stop(self):
        """Stop both drive motors immediately."""
        self._px.stop()

    # -- Steering ----------------------------------------------------------

    def turn(self, angle):
        """Point the front wheels at the given steering angle.

        `angle` is in degrees, where 0 is straight ahead, negative
        values steer left, and positive values steer right. The PiCar-X
        servo can only physically reach about -35° to +35°, so larger
        values are clipped.

        Note: this only sets the wheel direction — it does not start
        the motors. Combine with `drive_forward` to actually move.
        """
        angle = _clamp(angle, MIN_STEERING_ANGLE, MAX_STEERING_ANGLE)
        self._px.set_dir_servo_angle(angle)

    def straighten(self):
        """Centre the steering (point the wheels straight ahead)."""
        self.turn(0)

    # -- Convenience combinations -----------------------------------------

    def turn_left(self, speed=DEFAULT_SPEED, angle=30):
        """Drive forward while steering left by the given angle."""
        self.turn(-abs(angle))
        self.drive_forward(speed)

    def turn_right(self, speed=DEFAULT_SPEED, angle=30):
        """Drive forward while steering right by the given angle."""
        self.turn(abs(angle))
        self.drive_forward(speed)
