# PiCar-X Robot Template

A small, modular Python codebase for the [SunFounder PiCar-X v2.0](https://docs.sunfounder.com/projects/picar-x-v20/en/latest/).
Wraps SunFounder's `picarx` and `vilib` libraries behind clean, easy-to-extend modules.

## Project layout

```
ClubDR/
├── README.md
├── requirements.txt
├── picarx_robot/            # The library — import this from your code
│   ├── __init__.py
│   ├── robot.py             # Top-level Robot facade (use this!)
│   ├── movement.py          # forward / backward / turn / stop
│   ├── camera.py            # pan / tilt / start stream / take photo
│   ├── sensors.py           # ultrasonic + grayscale line sensors
│   └── config.py            # speed and angle limits in one place
└── examples/                # Runnable demo scripts
    ├── basic_drive.py
    ├── take_photo.py
    └── keyboard_control.py
```

This layout follows the standard "src package + examples" pattern
common in Python robotics projects — the SunFounder docs do not
prescribe a specific layout, so we use a conventional one.

## Quick start

On the Raspberry Pi (with the PiCar-X assembled and the SunFounder OS
image flashed):

```bash
# 1. Make sure the SunFounder libraries are present (they ship with the image).
sudo apt update && sudo apt install -y python3-picarx python3-vilib

# 2. Run a demo from the project root.
cd ~/ClubDR
python3 examples/basic_drive.py
```

## Using the library in your own code

```python
from picarx_robot import Robot

with Robot() as bot:
    bot.movement.drive_forward(speed=40)
    bot.movement.turn(-20)        # steer left

    bot.camera.start()
    bot.camera.look(pan_angle=15, tilt_angle=-10)
    bot.camera.take_photo("test")

    print("distance:", bot.sensors.distance_cm(), "cm")
```

The `with` block guarantees the motors stop and the camera releases
even if your code throws.

## Adding new behaviours

The codebase is organised so new features slot in cleanly:

| You want to...                                | Add to...           |
|-----------------------------------------------|---------------------|
| A new motion (spin, arc, dance)               | `movement.py`       |
| A new vision feature (face detect, line cam)  | `camera.py`         |
| A new sensor read or filter                   | `sensors.py`        |
| A new high-level behaviour (patrol, follow)   | a new module + wire it into `Robot` in `robot.py` |
| A tuning value (max speed, default angle)     | `config.py`         |

## Reference

- [PiCar-X v2.0 docs](https://docs.sunfounder.com/projects/picar-x-v20/en/latest/)
- [Movement tutorial](https://docs.sunfounder.com/projects/picar-x-v20/en/latest/python/python_move.html)
- [Video Car / Vilib tutorial](https://docs.sunfounder.com/projects/picar-x-v20/en/latest/python/python_video_car.html)
