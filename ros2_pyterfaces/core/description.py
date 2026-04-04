import hashlib
import json
from typing import Any

from .schema import get_type_name
from .types import (
    _TYPENAME_KEY,
    Array,
    BoundedString,
    CoreSchema,
    SchemaEntry,
    Sequence,
)

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
    "char": 13,
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

_PRIMITIVE_TO_TYPE_ID = {
    "bool": _ROS_SCALAR_TYPE_IDS["bool"],
    "byte": _ROS_SCALAR_TYPE_IDS["byte"],
    "char": _ROS_SCALAR_TYPE_IDS["char"],
    "int8": _ROS_SCALAR_TYPE_IDS["int8"],
    "uint8": _ROS_SCALAR_TYPE_IDS["uint8"],
    "int16": _ROS_SCALAR_TYPE_IDS["int16"],
    "uint16": _ROS_SCALAR_TYPE_IDS["uint16"],
    "int32": _ROS_SCALAR_TYPE_IDS["int32"],
    "uint32": _ROS_SCALAR_TYPE_IDS["uint32"],
    "int64": _ROS_SCALAR_TYPE_IDS["int64"],
    "uint64": _ROS_SCALAR_TYPE_IDS["uint64"],
    "float32": _ROS_SCALAR_TYPE_IDS["float32"],
    "float64": _ROS_SCALAR_TYPE_IDS["float64"],
    "string": _ROS_SCALAR_TYPE_IDS["string"],
}


def ros2_type_hash_from_json(type_description_json: str) -> "hashlib._Hash":
    raw = json.loads(type_description_json)

    if "successful" in raw:
        if not raw.get("successful", False):
            raise ValueError(
                "GetTypeDescription response is not successful: "
                f"{raw.get('failure_reason', '')}"
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


def _placeholder_field() -> dict[str, Any]:
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


def _field_type(
    entry: SchemaEntry,
) -> tuple[dict[str, Any], list[CoreSchema]]:
    if isinstance(entry, str):
        if entry not in _PRIMITIVE_TO_TYPE_ID:
            raise TypeError(f"Unsupported primitive type: {entry!r}")
        return (
            {
                "type_id": _PRIMITIVE_TO_TYPE_ID[entry],
                "capacity": 0,
                "string_capacity": 0,
                "nested_type_name": "",
            },
            [],
        )

    if isinstance(entry, BoundedString):
        if entry.max_length <= 0:
            raise ValueError("BoundedString.max_length must be > 0")
        return (
            {
                "type_id": _ROS_SCALAR_TYPE_IDS["bounded_string"],
                "capacity": 0,
                "string_capacity": int(entry.max_length),
                "nested_type_name": "",
            },
            [],
        )

    if isinstance(entry, Array):
        if entry.length <= 0:
            raise ValueError("Array.length must be > 0")
        element_type, refs = _field_type(entry.subtype)
        return (
            {
                "type_id": int(element_type["type_id"]) + _ARRAY_OFFSET,
                "capacity": int(entry.length),
                "string_capacity": int(element_type["string_capacity"]),
                "nested_type_name": element_type["nested_type_name"],
            },
            refs,
        )

    if isinstance(entry, Sequence):
        element_type, refs = _field_type(entry.subtype)
        if entry.max_length is None:
            type_id = int(element_type["type_id"]) + _UNBOUNDED_SEQUENCE_OFFSET
            capacity = 0
        else:
            if entry.max_length <= 0:
                raise ValueError("Sequence.max_length must be > 0 when provided")
            type_id = int(element_type["type_id"]) + _BOUNDED_SEQUENCE_OFFSET
            capacity = int(entry.max_length)
        return (
            {
                "type_id": type_id,
                "capacity": capacity,
                "string_capacity": int(element_type["string_capacity"]),
                "nested_type_name": element_type["nested_type_name"],
            },
            refs,
        )

    if isinstance(entry, dict):
        nested_type_name = get_type_name(entry)
        return (
            {
                "type_id": _ROS_SCALAR_TYPE_IDS["nested"],
                "capacity": 0,
                "string_capacity": 0,
                "nested_type_name": nested_type_name,
            },
            [entry],
        )

    raise TypeError(f"Unsupported schema entry: {entry!r}")


def json_style_type_description(core_description: CoreSchema) -> dict[str, Any]:
    root_type_name = get_type_name(core_description)
    seen: dict[str, dict[str, Any]] = {}

    def build_description(schema: CoreSchema) -> None:
        type_name = get_type_name(schema)
        if type_name in seen:
            return

        is_event_schema = type_name.endswith("_Event")

        seen[type_name] = {
            "type_name": type_name,
            "fields": [],
        }

        fields: list[dict[str, Any]] = []
        referenced: list[CoreSchema] = []

        for field_name, field_entry in schema.items():
            if field_name == _TYPENAME_KEY:
                continue

            if is_event_schema and field_name in {"request", "response"} and isinstance(
                field_entry, dict
            ):
                field_type, refs = _field_type(Sequence(field_entry, 1))
            else:
                field_type, refs = _field_type(field_entry)
            fields.append(
                {
                    "name": field_name,
                    "type": field_type,
                    "default_value": "",
                }
            )
            referenced.extend(refs)

        if not fields:
            fields = [_placeholder_field()]

        seen[type_name]["fields"] = fields

        for nested_schema in referenced:
            build_description(nested_schema)

    build_description(core_description)

    root = seen[root_type_name]
    referenced = [
        description
        for type_name, description in seen.items()
        if type_name != root_type_name
    ]
    referenced.sort(key=lambda description: description["type_name"])

    return {
        "type_description": root,
        "referenced_type_descriptions": referenced,
    }


def json_type_description(core_description: CoreSchema, indent: int = 2) -> str:
    return json.dumps(json_style_type_description(core_description), indent=indent)


def _hash_rihs01_raw(schema: CoreSchema) -> "hashlib._Hash":
    return ros2_type_hash_from_json(json_type_description(schema, indent=2))


def hash_rihs01(schema: CoreSchema) -> str:
    return f"RIHS01_{_hash_rihs01_raw(schema).hexdigest()}"
