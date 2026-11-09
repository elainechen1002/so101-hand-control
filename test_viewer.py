"""Check the vendored official model without additional packages."""
import hashlib
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

MODEL = Path(__file__).resolve().parent / "viewer/models/SO101"


class ModelTests(unittest.TestCase):
    def test_official_files_are_unchanged(self):
        manifest = json.loads((MODEL / "SHA256SUMS.json").read_text())
        for name, expected in manifest.items():
            with self.subTest(file=name):
                self.assertEqual(hashlib.sha256((MODEL / name).read_bytes()).hexdigest(), expected)

    def test_six_movable_joints_have_limits_containing_zero(self):
        robot = ET.parse(MODEL / "so101_new_calib.urdf").getroot()
        joints = [j for j in robot.findall("joint") if j.attrib["type"] != "fixed"]
        self.assertEqual({j.attrib["name"] for j in joints}, {
            "shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"})
        for joint in joints:
            self.assertEqual(joint.attrib["type"], "revolute")
            limit = joint.find("limit")
            self.assertLess(float(limit.attrib["lower"]), 0)
            self.assertGreater(float(limit.attrib["upper"]), 0)

    def test_every_mesh_is_local_and_present(self):
        for mesh in ET.parse(MODEL / "so101_new_calib.urdf").iter("mesh"):
            path = (MODEL / mesh.attrib["filename"]).resolve()
            self.assertIn(MODEL.resolve(), path.parents)
            self.assertTrue(path.is_file())


if __name__ == "__main__":
    unittest.main()
