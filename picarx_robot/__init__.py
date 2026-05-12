"""PiCar-X Robot package.

A small modular wrapper around SunFounder's `picarx` and `vilib` libraries.

Typical usage:

    from picarx_robot import Robot

    bot = Robot()
    bot.movement.forward(speed=30)
    bot.camera.start()
    bot.camera.take_photo("hello")
    bot.shutdown()
"""

from .robot import Robot

__all__ = ["Robot"]
__version__ = "0.1.0"
