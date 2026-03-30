from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import partial
from importlib import import_module
from typing import Any, cast, get_args

import numpy as np
from cydr import idl as jit_idl
from cydr.schema_types import (
    _is_ndarray_annotation,
    _ndarray_element_type,
    _ndarray_fixed_length,
)

from ..idl import IdlStruct as CoreStructBase
from ..idl_types import types as core_types
from ..utils.idl import (
    is_byte_sequence_annotation,
    is_uint8_sequence_annotation,
    message_field_annotations,
    unwrap_annotated,
)
from .idl import JitStruct

CoreStruct = CoreStructBase


_JIT_SCALAR_TO_CORE: dict[Any, Any] = {
    jit_idl.boolean: core_types.bool,
    jit_idl.byte: core_types.byte,
    jit_idl.int8: core_types.int8,
    jit_idl.uint8: core_types.uint8,
    jit_idl.int16: core_types.int16,
    jit_idl.uint16: core_types.uint16,
    jit_idl.int32: core_types.int32,
    jit_idl.uint32: core_types.uint32,
    jit_idl.int64: core_types.int64,
    jit_idl.uint64: core_types.uint64,
    jit_idl.float32: core_types.float32,
    jit_idl.float64: core_types.float64,
    jit_idl.string: str,
}

_CORE_STRUCT_CACHE: dict[type[JitStruct], type[CoreStruct]] = {}
_JIT_STRUCT_CACHE: dict[type[CoreStruct], type[JitStruct]] = {}
_REGISTERED_CORE_TYPES_BY_NAME: dict[str, type[CoreStruct]] | None = None
_JIT_NDARRAY_RE = re.compile(
    r"^types\.NDArray\[(?P<shape>.+),\s*types\.(?P<elem>[A-Za-z0-9_]+)\]$"
)
_JIT_SHAPE_RE = re.compile(r"""^types\.Shape\[['"](?P<length>\d+)['"]\]$""")
_JIT_STRING_TO_CORE: dict[str, Any] = {
    "types.boolean": core_types.bool,
    "types.byte": core_types.byte,
    "types.int8": core_types.int8,
    "types.uint8": core_types.uint8,
    "types.int16": core_types.int16,
    "types.uint16": core_types.uint16,
    "types.int32": core_types.int32,
    "types.uint32": core_types.uint32,
    "types.int64": core_types.int64,
    "types.uint64": core_types.uint64,
    "types.float32": core_types.float32,
    "types.float64": core_types.float64,
    "types.string": str,
    "idl.boolean": core_types.bool,
    "idl.byte": core_types.byte,
    "idl.int8": core_types.int8,
    "idl.uint8": core_types.uint8,
    "idl.int16": core_types.int16,
    "idl.uint16": core_types.uint16,
    "idl.int32": core_types.int32,
    "idl.uint32": core_types.uint32,
    "idl.int64": core_types.int64,
    "idl.uint64": core_types.uint64,
    "idl.float32": core_types.float32,
    "idl.float64": core_types.float64,
    "idl.string": str,
}
_JIT_NDARRAY_ELEMENT_TO_CORE: dict[str, Any] = {
    "Bool": core_types.bool,
    "Byte": core_types.byte,
    "Int8": core_types.int8,
    "UInt8": core_types.uint8,
    "Int16": core_types.int16,
    "UInt16": core_types.uint16,
    "Int32": core_types.int32,
    "UInt32": core_types.uint32,
    "Int64": core_types.int64,
    "UInt64": core_types.uint64,
    "Float32": core_types.float32,
    "Float64": core_types.float64,
    "Bytes": str,
}


def to_core_struct(struct: type[JitStruct] | JitStruct) -> type[CoreStruct] | CoreStruct:
    struct_type = struct if isinstance(struct, type) else type(struct)
    _ensure_supported(struct_type)

    if isinstance(struct, type):
        return _jit_type_to_core_type(struct)

    core_type = cast(type[CoreStruct], _jit_type_to_core_type(type(struct)))
    core_annotations = message_field_annotations(core_type, include_extras=True)
    kwargs = {
        field_name: _jit_value_to_core_value(
            getattr(struct, field_name),
            core_annotations[field_name],
        )
        for field_name in struct.__struct_fields__
    }
    return core_type(**kwargs)


