import importlib
import pkgutil

import pytest


PACKAGES = [
    "ros2_pyterfaces",
]


def iter_submodules(package_name: str):
    """Yield a package/module and all its recursive submodules."""
    root = importlib.import_module(package_name)
    yield package_name

    if not hasattr(root, "__path__"):
        return

    seen = set()
    stack = [(root.__name__, list(root.__path__))]

    while stack:
        parent_name, parent_paths = stack.pop()

        for module_info in pkgutil.iter_modules(parent_paths, prefix=parent_name + "."):
            name = module_info.name
            if name in seen:
                continue
            seen.add(name)
            yield name

            if module_info.ispkg:
                subpkg = importlib.import_module(name)
                if hasattr(subpkg, "__path__"):
                    stack.append((subpkg.__name__, list(subpkg.__path__)))


@pytest.mark.parametrize("package_name", PACKAGES)
def test_recursive_imports(package_name: str):
    failures = []

    for module_name in sorted(iter_submodules(package_name)):
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            failures.append(f"{module_name}: {type(exc).__name__}: {exc}")

    assert not failures, "Import failures:\n\n" + "\n".join(failures)
