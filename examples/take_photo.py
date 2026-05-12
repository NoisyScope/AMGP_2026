"""Start the camera, wait for it to warm up, save a photo, then stop.

The MJPEG stream is also available at http://<pi-ip>:9000/mjpg while
this script is running.
"""

from time import sleep

from picarx_robot import Robot


def main():
    with Robot() as bot:
        bot.camera.start(local_display=False, web_stream=True)
        sleep(2)  # Let the auto-exposure settle.

        path = bot.camera.take_photo()
        print(f"Saved photo to: {path}.jpg")


if __name__ == "__main__":
    main()