def from_core_struct(
    struct: type[CoreStruct] | CoreStruct,
    jit_type: type[JitStruct] | None = None,
) -> type[JitStruct] | JitStruct:
    if isinstance(struct, type):
        resolved_jit_type = jit_type or _JIT_STRUCT_CACHE.get(struct)
        if resolved_jit_type is None:
            raise TypeError(f"No jitcdr type mapping available for {struct!r}")
        _ensure_supported(resolved_jit_type)
        return resolved_jit_type

    resolved_jit_type = jit_type or _JIT_STRUCT_CACHE.get(type(struct))
    if resolved_jit_type is None:
        raise TypeError(
            f"No jitcdr type mapping available for {type(struct)!r}"
        )

    _ensure_supported(resolved_jit_type)
    jit_annotations = _jit_field_annotations(resolved_jit_type)
    annotation_namespace = _jit_annotation_namespace(resolved_jit_type)
    kwargs = {
        field_name: _core_value_to_jit_value(
            getattr(struct, field_name),
            jit_annotations[field_name],
            namespace=annotation_namespace,
        )
        for field_name in resolved_jit_type.__struct_fields__
    }
    return resolved_jit_type(**kwargs)


def to_core_type_name_overrides(
    type_name_overrides: dict[type[Any], str] | None,
) -> dict[type[Any], str] | None:
    if type_name_overrides is None:
        return None

    converted: dict[type[Any], str] = {}
    for schema_type, ros_name in type_name_overrides.items():
        if isinstance(schema_type, type) and issubclass(schema_type, JitStruct):
            converted[_jit_type_to_core_type(schema_type)] = ros_name
            continue
        converted[schema_type] = ros_name
    return converted


def _jit_type_to_core_type(struct_type: type[JitStruct]) -> type[CoreStruct]:
    cached = _CORE_STRUCT_CACHE.get(struct_type)
    if cached is not None:
        return cached

    _ensure_supported(struct_type)

    registered_core_type = _registered_core_type_for(struct_type)
    if registered_core_type is not None:
        _CORE_STRUCT_CACHE[struct_type] = registered_core_type
        _JIT_STRUCT_CACHE[registered_core_type] = struct_type
        return registered_core_type

    type_name = getattr(struct_type, "__idl_typename__", "")
    namespace: dict[str, Any] = {
        "__module__": struct_type.__module__,
        "__idl_typename__": type_name,
        "__annotations__": {},
    }

    core_type = cast(type[CoreStruct], type(struct_type.__name__, (CoreStruct,), namespace))
    _CORE_STRUCT_CACHE[struct_type] = core_type
    _JIT_STRUCT_CACHE[core_type] = struct_type

    jit_annotations = _jit_field_annotations(struct_type)
    jit_defaults = _jit_field_defaults(struct_type)
    core_annotations: dict[str, Any] = {}
    field_names = struct_type.__struct_fields__
    annotation_namespace = _jit_annotation_namespace(struct_type)

    for field_name in field_names:
        jit_annotation = jit_annotations[field_name]
        core_annotation = _jit_annotation_to_core_annotation(
            jit_annotation,
            namespace=annotation_namespace,
        )
        core_annotations[field_name] = core_annotation

        if field_name not in jit_defaults:
            continue

        default_spec = jit_defaults[field_name]
        if _is_factory_default(default_spec):
            factory = cast(Any, default_spec).factory
            namespace[field_name] = field(
                default_factory=partial(
                    _jit_factory_to_core_value,
                    factory,
                    core_annotation,
                )
            )
            continue

        namespace[field_name] = _jit_value_to_core_value(default_spec, core_annotation)

    core_type.__annotations__ = core_annotations
    for field_name, value in namespace.items():
        if field_name.startswith("__"):
            continue
        setattr(core_type, field_name, value)

    dataclass(core_type)
    return core_type


