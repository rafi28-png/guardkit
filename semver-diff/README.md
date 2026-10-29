# SemVer-Diff

**A patch release should not silently change what your code does. SemVer-Diff catches it before you publish.**

Many production outages happen because a library ships a "safe" patch (1.4.2 → 1.4.3) that compiles cleanly and passes basic tests, but changes behavior: a different rounding rule, a dropped value, a changed sort order.

SemVer-Diff compares two versions of the same Python functions side-by-side, bombards them with edge-case inputs, and tells you if the outputs differ — even if you have almost no tests.

## The demo (30 seconds)

This repo includes an example where version 1.4.3 looks safe, but isn't:

```bash
python -m semver_diff compare examples/old/math_utils.py examples/new/math_utils.py
```

Real output from this project:

```
Functions checked: 3
Cases checked: 88
Divergences: 4
Verdict: BEHAVIOR CHANGE DETECTED - this requires a MINOR or MAJOR bump, not a PATCH

Examples:
  - handle_missing([1, None, 2],): old=ok:[1, 0, 2]  new=ok:[1, 2]
  - handle_missing([None, None],): old=ok:[0, 0]  new=ok:[]
  - round_half(0.5,): old=ok:0  new=ok:1
  - round_half(2.5,): old=ok:2  new=ok:3
```

And comparing a file with itself correctly passes:

```
Divergences: 0
Verdict: No behavioral differences found - PATCH looks safe
```

## How it works

1. **Discovery (no tests needed):** It reads your code with Python's AST parser and finds all public functions and their type hints.
2. **Edge-case generation:** From those hints it builds boundary inputs — 0, -1, 2.5, empty lists, `None`, huge numbers, and more. Same inputs every run, so results are reproducible.
3. **Side-by-side comparison:** It loads the old and new versions separately, runs both on every input, and compares return values and exception types.
4. **Verdict:** Exit code `0` = safe to ship as a patch. Exit code `1` = behavioral change found, use MINOR or MAJOR instead. That exit code is what makes it work in CI.

## Use it in CI

See `.github/workflows/semver-diff.yml`. On every pull request it compares the PR branch against `main` and fails the check if behavior changed.

You can also compare two git refs directly:

```bash
python -m semver_diff compare --old-ref v1.4.2 --new-ref HEAD --file math_utils.py
```

## Scope of this MVP (honest limits)

- Python only, top-level functions only
- Best for pure functions (no network, files, or randomness inside the function)
- Compares values and exception *types*, not timing or memory yet
- That narrow scope is deliberate: it keeps false positives low, which is what makes maintainers trust it

## Run the tests

```bash
python -m pytest tests/ -q
# or without pytest:
python -m semver_diff compare examples/old/math_utils.py examples/new/math_utils.py
```

## Project layout

```
semver_diff/
  discovery.py  # AST: find public functions + type hints
  inputs.py     # Boundary inputs from type hints
  runner.py     # Load old/new safely, run one function
  differ.py     # Compare outputs, build the verdict
  cli.py        # Command-line interface
examples/
  old/math_utils.py  # v1.4.2
  new/math_utils.py  # v1.4.3, the "safe" patch that isn't
tests/
  test_differ.py
```

## License

MIT
