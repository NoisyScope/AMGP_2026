"""Camera module — point the camera and grab images.

The PiCar-X has two camera servos:
    * pan  (`set_camera_servo1_angle`) — left / right
    * tilt (`set_camera_servo2_angle`) — up / down

Image capture is delegated to SunFounder's `vilib` library, which also
provides an MJPEG web stream at `http://<pi-ip>:9000/mjpg` once started.

Extending this module:
    `vilib` exposes built-in detectors (faces, colours, traffic signs).
    Add new methods here that call e.g. `Vilib.face_detect_switch(True)`
    rather than scattering vilib calls across the codebase.
"""

import os
from time import localtime, strftime, time as now

from .config import (
    MAX_CAMERA_ANGLE,
    MIN_CAMERA_ANGLE,
    PHOTO_SUBDIR,
)


def _clamp(value, lo, hi):
    return max(lo, min(hi, value))


def _default_photo_dir():
    """Return the path where photos are saved, e.g. /home/pi/Pictures/picar-x/."""
    home = os.path.expanduser("~")
    return os.path.join(home, PHOTO_SUBDIR) + os.sep


class Camera:
    """Camera control + still image capture.

    Parameters
    ----------
    px : picarx.Picarx
        Hardware handle (used for the two camera servos).
    vilib : module, optional
        The `vilib.Vilib` class. Passed in for testability so a fake
        can be substituted in unit tests.
    """

    def __init__(self, px, vilib=None):
        self._px = px

        if vilib is None:
            # Imported lazily so the rest of the package can be imported
            # on a development laptop without vilib being installed.
            from vilib import Vilib  # type: ignore
            vilib = Vilib
        self._vilib = vilib

        self._running = False

    # -- Streaming lifecycle ----------------------------------------------

    def start(self, vflip=False, hflip=False, local_display=True, web_stream=True):
        """Power on the camera and start the video stream.

        `vflip` / `hflip` flip the picture vertically / horizontally —
        useful if you mounted the camera upside down.

        `local_display` shows a window on the Pi's HDMI output;
        `web_stream` exposes an MJPEG stream on port 9000.
        """
        self._vilib.camera_start(vflip=vflip, hflip=hflip)
        self._vilib.display(local=local_display, web=web_stream)
        self._running = True

    def stop(self):
        """Stop the camera and release the hardware."""
        if self._running:
            self._vilib.camera_close()
            self._running = False

    # -- Servos ------------------------------------------------------------

    def pan(self, angle):
        """Rotate the camera left / right.

        `angle` is in degrees. 0 is straight ahead, negative looks left,
        positive looks right. Limited to roughly -35° to +35°.
        """
        angle = _clamp(angle, MIN_CAMERA_ANGLE, MAX_CAMERA_ANGLE)
        self._px.set_camera_servo1_angle(angle)

    def tilt(self, angle):
        """Tilt the camera up / down.

        `angle` is in degrees. 0 is level, negative looks down, positive
        looks up. Limited to roughly -35° to +35°.
        """
        angle = _clamp(angle, MIN_CAMERA_ANGLE, MAX_CAMERA_ANGLE)
        self._px.set_camera_servo2_angle(angle)

    def look(self, pan_angle=0, tilt_angle=0):
        """Convenience: set pan and tilt in one call."""
        self.pan(pan_angle)
        self.tilt(tilt_angle)

    # -- Image capture -----------------------------------------------------

    def get_frame(self):
        """Return the current camera frame as a BGR numpy array.

        Vilib continuously refreshes `Vilib.img` after `start()` is
        called, so this is essentially the latest frame. Returns
        `None` if no frame has been captured yet.
        """
        if not self._running:
            raise RuntimeError(
                "Camera is not running. Call start() before get_frame()."
            )
        return getattr(self._vilib, "img", None)

    def take_photo(self, name=None, path=None):
        """Save a JPEG snapshot from the camera.

        If `name` is omitted, a timestamped filename is generated
        (e.g. `photo_2026-05-07-13-22-09`). If `path` is omitted, the
        image is saved to `~/Pictures/picar-x/`.

        Returns the full path (without extension — vilib appends .jpg).
        """
        if not self._running:
            raise RuntimeError(
                "Camera is not running. Call start() before take_photo()."
            )

        if name is None:
            name = "photo_" + strftime("%Y-%m-%d-%H-%M-%S", localtime(now()))
        if path is None:
            path = _default_photo_dir()

        os.makedirs(path, exist_ok=True)
        self._vilib.take_photo(name, path)
        return os.path.join(path, name)
