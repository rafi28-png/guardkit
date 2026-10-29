"""Load a module from a file path and run one function safely.

Each version gets a unique module name, so old and new can be loaded
side-by-side in the same process without clashing.
"""
import importlib.util
import sys


def load_module(path: str, label: str):
    spec = importlib.util.spec_from_file_location(f"semver_diff_{label}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_one(module, func_name: str, args: tuple):
    """Run func(*args). Return ('ok', repr) or ('error', 'Type: message')."""
    func = getattr(module, func_name, None)
    if func is None:
        return ("error", "MissingFunction")
    try:
        result = func(*args)
        # repr() is stable for ints, floats (incl. nan -> 'nan'),
        # strings, lists and dicts, which is all this MVP compares.
        return ("ok", repr(result))
    except Exception as exc:  # noqa: BLE001 - we want to record any divergence
        return ("error", f"{type(exc).__name__}: {exc}")
