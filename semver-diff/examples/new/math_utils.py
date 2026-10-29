"""Version 1.4.3 - released as a 'safe patch', but it is not.

Both changes below compile cleanly and pass a basic smoke test,
yet they silently change outputs for downstream users.
"""
import math


def add(a: int, b: int) -> int:
    return a + b


def round_half(value: float) -> float:
    """Changed to round-half-up: 2.5 -> 3. This breaks 2.5, -2.5, etc."""
    return math.floor(value + 0.5)


def handle_missing(values: list) -> list:
    """Changed to drop missing values instead of replacing them with 0.
    The output list is now shorter, which breaks code that zips it
    with the original input."""
    return [v for v in values if v is not None]
