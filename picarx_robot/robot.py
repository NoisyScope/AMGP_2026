"""Top-level Robot facade.

The `Robot` class is the single object the rest of your application
should talk to. It owns one `Picarx` hardware handle and exposes the
movement, camera, and sensor sub-modules as attributes:

    bot = Robot()
    bot.movement.drive_forward(30)
    bot.camera.take_photo()
    print(bot.sensors.distance_cm())
    bot.shutdown()

Using a context manager guarantees the motors stop and the camera is
released even if your code crashes:

    with Robot() as bot:
        bot.movement.drive_forward(30)
        ...
"""

from .camera import Camera
from .movement import Movement
from .sensors import Sensors


class Robot:
    """Composite robot object — movement + camera + sensors.

    Parameters
    ----------
    reset_hardware : bool, default True
        If True, calls `picarx.utils.reset_mcu()` before initialising
        the Picarx. The SunFounder examples do this to clear any stale
        state from a previous run; harmless to keep on.
    """

    def __init__(self, reset_hardware=True):
        # Imported lazily so this package can be imported on a dev
        # machine that does not have the SunFounder libraries installed.
        from picarx import Picarx  # type: ignore

        if reset_hardware:
            try:
                from picarx.utils import reset_mcu  # type: ignore
                reset_mcu()
            except ImportError:
                # Older picarx versions do not ship reset_mcu — ignore.
                pass

        self._px = Picarx()

        self.movement = Movement(self._px)
        self.camera = Camera(self._px)
        self.sensors = Sensors(self._px)

    # -- Lifecycle ---------------------------------------------------------

    def shutdown(self):
        """Stop the motors and release the camera. Safe to call twice."""
        try:
            self.movement.stop()
        finally:
            self.camera.stop()

    # -- Context manager support ------------------------------------------

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
        return False  # do not swallow exceptions
