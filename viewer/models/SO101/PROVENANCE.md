# Official SO-101 model

Source: https://github.com/TheRobotStudio/SO-ARM100
Revision: a758567c3978dfeefe282ede0500085a48fe8f78
Directory: Simulation/SO101
Variant: so101_new_calib.urdf (follower, new calibration, no camera)

The URDF, referenced STL meshes, and upstream README are copied unchanged.
SHA256SUMS.json records their checksums. LICENSE is the upstream Apache-2.0
license. TheRobotStudio retains its attribution; see upstream README and URDF
CAD source comments. Only referenced mesh assets are included.

The viewer uses URDF joint angles in radians internally and displays degrees.
The gripper is a revolute joint here, not LeRobot's 0–100 open scale.
Model limits are not calibrated hardware limits or collision protection.
