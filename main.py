"""Print example hand data. No robot commands are sent."""

from typing import Iterable, Optional

from hand_input import HandSample, example_samples


def format_sample(sample: Optional[HandSample]) -> str:
    if sample is None:
        return "Hand: MISSING | Position: unavailable | Gesture: UNKNOWN"

    gesture = "PINCHED" if sample.pinched else "OPEN"
    return (
        f"Hand: TRACKED | Position (mm): x={sample.x_mm:.1f}, "
        f"y={sample.y_mm:.1f}, z={sample.z_mm:.1f} | Gesture: {gesture}"
    )


def run(samples: Iterable[Optional[HandSample]]) -> None:
    print("SO-101 hand-input demo — EXAMPLE DATA ONLY; no motors connected")
    for number, sample in enumerate(samples, start=1):
        print(f"Sample {number}: {format_sample(sample)}")


if __name__ == "__main__":
    run(example_samples())
