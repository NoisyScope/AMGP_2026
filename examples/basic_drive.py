"""Drive forward, wiggle the steering, and stop.

Run on the Pi with:
    python3 examples/basic_drive.py
"""

from time import sleep

from picarx_robot import Robot


def main():
    with Robot() as bot:
        bot.movement.drive_forward(speed=30)
        sleep(0.5)

        # Sweep the steering left, right, then centre.
        for angle in (-30, 0, 30, 0):
            bot.movement.turn(angle)
            sleep(0.4)

        bot.movement.stop()


if __name__ == "__main__":
    main()
