from __future__ import annotations

import hashlib
import json
import typing as t
from collections.abc import Mapping
from typing import Any

from .idl import (
    get_message_type_name,
    is_message_type,
    message_field_annotations,
    message_field_names,
    unwrap_annotated,
)


def ros2_type_hash_from_json(type_description_json: str) -> "hashlib._Hash":
    """
    Compute the raw RIHS01 hash from type description JSON.
    """

    raw = json.loads(type_description_json)

    if "successful" in raw:
        if not raw.get("successful", False):
            raise ValueError(
                f"GetTypeDescription response is not successful: {raw.get('failure_reason', '')}"
            )
        raw = raw["type_description"]

    if not isinstance(raw, dict):
        raise TypeError("Top-level JSON must decode to an object")

    if "type_description" not in raw or "referenced_type_descriptions" not in raw:
        raise ValueError(
            "Expected a TypeDescription JSON object with keys "
            "'type_description' and 'referenced_type_descriptions'"
        )

    def normalize_field_type(ft: dict[str, Any]) -> dict[str, Any]:
        return {
            "type_id": ft["type_id"],
            "capacity": ft["capacity"],
            "string_capacity": ft["string_capacity"],
            "nested_type_name": ft["nested_type_name"],
        }

    def normalize_field(field: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": field["name"],
            "type": normalize_field_type(field["type"]),
        }

    def normalize_individual(td: dict[str, Any]) -> dict[str, Any]:
        return {
            "type_name": td["type_name"],
            "fields": [normalize_field(f) for f in td["fields"]],
        }

    hashable = {
        "type_description": normalize_individual(raw["type_description"]),
        "referenced_type_descriptions": [
            normalize_individual(td)
            for td in sorted(
                raw["referenced_type_descriptions"],
                key=lambda td: td["type_name"],
            )
        ],
    }

    hashable_repr = json.dumps(
        hashable,
        skipkeys=False,
        ensure_ascii=True,
        check_circular=True,
        allow_nan=False,
        indent=None,
        separators=(", ", ": "),
        sort_keys=False,
    )

    return hashlib.sha256(hashable_repr.encode("utf-8"))


_ROS_SCALAR_TYPE_IDS = {
    "nested": 1,
    "int8": 2,
    "uint8": 3,
    "int16": 4,
    "uint16": 5,
    "int32": 6,
    "uint32": 7,
    "int64": 8,
    "uint64": 9,
    "float32": 10,
    "float64": 11,
    "char": 13,  # replaced by uint8?
    "wchar": 14,
    "bool": 15,
    "byte": 16,
    "string": 17,
    "wstring": 18,
    "fixed_string": 19,
    "fixed_wstring": 20,
    "bounded_string": 21,
    "bounded_wstring": 22,
}

_ARRAY_OFFSET = 48
_BOUNDED_SEQUENCE_OFFSET = 96
_UNBOUNDED_SEQUENCE_OFFSET = 144

_IDL_PRIMITIVE_TAG_TO_ROS = _ROS_SCALAR_TYPE_IDS


def _placeholder_field() -> dict[str, Any]:
    """
    Build the placeholder field used for empty structures.
    """
    return {
        "name": "structure_needs_at_least_one_member",
        "type": {
            "type_id": _ROS_SCALAR_TYPE_IDS["uint8"],
            "capacity": 0,
            "string_capacity": 0,
            "nested_type_name": "",
        },
        "default_value": "",
    }


