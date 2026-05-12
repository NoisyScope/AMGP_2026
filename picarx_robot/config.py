"""Configuration constants for the PiCar-X robot.

Centralising these values means future code does not have to hard-code
limits — change the value here once and every module picks it up.
"""

# --- Motor speed limits ---------------------------------------------------
# The picarx library accepts speed values from 0 to 100.
MIN_SPEED = 0
MAX_SPEED = 100

# A safer "default" speed used when the user does not specify one.
DEFAULT_SPEED = 30

# --- Servo angle limits ---------------------------------------------------
# Steering and the two camera servos (pan / tilt) all share the same
# mechanical range on the PiCar-X: roughly -35 to +35 degrees.
MIN_STEERING_ANGLE = -35
MAX_STEERING_ANGLE = 35

MIN_CAMERA_ANGLE = -35
MAX_CAMERA_ANGLE = 35

# --- File paths -----------------------------------------------------------
# Default folder where photos are saved. Resolved relative to the current
# user's home directory at runtime.
PHOTO_SUBDIR = "Pictures/picar-x"
