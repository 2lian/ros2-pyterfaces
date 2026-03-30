"""
Internal IDL runtime helpers.
"""

import sys
from collections.abc import Sequence
from typing import (
    Annotated,
    Any,
    ClassVar,
    Final,
    Literal,
    get_args,
    get_origin,
    get_type_hints,
)


def unwrap_annotated(tp: Any) -> tuple[Any, list[Any]]:
    metadata: list[Any] = []
    while get_origin(tp) is Annotated:
        args = get_args(tp)
        tp = args[0]
        metadata.extend(args[1:])
    return tp, metadata


def is_ignored_field_annotation(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return (
        annotation is ClassVar
        or annotation is Literal
        or annotation is Final
        or origin is ClassVar
        or origin is Literal
        or origin is Final
    )


def _annotation_namespace(schema_type: type[Any]) -> dict[str, Any]:
    namespace: dict[str, Any] = {}
    for base in reversed(schema_type.__mro__):
        module = sys.modules.get(base.__module__)
        if module is not None:
            namespace.update(vars(module))
    namespace.update(getattr(schema_type, "__dict__", {}))
    return namespace


def _resolve_annotation(annotation: Any, schema_type: type[Any]) -> Any:
    if not isinstance(annotation, str):
        return annotation

    namespace = _annotation_namespace(schema_type)
    try:
        return eval(annotation, namespace, namespace)
    except Exception:
        return annotation


def raw_message_field_annotations(schema_type: type[Any]) -> dict[str, Any]:
    annotations: dict[str, Any] = {}
    for base in reversed(schema_type.__mro__):
        base_annotations = getattr(base, "__annotations__", None)
        if not base_annotations:
            continue
        for field_name, field_type in base_annotations.items():
            resolved_field_type = _resolve_annotation(field_type, base)
            if is_ignored_field_annotation(resolved_field_type):
                annotations.pop(field_name, None)
                continue
            annotations[field_name] = resolved_field_type
    return annotations


def message_field_annotations(
    schema_type: type[Any], include_extras: bool = True
) -> dict[str, Any]:
    raw_annotations = raw_message_field_annotations(schema_type)
    if not raw_annotations:
        return {}

    module_globals = _annotation_namespace(schema_type)
    resolved_annotations = get_type_hints(
        schema_type,
        globalns=module_globals,
        localns=module_globals,
        include_extras=include_extras,
    )
    return {
        field_name: resolved_annotations.get(field_name, field_type)
        for field_name, field_type in raw_annotations.items()
    }


def message_field_names(schema_type: type[Any]) -> tuple[str, ...]:
    return tuple(raw_message_field_annotations(schema_type).keys())


def get_message_type_name(value_or_type: Any) -> str:
    schema_type = value_or_type if isinstance(value_or_type, type) else type(value_or_type)
    return getattr(schema_type, "__idl_typename__", "")


def is_message_type(tp: Any, struct_base: type[Any] | None = None) -> bool:
    tp, _ = unwrap_annotated(tp)
    if not isinstance(tp, type):
        return False

    if struct_base is not None:
        try:
            if issubclass(tp, struct_base):
                return True
        except TypeError:
            pass

    return bool(raw_message_field_annotations(tp)) or bool(get_message_type_name(tp))


def is_idl_struct_type(tp: Any, struct_base: type[Any]) -> bool:
    return is_message_type(tp, struct_base=struct_base)


def is_uint8_sequence_annotation(annotation: Any | None) -> bool:
    if annotation is None:
        return False

    _, metadata = unwrap_annotated(annotation)
    sequence_meta = next((item for item in metadata if hasattr(item, "subtype")), None)
    return sequence_meta is not None and _is_uint8_like_type(sequence_meta.subtype)


def is_byte_sequence_annotation(annotation: Any | None) -> bool:
    if annotation is None:
        return False

    _, metadata = unwrap_annotated(annotation)
    sequence_meta = next((item for item in metadata if hasattr(item, "subtype")), None)
    return sequence_meta is not None and _is_byte_like_type(sequence_meta.subtype)


def coerce_uint8_sequence(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, memoryview):
        return value.tobytes()
    if hasattr(value, "tolist") and not isinstance(value, str):
        value = value.tolist()
    if isinstance(value, Sequence) and not isinstance(value, str):
        return bytes(value)
    raise TypeError(f"Unsupported uint8 sequence value: {value!r}")


def coerce_byte_sequence(value: Any) -> list[int]:
    if isinstance(value, (bytes, bytearray, memoryview)):
        return list(bytes(value))
    if hasattr(value, "tolist") and not isinstance(value, str):
        value = value.tolist()
    if isinstance(value, Sequence) and not isinstance(value, str):
        normalized: list[int] = []
        for item in value:
            if isinstance(item, int):
                normalized.append(int(item))
                continue
            if isinstance(item, (bytes, bytearray, memoryview)):
                item_bytes = bytes(item)
                if len(item_bytes) != 1:
                    raise TypeError(
                        f"Unsupported byte sequence element length: {item!r}"
                    )
                normalized.append(item_bytes[0])
                continue
            raise TypeError(f"Unsupported byte sequence element: {item!r}")
        return normalized
    raise TypeError(f"Unsupported byte sequence value: {value!r}")


def to_ros_byte_sequence(value: Any) -> list[bytes]:
    if hasattr(value, "tolist") and not isinstance(value, str):
        value = value.tolist()
    if isinstance(value, (bytes, bytearray, memoryview)):
        value = bytes(value)
    if isinstance(value, Sequence) and not isinstance(value, str):
        normalized: list[bytes] = []
        for item in value:
            if isinstance(item, int):
                normalized.append(bytes([int(item) & 0xFF]))
                continue
            if isinstance(item, (bytes, bytearray, memoryview)):
                item_bytes = bytes(item)
                if len(item_bytes) != 1:
                    raise TypeError(
                        f"Unsupported ROS byte sequence element length: {item!r}"
                    )
                normalized.append(item_bytes)
                continue
            raise TypeError(f"Unsupported ROS byte sequence element: {item!r}")
        return normalized
    raise TypeError(f"Unsupported ROS byte sequence value: {value!r}")


def _is_uint8_like_type(tp: Any) -> bool:
    base_type, metadata = unwrap_annotated(tp)
    return base_type is int and "uint8" in metadata


def _is_byte_like_type(tp: Any) -> bool:
    base_type, metadata = unwrap_annotated(tp)
    return base_type is int and "byte" in metadata


def strip_ignored_field_annotations(namespace: dict[str, Any]) -> None:
    """
    Remove annotations that should not be treated as schema fields.
    """
    annotations = namespace.get("__annotations__")
    if not annotations:
        return

    for field_name in list(annotations):
        if is_ignored_field_annotation(annotations[field_name]):
            annotations.pop(field_name)
