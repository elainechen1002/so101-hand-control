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

## Second milestone: local SO-101 joint viewer

Open this project folder in VS Code: `/Users/elainechen/Documents/so101-hand-control`.
The browser viewer loads the actual official SO-101 follower model, with six joint
sliders (including the gripper). Drag the scene to orbit, scroll to zoom, and
right-drag to pan. Each slider supports arrow keys (1 degree), Page Up/Down
(10 degrees), and Home/End (model endpoints). Reset buttons restore zero angles
or the initial viewing direction. Zero is the model's virtual calibration, not a
command to home physical hardware.

One-time dependency setup (Node.js/npm and internet required; Node 26.8.1 and
npm 11.19.0 are installed on this Mac):

```sh
cd ~/Documents/so101-hand-control
npm --prefix viewer ci
```

Launch using Python, with no additional Python packages:

```sh
cd ~/Documents/so101-hand-control
python3 viewer.py
```

Open **http://127.0.0.1:8000** in a modern browser with WebGL enabled. Keep the
Terminal command running; press Ctrl+C to stop. If port 8000 is busy, use
`python3 viewer.py --port 8001` and open http://127.0.0.1:8001 instead.
Do not open the HTML file directly. Once dependencies are installed, all viewer
scripts and models load locally; no CDN or network connection is needed.

### Added files

- `viewer.py`: serves only the viewer folder, bound to this computer's loopback
  address. It neither imports hand input nor opens hardware connections.
- `viewer/index.html` and `viewer/style.css`: the page, labels, and responsive layout.
- `viewer/app.js`: loads the URDF with `urdf-loader`, draws it with Three.js, and
  converts degree slider values to radians. Joint relationships and mesh placement
  come from the URDF; there is no IK solver. Rendering occurs only on changes.
- `viewer/package.json` and `viewer/package-lock.json`: pinned browser dependencies;
  `npm ci` installs them into the ignored `viewer/node_modules/` directory.
- `viewer/models/SO101/`: unchanged official URDF and referenced STL meshes, upstream
  README/license, source revision in `PROVENANCE.md`, and asset checksums.
- `test_viewer.py`: verifies model integrity, six joint limits, and local mesh paths.

Source: [TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100/tree/a758567c3978dfeefe282ede0500085a48fe8f78/Simulation/SO101),
revision `a758567c3978dfeefe282ede0500085a48fe8f78`, Apache-2.0.
The selected file is `so101_new_calib.urdf`, the follower model without a camera.
The upstream gripper is angular; its slider is not an open percentage. Model joint
limits constrain the viewer only. There is no collision checking or physics, and
these limits are not verified safe ranges for your physical arm.

Run checks with `python3 -m unittest -v`. The original `python3 main.py` demo is
unchanged. Try moving just Shoulder pan, then use Reset all joints to zero.

After this viewer works, the next milestone is a mouse-controlled target, followed
by IK. Keep sensing → mapping → IK → motor control separate. No camera, Leap,
motor connection, stop/enable controls, or physical safety system is implemented
here; those safety prerequisites remain required before physical operation.
