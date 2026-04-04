from concurrent.futures import ThreadPoolExecutor
import inspect
from typing import Any


def _collect_brewable_types(*modules: Any) -> list[type[Any]]:
    brewable_by_typename: dict[str, type[Any]] = {}
    anonymous: list[type[Any]] = []

    for module in modules:
        for value in vars(module).values():
            if not inspect.isclass(value):
                continue
            if not callable(getattr(value, "brew", None)):
                continue
            if isinstance(getattr(value, "__unsupported_reason__", None), str):
                continue

            get_type_name = getattr(value, "get_type_name", None)
            if callable(get_type_name):
                brewable_by_typename.setdefault(get_type_name(), value)
                continue

            anonymous.append(value)

    return sorted(
        brewable_by_typename.values(),
        key=lambda value: value.get_type_name(),
    ) + anonymous


def _compile_types(
    msg_types: list[type[Any]], max_workers: int | None = None
) -> list[type[Any]]:
    if max_workers != 1:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(msg_type.brew) for msg_type in msg_types]
            for future in futures:
                try:
                    future.result()
                except Exception:
                    pass

    for msg_type in msg_types:
        msg_type.brew()

    return msg_types


def _compile_all(max_workers: int | None = None) -> list[type[Any]]:
    from . import all_msgs, all_srvs

    msg_types = _collect_brewable_types(all_msgs, all_srvs)
    return _compile_types(msg_types, max_workers=max_workers)
