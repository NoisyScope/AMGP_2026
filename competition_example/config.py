"""Tunable constants for the competition run.

Everything you might want to tweak on the day of the competition lives
here. The vision values are HSV (OpenCV's `cv2.cvtColor(..., COLOR_BGR2HSV)`):
    H: 0–179, S: 0–255, V: 0–255.
"""

# --- Colour ranges (HSV) -------------------------------------------------
# White edge-line colour. White has any hue, very low saturation, very
# high value. Tighten on the actual track lighting.
WHITE_LINE_HSV_LOWER = (0, 0, 200)
WHITE_LINE_HSV_UPPER = (180, 40, 255)

# Road surface colour. The track in the SunFounder competition kit is a
# medium grey; widen / narrow this on the day with sample frames.
ROAD_HSV_LOWER = (0, 0, 50)
ROAD_HSV_UPPER = (180, 60, 200)

# --- Region of interest --------------------------------------------------
# Fractions (0.0 – 1.0) of the full camera frame that we will analyse.
# Default = lower half: vision should look at the road in front of the
# car, not at the horizon.
ROI_TOP    = 0.50
ROI_BOTTOM = 1.00
ROI_LEFT   = 0.00
ROI_RIGHT  = 1.00

# --- PID gains -----------------------------------------------------------
# Error = (lane_centre_x - frame_centre_x) in pixels, output = steering
# degrees. Start with KP, add KD if the car oscillates, KI almost never
# needed for lane keeping.
PID_KP = 0.05
PID_KI = 0.0
PID_KD = 0.02

# --- Drive parameters ----------------------------------------------------
DRIVE_SPEED        = 25   # 0–100, picarx units
MAX_STEERING_ANGLE = 30   # degrees, capped well below the ±35 servo limit

# --- Sensor thresholds ---------------------------------------------------
# Above this grayscale reading = the sensor is over a white edge line.
# Calibrate using calibration/grayscale_calibration.py.
GRAYSCALE_LINE_THRESHOLD = 600

# Distance below which the ultrasonic sensor flags an obstacle (cm).
OBSTACLE_DISTANCE_CM = 25

# Minimum contour area (px^2) to count as a real obstacle, not noise.
OBSTACLE_MIN_AREA_PX = 500

# Main loop period (seconds).
LOOP_PERIOD_S = 0.05
