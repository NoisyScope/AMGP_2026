"""Sensors module — placeholder for ultrasonic + grayscale line sensors.

The PiCar-X ships with:
    * an HC-SR04 ultrasonic distance sensor on the front bumper
    * a 3-channel grayscale module underneath (line / cliff detection)

Both are exposed through the same `Picarx` object used elsewhere, so
this module is intentionally thin — it just gives them readable names.

Extending this module:
    Add filtering (e.g. moving average for ultrasonic readings) or
    higher-level helpers like `is_line_detected()` here.
"""


class Sensors:
    """Read distance and grayscale (line) sensors.

    Parameters
    ----------
    px : picarx.Picarx
        Hardware handle.
    """

    def __init__(self, px):
        self._px = px

    def distance_cm(self):
        """Return the distance to the nearest obstacle in centimetres.

        The PiCar-X ultrasonic sensor returns a negative number when
        nothing is in range — callers should treat values <= 0 as
        "no reading".
        """
        return self._px.get_distance()

    def grayscale(self):
        """Return the three grayscale channel readings as a list.

        Higher values = lighter surface, lower values = darker surface.
        Useful for line-following or detecting the edge of a table.
        """
        return self._px.get_grayscale_data()