def _jit_field_defaults(struct_type: type[JitStruct]) -> dict[str, Any]:
    field_names = struct_type.__struct_fields__
    defaults = getattr(struct_type, "__struct_defaults__", ())
    if not defaults:
        return {}

    first_default_index = len(field_names) - len(defaults)
    return {
        field_name: defaults[index - first_default_index]
        for index, field_name in enumerate(
            field_names[first_default_index:],
            start=first_default_index,
        )
    }


def _jit_annotation_to_core_annotation(
    annotation: Any,
    namespace: dict[str, Any] | None = None,
) -> Any:
    if isinstance(annotation, str):
        translated = _JIT_STRING_TO_CORE.get(annotation)
        if translated is not None:
            return translated

        match = _JIT_NDARRAY_RE.fullmatch(annotation)
        if match is not None:
            element_annotation = _JIT_NDARRAY_ELEMENT_TO_CORE.get(match.group("elem"))
            if element_annotation is None:
                raise TypeError(f"Unsupported jitcdr ndarray element type: {annotation!r}")

            shape = match.group("shape").strip()
            if shape == "Any":
                return core_types.sequence[element_annotation]

            shape_match = _JIT_SHAPE_RE.fullmatch(shape)
            if shape_match is None:
                raise TypeError(f"Unsupported jitcdr ndarray shape: {annotation!r}")
            return core_types.array[element_annotation, int(shape_match.group("length"))]

        if namespace is None:
            raise TypeError(f"Unsupported jitcdr annotation: {annotation!r}")
        return _jit_annotation_to_core_annotation(
            eval(annotation, namespace, namespace),
            namespace=namespace,
        )

    if isinstance(annotation, type) and issubclass(annotation, JitStruct):
        return _jit_type_to_core_type(annotation)

    if _is_ndarray_annotation(annotation):
        element_annotation = _jit_annotation_to_core_annotation(
            _ndarray_element_type(annotation),
            namespace=namespace,
        )
        fixed_length = _ndarray_fixed_length(annotation)
        if fixed_length is None:
            return core_types.sequence[element_annotation]
        return core_types.array[element_annotation, fixed_length]

    translated = _JIT_SCALAR_TO_CORE.get(annotation)
    if translated is not None:
        return translated

    raise TypeError(f"Unsupported jitcdr annotation: {annotation!r}")


def jit_annotation_to_core_annotation(annotation: Any) -> Any:
    return _jit_annotation_to_core_annotation(annotation)


def _jit_factory_to_core_value(factory_fn: Any, annotation: Any) -> Any:
    return _jit_value_to_core_value(factory_fn(), annotation)


def _jit_value_to_core_value(value: Any, annotation: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, JitStruct):
        return cast(CoreStruct, to_core_struct(value))

    if is_uint8_sequence_annotation(annotation):
        if hasattr(value, "tolist") and not isinstance(value, (str, bytes, bytearray)):
            value = value.tolist()
        if isinstance(value, (bytes, bytearray, memoryview)):
            return bytes(value)
        return bytes(int(item) & 0xFF for item in value)

    if is_byte_sequence_annotation(annotation):
        if hasattr(value, "tolist") and not isinstance(value, (str, bytes, bytearray)):
            value = value.tolist()
        if isinstance(value, (bytes, bytearray, memoryview)):
            return list(bytes(value))
        return [int(item) & 0xFF for item in value]

    base_annotation, _ = unwrap_annotated(annotation)
    if (
        hasattr(value, "item")
        and callable(value.item)
        and getattr(value, "shape", ()) == ()
    ):
        try:
            value = value.item()
        except ValueError:
            pass

    if isinstance(value, memoryview):
        value = value.tobytes()

    if base_annotation is str and isinstance(value, (bytes, bytearray)):
        return bytes(value).decode("utf-8")

    if hasattr(value, "tolist") and not isinstance(value, (str, bytes, bytearray)):
        value = value.tolist()

    args = get_args(base_annotation) or getattr(base_annotation, "__args__", ())
    if args and isinstance(value, list | tuple) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        return [_jit_value_to_core_value(item, args[0]) for item in value]

    if base_annotation is bool:
        return bool(value)
    if base_annotation is int:
        return int(value)
    if base_annotation is float:
        return float(value)

    return value


