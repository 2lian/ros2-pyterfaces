import json
import hashlib
from dataclasses import dataclass
from typing import Any, Dict, Literal, Type, TypeAlias

from . import idl

Primitives: TypeAlias = Literal[
    "bool",
    "byte",
    "char",
    "int8",
    "uint8",
    "int16",
    "uint16",
    "int32",
    "uint32",
    "int64",
    "uint64",
    "float32",
    "float64",
    "string", # only unbounded for now
]


@dataclass(frozen=True)
class BoundedString:
    max_length: int


@dataclass(frozen=True)
class Sequence:
    subtype: Primitives | "CoreSchema"


@dataclass(frozen=True)
class Array:
    subtype: Primitives | "CoreSchema"
    length: int

Entry: TypeAlias = Primitives | Sequence | Array | BoundedString

CoreSchema :TypeAlias = Dict[str, Entry | "CoreSchema"]

# core shema examples:

Time = {
    "__typename": "builtin_interfaces/msg/Duration",
    "sec": "int32",
    "nanosec": "uint32",
}

Header = {
    "__typename": "std_msgs/msg/Header",
    "stamp": Time,
    "frame_id": "uint32",
}

JointState = {
    "__typename": "sensor_msgs/msg/JointState",
    "header": Header,
    "name": Sequence("uint32"),
    "position": Sequence("float64"),
    "velocity": Sequence("float64"),
    "effort": Sequence("float64"),
}

# core type message example:


JointState = {
    "__typename": "sensor_msgs/msg/JointState",
    "header": {
        "__typename": "std_msgs/msg/Header",
        "stamp": {
            "__typename": "builtin_interfaces/msg/Duration",
            "sec": 17000000,
            "nanosec": 43,
        },
        "frame_id": "some_string",
    },
    "name": ["j1", "j2"],
    "position": [1, 2],
    "velocity": [1, 2],
    "effort": [1, 2],
}

# needed functions:

def json_style_type_description(core_descrption: CoreSchema) -> Dict[str, Any]:
    """Return the ros type description in a json style dict.

    Args:
        core_descrption: The schema to make the representation of

    Returns:
        Dictionary representing the ros type description of the schema
    """
    ...

def json_type_description(...) -> str:
    """TODO"""
    json.dumps(json_style_type_description(...))


def _hash_rihs01_raw(schema: CoreSchema) -> "hashlib._Hash":
    """
    Compute the raw RIHS01 hash object for a schema class.
    """
    ...

def hash_rihs01(schema: CoreSchema) -> str:
    """
    Compute the RIHS01 hash string for a schema class.
    """
    return f"RIHS01_{_hash_rihs01_raw(schema).hexdigest()}"

def ros2_type_hash_from_json(type_description_json: str) -> "hashlib._Hash":
    """
    Compute the raw RIHS01 hash from type description JSON.
    """
    # this is copied from the old code

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

def to_ros_type(schema:CoreSchema) -> Type:
    """
    Resolve the matching ROS type for a schema class.
    """

def from_ros_type(Any) -> CoreSchema:
    """Not needed"""
    return NotImplemented
