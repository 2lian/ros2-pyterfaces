from importlib import import_module
from typing import Any

from .description import (
    _hash_rihs01_raw,
    hash_rihs01,
    json_style_type_description,
    json_type_description,
    ros2_type_hash_from_json,
)
from .random import random_message
from .ros import from_ros, to_ros, to_ros_type
from .schema import _service_name_from_request_response, get_type_name, make_srv_schema
from .verify import verify_message
from .types import (
    PRIMITIVES,
    TYPENAME_KEY,
    Array,
    BoundedString,
    CoreSchema,
    Primitive,
    SchemaEntry,
    Sequence,
)


def __getattr__(name: str) -> Any:
    if name in {"all_msgs", "all_srvs"}:
        return import_module(f"{__name__}.{name}")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Array",
    "BoundedString",
    "CoreSchema",
    "PRIMITIVES",
    "Primitive",
    "SchemaEntry",
    "Sequence",
    "TYPENAME_KEY",
    "_hash_rihs01_raw",
    "_service_name_from_request_response",
    "from_ros",
    "get_type_name",
    "hash_rihs01",
    "json_style_type_description",
    "json_type_description",
    "make_srv_schema",
    "random_message",
    "ros2_type_hash_from_json",
    "to_ros",
    "to_ros_type",
    "verify_message",
]
