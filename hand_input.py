"""Example hand input. A future Leap adapter can emit the same sample type."""

from dataclasses import dataclass
from typing import Iterator, Optional


@dataclass(frozen=True)
class HandSample:
    """Demo position in millimeters and a pinch state; not robot coordinates."""

    x_mm: float
    y_mm: float
    z_mm: float
    pinched: bool


def example_samples() -> Iterator[Optional[HandSample]]:
    """Yield open, pinched, missing, then recovered tracking. None means missing."""
    yield HandSample(x_mm=0.0, y_mm=200.0, z_mm=0.0, pinched=False)
    yield HandSample(x_mm=30.0, y_mm=220.0, z_mm=-10.0, pinched=False)
    yield HandSample(x_mm=30.0, y_mm=220.0, z_mm=-10.0, pinched=True)
    yield None
    yield HandSample(x_mm=-20.0, y_mm=180.0, z_mm=15.0, pinched=False)
