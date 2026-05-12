"""Vision helpers: ROI cropping, lane-line detection, obstacle finding.

All functions take BGR frames (the format Vilib hands out) and return
plain Python tuples, so they are easy to unit-test on a laptop with
saved frames.
"""

import cv2
import numpy as np

from . import config


# --- ROI ------------------------------------------------------------------

def crop_roi(frame):
    """Return the configured region of interest from a full frame.

    The crop is driven by ROI_TOP / ROI_BOTTOM / ROI_LEFT / ROI_RIGHT
    in `config.py`, expressed as fractions (0.0 – 1.0). Default is the
    lower half of the image — useful for line following.
    """
    h, w = frame.shape[:2]
    y0 = int(h * config.ROI_TOP)
    y1 = int(h * config.ROI_BOTTOM)
    x0 = int(w * config.ROI_LEFT)
    x1 = int(w * config.ROI_RIGHT)
    return frame[y0:y1, x0:x1]


# --- Helpers --------------------------------------------------------------

def _hsv_mask(frame_bgr, lower, upper):
    """Return a binary mask of pixels in `frame_bgr` whose HSV value
    falls inside [lower, upper]."""
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, np.array(lower, dtype=np.uint8),
                            np.array(upper, dtype=np.uint8))


# --- Lane lines -----------------------------------------------------------

def detect_lane(roi_bgr):
    """Find the two white edge lines and the road centre.

    Strategy: take the bottom 25% of the ROI (closest to the car),
    threshold for white, and pick the leftmost and rightmost columns
    that contain white pixels. Their midpoint is the road centre.

    Returns
    -------
    (left_x, right_x, centre_x) in ROI pixel coordinates,
    or `None` if fewer than two lines are visible.
    """
    mask = _hsv_mask(roi_bgr,
                     config.WHITE_LINE_HSV_LOWER,
                     config.WHITE_LINE_HSV_UPPER)
    h, w = mask.shape
    band = mask[int(h * 0.75):, :]      # bottom strip is most reliable
    cols = np.where(np.any(band > 0, axis=0))[0]

    if cols.size < 2:
        return None

    left_x = int(cols.min())
    right_x = int(cols.max())

    # Reject if the two "lines" are too close — probably one fat line,
    # not two edges.
    if (right_x - left_x) < (w * 0.20):
        return None

    centre_x = (left_x + right_x) // 2
    return left_x, right_x, centre_x


# --- Obstacle detection ---------------------------------------------------

def detect_obstacle(roi_bgr):
    """Find the largest "thing that is neither road nor white line".

    Pipeline:
        1. Build a mask of road pixels + white-line pixels (the
           "background" we expect to see).
        2. Invert it — anything left is a foreign object.
        3. Open with a small kernel to drop speckle noise.
        4. Take the largest contour; reject if smaller than
           `OBSTACLE_MIN_AREA_PX`.
        5. Compute its centroid via image moments.

    Returns
    -------
    (centroid_x, centroid_y, area_px) in ROI pixel coordinates,
    or `None` if no obstacle is present.
    """
    line_mask = _hsv_mask(roi_bgr,
                          config.WHITE_LINE_HSV_LOWER,
                          config.WHITE_LINE_HSV_UPPER)
    road_mask = _hsv_mask(roi_bgr,
                          config.ROAD_HSV_LOWER,
                          config.ROAD_HSV_UPPER)
    background = cv2.bitwise_or(line_mask, road_mask)
    obstacle_mask = cv2.bitwise_not(background)

    kernel = np.ones((5, 5), np.uint8)
    obstacle_mask = cv2.morphologyEx(obstacle_mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(obstacle_mask,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    biggest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(biggest)
    if area < config.OBSTACLE_MIN_AREA_PX:
        return None

    M = cv2.moments(biggest)
    if M["m00"] == 0:
        return None
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return cx, cy, area
