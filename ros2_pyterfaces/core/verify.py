from typing import Any

from .types import Array, BoundedString, CoreSchema, SchemaEntry, Sequence, TYPENAME_KEY


def verify_message(schema: CoreSchema, message: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    if not isinstance(message, dict):
        return [f"$ expected dict core message, got {type(message).__name__}"]

    expected_type_name = schema.get(TYPENAME_KEY)
    actual_type_name = message.get(TYPENAME_KEY)
    if actual_type_name != expected_type_name:
        issues.append(
            f"{TYPENAME_KEY} expected {expected_type_name!r}, got {actual_type_name!r}"
        )

    schema_keys = set(schema.keys())
    message_keys = set(message.keys())

    missing_keys = sorted(schema_keys - message_keys)
    for key in missing_keys:
        issues.append(f"{key} missing")

    extra_keys = sorted(message_keys - schema_keys)
    for key in extra_keys:
        issues.append(f"{key} unexpected")

    for field_name, entry in schema.items():
        if field_name == TYPENAME_KEY:
            continue
        if field_name not in message:
            continue
        _verify_entry(entry, message[field_name], field_name, issues)

    return issues


_INTEGER_PRIMITIVES = {
    "char",
    "int8",
    "uint8",
    "int16",
    "uint16",
    "int32",
    "uint32",
    "int64",
    "uint64",
}


def _verify_entry(entry: SchemaEntry, value: Any, path: str, issues: list[str]) -> None:
    if isinstance(entry, dict):
        if not isinstance(value, dict):
            issues.append(f"{path} expected dict, got {type(value).__name__}")
            return
        nested_issues = verify_message(entry, value)
        for issue in nested_issues:
            issues.append(f"{path}.{issue}")
        return

    if isinstance(entry, Sequence):
        subtype = entry.subtype
        if subtype == "byte":
            if not isinstance(value, (bytes, bytearray, memoryview)):
                issues.append(
                    f"{path} expected (bytes | bytearray | memoryview), got {type(value).__name__}"
                )
                return
            if entry.max_length is not None and len(value) > entry.max_length:
                issues.append(
                    f"{path} expected len <= {entry.max_length}, got {len(value)}"
                )
            return

        if not isinstance(value, list):
            issues.append(f"{path} expected list, got {type(value).__name__}")
            return

        if entry.max_length is not None and len(value) > entry.max_length:
            issues.append(f"{path} expected len <= {entry.max_length}, got {len(value)}")

        for index, item in enumerate(value):
            _verify_entry(subtype, item, f"{path}[{index}]", issues)
        return

    if isinstance(entry, Array):
        subtype = entry.subtype
        if subtype == "byte":
            if not isinstance(value, (bytes, bytearray, memoryview)):
                issues.append(
                    f"{path} expected (bytes | bytearray | memoryview), got {type(value).__name__}"
                )
                return
            if len(value) != entry.length:
                issues.append(f"{path} expected len == {entry.length}, got {len(value)}")
            return

        if not isinstance(value, list):
            issues.append(f"{path} expected list, got {type(value).__name__}")
            return
        if len(value) != entry.length:
            issues.append(f"{path} expected len == {entry.length}, got {len(value)}")
            return

        for index, item in enumerate(value):
            _verify_entry(subtype, item, f"{path}[{index}]", issues)
        return

    if isinstance(entry, BoundedString):
        if not isinstance(value, str):
            issues.append(f"{path} expected str, got {type(value).__name__}")
            return
        if len(value) > entry.max_length:
            issues.append(f"{path} expected len <= {entry.max_length}, got {len(value)}")
        return

    if not isinstance(entry, str):
        issues.append(f"{path} has unsupported schema entry {entry!r}")
        return

    if entry == "bool":
        if not isinstance(value, bool):
            issues.append(f"{path} expected bool, got {type(value).__name__}")
        return

    if entry in {"float32", "float64"}:
        if not isinstance(value, float):
            issues.append(f"{path} expected float, got {type(value).__name__}")
        return

    if entry == "string":
        if not isinstance(value, str):
            issues.append(f"{path} expected str, got {type(value).__name__}")
        return

    if entry == "byte":
        if not isinstance(value, (bytes, bytearray, memoryview)):
            issues.append(
                f"{path} expected (bytes | bytearray | memoryview) len == 1, got {type(value).__name__}"
            )
            return
        if len(value) != 1:
            issues.append(f"{path} expected len == 1, got {len(value)}")
        return

    if entry in _INTEGER_PRIMITIVES:
        if not isinstance(value, int) or isinstance(value, bool):
            issues.append(f"{path} expected int, got {type(value).__name__}")
        return

    issues.append(f"{path} has unsupported primitive schema entry {entry!r}")
