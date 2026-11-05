"""Checks for display states, including losing and recovering tracking."""

import io
import unittest
from contextlib import redirect_stdout

from hand_input import HandSample, example_samples
from main import format_sample, run


class DemoTests(unittest.TestCase):
    def test_coordinates_and_gestures_are_labeled(self):
        for pinched, label in [(False, "OPEN"), (True, "PINCHED")]:
            with self.subTest(pinched=pinched):
                line = format_sample(HandSample(1.0, -2.0, 3.0, pinched))
                self.assertIn("Position (mm): x=1.0, y=-2.0, z=3.0", line)
                self.assertIn(f"Gesture: {label}", line)

    def test_missing_hand_has_no_position_or_assumed_gesture(self):
        line = format_sample(None)
        self.assertIn("Hand: MISSING", line)
        self.assertIn("Position: unavailable", line)
        self.assertIn("Gesture: UNKNOWN", line)
        self.assertNotIn("x=", line)

    def test_example_sequence_recovers_after_missing_tracking(self):
        output = io.StringIO()
        with redirect_stdout(output):
            run(example_samples())
        lines = output.getvalue().splitlines()
        self.assertEqual(len(lines), 6)
        self.assertIn("EXAMPLE DATA ONLY", lines[0])
        self.assertIn("Gesture: PINCHED", lines[3])
        self.assertIn("Hand: MISSING", lines[4])
        self.assertNotIn("x=", lines[4])
        self.assertIn("Hand: TRACKED", lines[5])
        self.assertIn("Gesture: OPEN", lines[5])


if __name__ == "__main__":
    unittest.main()
