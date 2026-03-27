"""
Internal IDL runtime helpers.
"""

from collections.abc import Sequence
from typing import Annotated, Any, ClassVar, Final, Literal, get_args, get_origin

import cyclonedds_idl as _idl


def unwrap_annotated(tp: Any) -> tuple[Any, list[Any]]:
    metadata: list[Any] = []
    while get_origin(tp) is Annotated:
        args = get_args(tp)
        tp = args[0]
        metadata.extend(args[1:])
    return tp, metadata


def is_idl_struct_type(tp: Any, struct_base: type[Any]) -> bool:
    tp, _ = unwrap_annotated(tp)
    return isinstance(tp, type) and issubclass(tp, struct_base)


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


class IdlMetaIgnoreFinal(type(_idl.IdlStruct)):
    def __new__(mcls, name, bases, namespace, **kwargs):
        """
        Create a class while stripping ``Final`` and ``Literal`` field annotations.
        """
        ann = namespace.get("__annotations__")
        if ann:
            for key in list(ann):
                if get_origin(ann[key]) is ClassVar:
                    ann.pop(key)
                elif get_origin(ann[key]) is Literal:
                    ann.pop(key)
                elif get_origin(ann[key]) is Final:
                    ann.pop(key)
        return super().__new__(mcls, name, bases, namespace, **kwargs)
