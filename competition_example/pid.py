"""Minimal PID controller used by the lane-keeping loop.

A PID controller computes a correction from an error signal:
    output = Kp * error + Ki * integral(error) + Kd * derivative(error)

For lane keeping the error is "how many pixels is the road centre off
from the image centre", and the output is the steering angle.
"""

import time


class PID:
    """Standard time-aware PID controller.

    Parameters
    ----------
    kp, ki, kd : float
        Proportional, integral and derivative gains.
    output_limit : tuple(float, float) | None
        Optional (min, max) clamp applied to the controller output —
        useful so the steering command never exceeds the servo's
        physical range.
    """

    def __init__(self, kp, ki, kd, output_limit=None):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_limit = output_limit
        self._integral = 0.0
        self._last_error = 0.0
        self._last_time = None

    def reset(self):
        """Wipe accumulated state. Call when control mode changes
        (e.g. after a grayscale-triggered hard turn) so the integral
        and derivative do not carry stale history."""
        self._integral = 0.0
        self._last_error = 0.0
        self._last_time = None

    def update(self, error):
        """Feed a new error sample, return the new control output."""
        now = time.monotonic()
        if self._last_time is None:
            dt = 0.0
        else:
            dt = max(1e-6, now - self._last_time)
        self._last_time = now

        self._integral += error * dt
        derivative = (error - self._last_error) / dt if dt > 0 else 0.0
        self._last_error = error

        output = (self.kp * error
                  + self.ki * self._integral
                  + self.kd * derivative)

        if self.output_limit is not None:
            lo, hi = self.output_limit
            output = max(lo, min(hi, output))
        return output
