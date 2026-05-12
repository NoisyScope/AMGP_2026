# Calibration scripts

These scripts are the **official SunFounder calibration tools**, copied
verbatim from the `sunfounder/picar-x` GitHub repo (`v2.0` branch,
`example/calibration/` and `example/servo_zeroing.py`). They are used
once after assembly — and again any time the wheels/camera look
visibly off-centre — to write trim values into the persistent
`/opt/picar-x/picar-x.conf` file.

## What each script does

| Script                     | Purpose                                                                                  |
|----------------------------|------------------------------------------------------------------------------------------|
| `servo_zeroing.py`         | Sends a 0° pulse to **every servo** so you can fit the arms in the neutral position.    |
| `calibration.py`           | Interactive trim for **steering, camera pan, camera tilt, and both drive motors**.       |
| `grayscale_calibration.py` | Interactive trim for the 3-channel grayscale (line / cliff) sensor underneath the car.  |

## Steering calibration — quick start

The official flow is:

1. Power on the PiCar-X with the wheels off the ground.
2. Run `servo_zeroing.py` first so all servos move to 0°. Detach the
   steering linkage / servo arms and re-fit them as straight as
   possible by hand. Then `Ctrl+C` to exit.
3. Run `calibration.py`:
   ```bash
   sudo python3 calibration/calibration.py
   ```
4. Press `1` to select the **direction (steering) servo**.
5. Press `A` / `D` to nudge the trim left / right until the front
   wheels point dead straight.
6. Press `R` to test (the script briefly drives the servo through its
   range so you can confirm it returns to centre).
7. Press `SPACE` to **save** the trim. The value is persisted via
   `px.dir_servo_calibrate(...)` and survives reboots.
8. (Optional) Repeat for `2` (camera pan), `3` (camera tilt), and
   `4` / `5` (motor direction) using the same workflow.
9. `Ctrl+C` to quit.

## Key picarx APIs the script uses

These are useful if you want to write your own calibration tools
later — they are exposed directly on the `Picarx` object:

- `px.dir_cali_val`, `px.cam_pan_cali_val`, `px.cam_tilt_cali_val` —
  the currently-stored servo trim offsets (degrees).
- `px.cali_dir_value` — list of motor direction calibration values
  (`[left, right]`, each `+1` or `-1`).
- `px.dir_servo_calibrate(value)` — write a new steering trim.
- `px.cam_pan_servo_calibrate(value)` / `px.cam_tilt_servo_calibrate(value)`
- `px.motor_direction_calibrate(motor, value)` — flip a motor that
  spins the wrong way (`motor` is `1` or `2`, `value` is `±1`).

## Source

- [`example/calibration/calibration.py`](https://github.com/sunfounder/picar-x/blob/v2.0/example/calibration/calibration.py)
- [`example/calibration/grayscale_calibration.py`](https://github.com/sunfounder/picar-x/blob/v2.0/example/calibration/grayscale_calibration.py)
- [`example/servo_zeroing.py`](https://github.com/sunfounder/picar-x/blob/v2.0/example/servo_zeroing.py)
- Tutorial: [Calibrating the PiCar-X](https://docs.sunfounder.com/projects/picar-x-v20/en/latest/python/python_calibrate.html)
