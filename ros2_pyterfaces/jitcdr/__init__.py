from importlib import import_module
from typing import Any

from .converter import to_core_struct
from .idl import JitStruct


def __getattr__(name: str) -> Any:
    if name in {"all_msgs", "all_srvs", "idl"}:
        return import_module(f"{__name__}.{name}")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
