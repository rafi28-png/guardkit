"""Discover public functions from a Python file using AST inspection.

No code is executed during discovery - we only read the source tree.
This is what makes SemVer-Diff work even on repos with poor test coverage.
"""
import ast
from dataclasses import dataclass


@dataclass
class FunctionInfo:
    name: str
    arg_names: list
    arg_types: list  # annotation as a string, e.g. "int", "list", ""


def discover_functions(path: str) -> list[FunctionInfo]:
    """Return top-level public functions (names not starting with _)."""
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)

    functions = []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name.startswith("_"):
            continue
        arg_names = [a.arg for a in node.args.args]
        arg_types = []
        for a in node.args.args:
            if a.annotation is not None:
                # ast.unparse is available in Python 3.9+
                arg_types.append(ast.unparse(a.annotation))
            else:
                arg_types.append("")
        functions.append(FunctionInfo(node.name, arg_names, arg_types))
    return functions
