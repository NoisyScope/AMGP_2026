"""Competition main loop.

Behaviour, in priority order on every cycle:

    1. Grayscale safety override — if either edge sensor sees the
       white line, do a hard turn away from it. Highest priority
       because it means we are about to leave the road.
    2. Obstacle avoidance — if the ultrasonic flags something
       close, find the obstacle in the camera, compare how much
       free road exists on each side, and steer toward the
       roomier side.
    3. PID lane keeping — find the two lines in the camera,
       compute the road centre, and let the PID nudge the
       steering so the car stays in the middle.

Run from the project root with:
    python3 -m competition_example.main
"""

from time import sleep

from picarx_robot import Robot

from . import config
from .pid import PID
from .vision import crop_roi, detect_lane, detect_obstacle


def _grayscale_edges(values):
    """Return (left_on_line, right_on_line).

    `values` is a 3-element list `[left, middle, right]` from the
    PiCar-X grayscale module. White line ⇒ high reading, so a value
    above the threshold means that sensor is sitting on the edge.
    """
    threshold = config.GRAYSCALE_LINE_THRESHOLD
    left = values[0] > threshold
    right = values[2] > threshold
    return left, right


def _avoid_obstacle(bot, roi):
    """Check for an obstacle and steer toward the side with more space.

    Returns True if it took control of steering this cycle, False if
    the lane keeper should run instead.
    """
    obstacle = detect_obstacle(roi)
    lane = detect_lane(roi)
    if obstacle is None or lane is None:
        return False

    obs_cx, _, _ = obstacle
    left_x, right_x, _ = lane

    space_left = obs_cx - left_x        # px between obstacle and left line
    space_right = right_x - obs_cx      # px between obstacle and right line

    # Steer toward whichever side has more clearance.
    if space_right >= space_left:
        bot.movement.turn(config.MAX_STEERING_ANGLE)
    else:
        bot.movement.turn(-config.MAX_STEERING_ANGLE)
    bot.movement.drive_forward(config.DRIVE_SPEED)
    return True


def _lane_keep(bot, roi, pid):
    """PID lane keeping. Returns True if lines were found, False otherwise."""
    lane = detect_lane(roi)
    if lane is None:
        return False

    _, _, lane_cx = lane
    roi_centre_x = roi.shape[1] // 2

    # Positive error = road centre is to the right of frame centre
    # ⇒ steer right (positive angle).
    error = lane_cx - roi_centre_x
    steering = pid.update(error)
    bot.movement.turn(steering)
    bot.movement.drive_forward(config.DRIVE_SPEED)
    return True


def main():
    pid = PID(
        kp=config.PID_KP,
        ki=config.PID_KI,
        kd=config.PID_KD,
        output_limit=(-config.MAX_STEERING_ANGLE, config.MAX_STEERING_ANGLE),
    )

    with Robot() as bot:
        bot.camera.start(local_display=False, web_stream=True)
        sleep(2)  # auto-exposure + first frame

        while True:
            # ---------- 1. Grayscale safety override ------------------
            try:
                left_on, right_on = _grayscale_edges(bot.sensors.grayscale())
            except Exception:
                left_on = right_on = False

            if left_on:
                # Edge sensor sees the left line ⇒ steer right.
                bot.movement.turn(config.MAX_STEERING_ANGLE)
                bot.movement.drive_forward(config.DRIVE_SPEED)
                pid.reset()
                sleep(config.LOOP_PERIOD_S)
                continue
            if right_on:
                bot.movement.turn(-config.MAX_STEERING_ANGLE)
                bot.movement.drive_forward(config.DRIVE_SPEED)
                pid.reset()
                sleep(config.LOOP_PERIOD_S)
                continue

            # ---------- Grab a frame for the vision branches ----------
            frame = bot.camera.get_frame()
            if frame is None:
                sleep(config.LOOP_PERIOD_S)
                continue
            roi = crop_roi(frame)

            # ---------- 2. Ultrasonic obstacle avoidance --------------
            distance = bot.sensors.distance_cm()
            if 0 < distance < config.OBSTACLE_DISTANCE_CM:
                if _avoid_obstacle(bot, roi):
                    pid.reset()
                    sleep(config.LOOP_PERIOD_S)
                    continue

            # ---------- 3. Default: PID lane keeping ------------------
            if not _lane_keep(bot, roi, pid):
                # No lines visible ⇒ creep straight at half speed
                # rather than running blind at full speed.
                bot.movement.straighten()
                bot.movement.drive_forward(config.DRIVE_SPEED // 2)
                pid.reset()

            sleep(config.LOOP_PERIOD_S)


if __name__ == "__main__":
    main()