def schema_to_ros_type_description_json(
    cls: type[Any],
    root_type_name: str | None = None,
    type_name_overrides: Mapping[type, str] | None = None,
    indent: int = 2,
) -> str:
    """
    Convert an IDL struct type to ROS 2 type description JSON.

    Args:
        cls: IDL struct type.
        root_type_name: Optional root ROS type name.
        type_name_overrides: Optional nested type name overrides.
        indent: JSON indentation level.

    Returns:
        Type description JSON.
    """
    if not is_message_type(cls):
        raise TypeError("cls must be an annotated schema class")

    types_map: Mapping[type, str] = (
        dict(type_name_overrides) if type_name_overrides is not None else dict()
    )

    def resolve_ros_type_name(tp_cls: type, is_root: bool = False) -> str:
        nonlocal types_map, root_type_name
        if tp_cls in types_map:
            return types_map[tp_cls]

        if is_root and root_type_name:
            return root_type_name

        name = get_message_type_name(tp_cls)
        if isinstance(name, str) and "/" in name:
            return name

        raise ValueError(
            f"No ROS type name available for {tp_cls.__module__}.{tp_cls.__qualname__}. "
            f"Pass root_type_name=... for the root class, and/or type_name_overrides={{ThatClass: 'pkg/msg/Name'}} "
            f"for nested classes."
        )

    def metadata_by_class_name(metadata: list[t.Any], class_name: str) -> t.Any | None:
        for item in metadata:
            if item.__class__.__name__ == class_name:
                return item
        return None

    def primitive_type_id_from_python_type(
        base: t.Any, metadata: list[t.Any]
    ) -> int | None:
        for item in metadata:
            if isinstance(item, str) and item in _IDL_PRIMITIVE_TAG_TO_ROS:
                return _IDL_PRIMITIVE_TAG_TO_ROS[item]
        if base is str:
            return _ROS_SCALAR_TYPE_IDS["string"]
        if base is bool:
            return _ROS_SCALAR_TYPE_IDS["bool"]
        if base is int:
            return _ROS_SCALAR_TYPE_IDS["int64"]
        if base is float:
            return _ROS_SCALAR_TYPE_IDS["float64"]
        return None

    def field_type_from_annotation(tp: t.Any) -> tuple[dict[str, t.Any], set[type]]:
        base, metadata = unwrap_annotated(tp)

        td = metadata_by_class_name(metadata, "typedef")
        if td is not None:
            return field_type_from_annotation(td.subtype)

        arr = metadata_by_class_name(metadata, "array")
        seq = metadata_by_class_name(metadata, "sequence")
        bstr = metadata_by_class_name(metadata, "bounded_str")

        if arr is not None and seq is not None:
            raise TypeError(
                f"Unsupported type annotation with both array and sequence metadata: {tp!r}"
            )

        if bstr is not None:
            return (
                {
                    "type_id": _ROS_SCALAR_TYPE_IDS["bounded_string"],
                    "capacity": 0,
                    "string_capacity": int(bstr.max_length),
                    "nested_type_name": "",
                },
                set(),
            )

        if arr is not None:
            elem_ft, refs = field_type_from_annotation(arr.subtype)
            return (
                {
                    "type_id": int(elem_ft["type_id"]) + _ARRAY_OFFSET,
                    "capacity": int(arr.length),
                    "string_capacity": int(elem_ft["string_capacity"]),
                    "nested_type_name": elem_ft["nested_type_name"],
                },
                refs,
            )

        if seq is not None:
            elem_ft, refs = field_type_from_annotation(seq.subtype)
            if seq.max_length is None:
                type_id = int(elem_ft["type_id"]) + _UNBOUNDED_SEQUENCE_OFFSET
                capacity = 0
            else:
                type_id = int(elem_ft["type_id"]) + _BOUNDED_SEQUENCE_OFFSET
                capacity = int(seq.max_length)
            return (
                {
                    "type_id": type_id,
                    "capacity": capacity,
                    "string_capacity": int(elem_ft["string_capacity"]),
                    "nested_type_name": elem_ft["nested_type_name"],
                },
                refs,
            )

        prim = primitive_type_id_from_python_type(base, metadata)
        if prim is not None:
            return (
                {
                    "type_id": prim,
                    "capacity": 0,
                    "string_capacity": 0,
                    "nested_type_name": "",
                },
                set(),
            )

        if is_message_type(base):
            return (
                {
                    "type_id": _ROS_SCALAR_TYPE_IDS["nested"],
                    "capacity": 0,
                    "string_capacity": 0,
                    "nested_type_name": resolve_ros_type_name(base, is_root=False),
                },
                {base},
            )

        raise TypeError(f"Unsupported field type annotation: {tp!r}")

    seen: dict[type, dict[str, t.Any]] = {}

    def build_individual_type(tp_cls: type[Any], is_root: bool = False) -> None:
        if tp_cls in seen:
            return

        hints = message_field_annotations(tp_cls, include_extras=True)
        raw_field_names = message_field_names(tp_cls)
        field_annotations = getattr(tp_cls, "__idl_field_annotations__", {})

        referenced: set[type] = set()
        fields: list[dict[str, t.Any]] = []

        for py_field_name in raw_field_names:
            field_tp = hints[py_field_name]
            field_type, refs = field_type_from_annotation(field_tp)
            referenced |= refs

            ros_field_name = field_annotations.get(py_field_name, {}).get(
                "name", py_field_name
            )

            fields.append(
                {
                    "name": ros_field_name,
                    "type": field_type,
                    "default_value": "",
                }
            )

        if len(fields) == 0:
            fields = [_placeholder_field()]

        seen[tp_cls] = {
            "type_name": resolve_ros_type_name(tp_cls, is_root=is_root),
            "fields": fields,
        }

        for ref_cls in referenced:
            build_individual_type(ref_cls, is_root=False)

    build_individual_type(cls, is_root=True)

    root = seen[cls]
    referenced = [desc for c, desc in seen.items() if c is not cls]
    referenced.sort(key=lambda d: d["type_name"])

    out = {
        "type_description": root,
        "referenced_type_descriptions": referenced,
    }
    return json.dumps(out, indent=indent)


cyclonedds_struct_to_ros_type_description_json = schema_to_ros_type_description_json
