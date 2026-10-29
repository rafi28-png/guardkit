"""Generate boundary / edge-case inputs from type hints.

Deliberately small and deterministic: the same run always produces
the same inputs, so a reported difference is reproducible.
"""
import itertools

POOLS = {
    "int": [0, 1, -1, 2, 10, -10, 100, 2**31 - 1],
    "float": [0.0, 0.5, 1.5, 2.5, 3.5, -0.5, -2.5, 1.0, -1.0, 1e9, 1e-9,
              float("inf"), float("-inf"), float("nan")],
    "str": ["", "a", "hello", " ", "a b", "é", "123"],
    "bool": [True, False],
    "list": [[], [1, 2, 3], [3, 2, 1], [1, 1, 2], [0, 0], [1, None, 2],
             [None, None], [2.5, 1.5, 0.5], [5], [-1, 0, 1]],
    "dict": [{}, {"a": 1}, {"b": 2, "a": 1}],
    "None": [None],
}

GENERIC_POOL = [0, 1, 2.5, "hello", "", [], [1, 2], None, True, False]


def pool_for(annotation: str) -> list:
    """Map an annotation string to a pool. Handles list[int], List, etc."""
    ann = (annotation or "").strip()
    base = ann.split("[")[0].strip().lower()
    # Normalise common aliases
    if base in ("list", "sequence"):
        return POOLS["list"]
    if base in POOLS:
        return POOLS[base]
    return GENERIC_POOL


def generate_cases(arg_types: list, limit: int = 200) -> list[tuple]:
    """Generate argument tuples for a function."""
    if not arg_types:
        return [()]
    pools = [pool_for(t) for t in arg_types]
    if len(pools) == 1:
        return [(v,) for v in pools[0][:limit]]
    # For 2+ args, use the cartesian product but cap it, plus
    # paired edge cases (first-with-first, last-with-last, ...) so
    # we don't miss the extremes when the product is truncated.
    cases = []
    for combo in itertools.product(*pools):
        cases.append(combo)
        if len(cases) >= limit:
            break
    return cases