def jit_value_to_core_value(value: Any, annotation: Any) -> Any:
    return _jit_value_to_core_value(value, annotation)


def _core_value_to_jit_value(
    value: Any,
    annotation: Any,
    namespace: dict[str, Any] | None = None,
) -> Any:
    if value is None:
        return None

    if isinstance(annotation, str):
        if annotation in {"types.string", "idl.string"}:
            if isinstance(value, str):
                return value.encode("utf-8")
            return bytes(value)

        if annotation in {
            "types.boolean",
            "idl.boolean",
        }:
            return bool(value)

        if namespace is None:
            return value
        return _core_value_to_jit_value(
            value,
            eval(annotation, namespace, namespace),
            namespace=namespace,
        )

    if isinstance(value, CoreStruct):
        return cast(JitStruct, from_core_struct(value))

    if isinstance(annotation, type) and issubclass(annotation, JitStruct):
        return cast(JitStruct, from_core_struct(cast(CoreStruct, value), annotation))

    if _is_ndarray_annotation(annotation):
        elem_type = _ndarray_element_type(annotation)
        raw_values = value
        if isinstance(raw_values, (bytes, bytearray, memoryview)):
            raw_values = list(bytes(raw_values))
        elif hasattr(raw_values, "tolist") and not isinstance(raw_values, str):
            raw_values = raw_values.tolist()

        if elem_type is bytes:
            encoded_values = [
                item.encode("utf-8") if isinstance(item, str) else bytes(item)
                for item in raw_values
            ]
            return np.asarray(encoded_values, dtype=np.bytes_)

        return np.asarray(raw_values, dtype=elem_type)

    if annotation is jit_idl.string:
        if isinstance(value, str):
            return value.encode("utf-8")
        return bytes(value)

    if annotation in _JIT_SCALAR_TO_CORE:
        return annotation(value)

    return value


def core_value_to_jit_value(value: Any, annotation: Any) -> Any:
    return _core_value_to_jit_value(value, annotation)


def _is_factory_default(value: Any) -> bool:
    return hasattr(value, "factory")


def _jit_field_annotations(struct_type: type[JitStruct]) -> dict[str, Any]:
    annotations: dict[str, Any] = {}
    for base in reversed(struct_type.__mro__):
        base_annotations = getattr(base, "__annotations__", None)
        if not base_annotations:
            continue
        for field_name, field_type in base_annotations.items():
            if field_name.startswith("__"):
                annotations.pop(field_name, None)
                continue
            annotations[field_name] = field_type
    return annotations


def _jit_annotation_namespace(struct_type: type[JitStruct]) -> dict[str, Any]:
    module = __import__(struct_type.__module__, fromlist=["*"])
    return vars(module)


def _ensure_supported(struct_type: type[JitStruct]) -> None:
    reason = getattr(struct_type, "__unsupported_reason__", None)
    if reason:
        raise NotImplementedError(
            f"{struct_type.__module__}.{struct_type.__qualname__} is not implemented for jitcdr: {reason}"
        )


def _registered_core_type_for(struct_type: type[JitStruct]) -> type[CoreStruct] | None:
    type_name = getattr(struct_type, "__idl_typename__", "")
    if not type_name:
        return None
    return _registered_core_types_by_name().get(type_name)


def _registered_core_types_by_name() -> dict[str, type[CoreStruct]]:
    global _REGISTERED_CORE_TYPES_BY_NAME
    if _REGISTERED_CORE_TYPES_BY_NAME is not None:
        return _REGISTERED_CORE_TYPES_BY_NAME

    registered: dict[str, type[CoreStruct]] = {}
    for module_name in (
        "ros2_pyterfaces.cyclone.all_msgs",
        "ros2_pyterfaces.cyclone.all_srvs",
    ):
        module = import_module(module_name)
        for obj in vars(module).values():
            if not isinstance(obj, type):
                continue
            if not issubclass(obj, CoreStruct):
                continue
            if obj is CoreStruct:
                continue
            type_name = getattr(obj, "__idl_typename__", "")
            if type_name:
                registered[type_name] = obj

    _REGISTERED_CORE_TYPES_BY_NAME = registered
    return registered
