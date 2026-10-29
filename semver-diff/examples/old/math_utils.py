"""Version 1.4.2 - the 'safe' version."""


def add(a: int, b: int) -> int:
    return a + b


def round_half(value: float) -> float:
    """Python's built-in round: bankers rounding, 2.5 -> 2, 3.5 -> 4."""
    return round(value)


def handle_missing(values: list) -> list:
    """Keep the length: missing values become 0."""
    return [0 if v is None else v for v in values]
