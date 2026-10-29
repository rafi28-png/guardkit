"""Compare two versions of the same functions, case by case."""
from dataclasses import dataclass

from .discovery import discover_functions
from .inputs import generate_cases
from .runner import load_module, run_one


@dataclass
class Divergence:
    function: str
    args: tuple
    old: str
    new: str

    def describe(self) -> str:
        return f"{self.function}{self.args!r}: old={self.old}  new={self.new}"


@dataclass
class Report:
    functions_checked: int
    cases_checked: int
    divergences: list

    @property
    def verdict(self) -> str:
        if self.divergences:
            return ("BEHAVIOR CHANGE DETECTED - "
                    "this requires a MINOR or MAJOR bump, not a PATCH")
        return "No behavioral differences found - PATCH looks safe"

    def summary(self) -> str:
        lines = [
            f"Functions checked: {self.functions_checked}",
            f"Cases checked: {self.cases_checked}",
            f"Divergences: {len(self.divergences)}",
            f"Verdict: {self.verdict}",
            "",
        ]
        if self.divergences:
            lines.append("Examples:")
            for d in self.divergences[:5]:
                lines.append(f"  - {d.describe()}")
            if len(self.divergences) > 5:
                lines.append(f"  ... and {len(self.divergences) - 5} more")
        return "\n".join(lines)


def compare_files(old_path: str, new_path: str, limit_per_function: int = 200) -> Report:
    old_funcs = {f.name: f for f in discover_functions(old_path)}
    new_funcs = {f.name: f for f in discover_functions(new_path)}
    common = sorted(set(old_funcs) & set(new_funcs))

    old_mod = load_module(old_path, "old")
    new_mod = load_module(new_path, "new")

    divergences = []
    cases_checked = 0
    for name in common:
        info = old_funcs[name]
        for args in generate_cases(info.arg_types, limit=limit_per_function):
            cases_checked += 1
            old_status, old_out = run_one(old_mod, name, args)
            new_status, new_out = run_one(new_mod, name, args)
            # Different status (ok vs error) or different output = divergence.
            # Note: for errors we compare only the exception type, not the
            # message, to avoid noise from wording changes.
            old_key = (old_status, old_out.split(":")[0] if old_status == "error" else old_out)
            new_key = (new_status, new_out.split(":")[0] if new_status == "error" else new_out)
            if old_key != new_key:
                divergences.append(Divergence(name, args, f"{old_status}:{old_out}", f"{new_status}:{new_out}"))

    # Functions added/removed are also a signal, reported as divergences.
    for name in sorted(set(old_funcs) - set(new_funcs)):
        divergences.append(Divergence(name, (), "present in old", "removed in new"))
    for name in sorted(set(new_funcs) - set(old_funcs)):
        divergences.append(Divergence(name, (), "not in old", "added in new"))

    return Report(functions_checked=len(common), cases_checked=cases_checked,
                  divergences=divergences)
