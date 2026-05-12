"""Drive the PiCar-X with the keyboard. Inspired by SunFounder's video_car demo.

Keys:
    W / S      forward / backward
    A / D      steer left / right
    F          stop
    O / P      speed up / down
    T          take a photo
    Ctrl+C     quit
"""

from time import sleep

import readchar

from picarx_robot import Robot

HELP = __doc__


def _move(bot, action, speed):
    if action == "stop":
        bot.movement.stop()
    elif action == "forward":
        bot.movement.straighten()
        bot.movement.drive_forward(speed)
    elif action == "backward":
        bot.movement.straighten()
        bot.movement.drive_backward(speed)
    elif action == "left":
        bot.movement.turn_left(speed=speed, angle=30)
    elif action == "right":
        bot.movement.turn_right(speed=speed, angle=30)


def main():
    with Robot() as bot:
        bot.camera.start()
        sleep(2)
        print(HELP)

        speed, status = 0, "stop"

        while True:
            print(f"\rstatus: {status:<8} speed: {speed:<3}", end="", flush=True)
            key = readchar.readkey().lower()

            if key == "o" and speed <= 90:
                speed += 10
            elif key == "p" and speed >= 10:
                speed -= 10
                if speed == 0:
                    status = "stop"
            elif key in "wsad":
                if speed == 0:
                    speed = 10
                status = {"w": "forward", "s": "backward",
                          "a": "left", "d": "right"}[key]
            elif key == "f":
                status = "stop"
            elif key == "t":
                path = bot.camera.take_photo()
                print(f"\nSaved photo: {path}.jpg")
                continue
            elif key == readchar.key.CTRL_C:
                print("\nquitting...")
                break
            else:
                continue

            _move(bot, status, speed)
            sleep(0.05)


if __name__ == "__main__":
    main()
