# SO-101 hand control

We are building a hand-controlled SO-101 robot arm. The planned pipeline is:

**hand sensing → coordinate mapping → inverse kinematics (IK) → motor control**

Leap Motion will eventually supply hand position and pinch detection. Mapping will
convert a hand position into a robot target, IK will calculate joint angles, and
motor control will move the arm. The eventual intent is for pinching to close the
gripper. There is no webcam work or reinforcement learning in this project.

## First milestone: example hand input

This version only prints five example samples and exits. It shows labeled x/y/z
positions in millimeters, OPEN and PINCHED gestures, a MISSING hand with UNKNOWN
gesture, and recovered tracking. These are made-up input positions, not calibrated
robot targets. Axis conventions and tracking integration still need to be defined.
No Leap SDK, IK, gripper control, or motor connection is implemented.

## Setup and exact run commands

On the development Mac, `python3 --version` reports Python 3.9.6. That is sufficient
for this standard-library-only demo. No packages, virtual environment, or hardware
are required for this milestone; the M5 MacBook Air can run it directly. Future
Leap SDK compatibility with macOS, Apple Silicon, and Python must be verified when
we choose the integration; this demo does not establish hardware compatibility.

In Terminal:

```sh
cd ~/Documents/so101-hand-control
python3 --version
python3 main.py
python3 -m unittest -v
```

If you cloned into another folder, change the `cd` path accordingly. No `pip install`
step is needed. A virtual environment can be added when dependencies are introduced.

Example output includes:

```text
Sample 3: Hand: TRACKED | Position (mm): x=30.0, y=220.0, z=-10.0 | Gesture: PINCHED
Sample 4: Hand: MISSING | Position: unavailable | Gesture: UNKNOWN
Sample 5: Hand: TRACKED | Position (mm): x=-20.0, y=180.0, z=15.0 | Gesture: OPEN
```

## Files and how the code works

- `hand_input.py`: `HandSample` holds one position and a pinch boolean (`True` means
  pinched). `example_samples()` yields samples one at a time. `None` means no hand
  is tracked, so it carries no stale position or assumed open/pinched state.
- `main.py`: `format_sample()` turns a sample into labeled text. `run()` accepts an
  iterable of samples and prints them. Later, a separate Leap input adapter can
  supply the same sample type without mixing sensing into mapping or motor code.
- `test_demo.py`: checks coordinate labels, both gestures, missing tracking, and
  recovery. These are software display checks, not robot safety tests.
- `.gitignore`: excludes Python environments, caches, common credential files,
  editor settings, and the `personal/` and `local_data/` folders. It is not a secret
  scanner; review staged files before committing.
- `README.md`: setup, explanation, scope, and next milestones.

## One small edit to try

In `hand_input.py`, change the first sample's `x_mm=0.0` to `x_mm=50.0`.
Run `python3 main.py` again. Sample 1 should now show `x=50.0`.

## Next milestones (not implemented)

1. Connect Leap input after verifying the supported SDK and platform setup. Keep
   example input available. Define axes, units, pinch detection, and missing tracking.
2. Add and test coordinate mapping separately, using example input and printed
   targets before attempting movement.
3. Add and test IK separately using verified arm geometry and joint conventions,
   including unreachable targets, with no motor commands.
4. Before physical operation, implement and test explicit stop/enable controls,
   movement and speed limits, and safe handling of missing or stale tracking. Verify
   the actual hardware specifications and limits; none are assumed here. Printing
   MISSING in this demo is not a safety stop.
5. Only after those prerequisites, integrate motor control and gripper behavior
   using verified wiring, calibration, and hardware documentation.

For collaboration, review changes before committing and coordinate with each other
before pushing. This milestone is intended as a local commit only.
