from __future__ import annotations

import pytest
from rclpy.serialization import deserialize_message, serialize_message

from ros2_pyterfaces.core import (
    CoreSchema,
    all_msgs,
    from_ros,
    get_type_name,
    random_message,
    to_ros,
    to_ros_type,
)

from .utils import MESSAGE_SCHEMA_IDS, MESSAGE_SCHEMAS


def _try_resolve_ros_type(schema: CoreSchema) -> type | None:
    try:
        return to_ros_type(schema)
    except (ImportError, ModuleNotFoundError, AttributeError, ValueError):
        return None


_RESOLVED_BY_TYPENAME = {
    get_type_name(schema): _try_resolve_ros_type(schema) for schema in MESSAGE_SCHEMAS
}
IGNORED_MESSAGE_SCHEMA_TYPENAMES = {
    get_type_name(schema)
    for schema in MESSAGE_SCHEMAS
    if _RESOLVED_BY_TYPENAME[get_type_name(schema)] is None
}
MESSAGE_SCHEMA_PARAMS = [
    pytest.param(
        schema,
        id=schema_id,
        marks=(
            [pytest.mark.skip(reason=f"in ignore list: {get_type_name(schema)}")]
            if get_type_name(schema) in IGNORED_MESSAGE_SCHEMA_TYPENAMES
            else []
        ),
    )
    for schema, schema_id in zip(MESSAGE_SCHEMAS, MESSAGE_SCHEMA_IDS)
]


def _resolved_ros_type(schema: CoreSchema) -> type:
    ros_type = _RESOLVED_BY_TYPENAME[get_type_name(schema)]
    assert ros_type is not None
    return ros_type


@pytest.mark.parametrize(
    "schema", MESSAGE_SCHEMA_PARAMS
)
def test_message_to_ros_type(schema: CoreSchema) -> None:
    ros_type = _resolved_ros_type(schema)
    assert isinstance(ros_type, type)


@pytest.mark.parametrize(
    "schema", MESSAGE_SCHEMA_PARAMS
)
def test_message_to_ros(schema: CoreSchema) -> None:
    ros_type = _resolved_ros_type(schema)
    core_msg = random_message(schema)
    ros_msg = to_ros(core_msg)

    assert isinstance(ros_msg, ros_type)


@pytest.mark.parametrize(
    "schema", MESSAGE_SCHEMA_PARAMS
)
def test_message_from_ros(schema: CoreSchema) -> None:
    ros_type = _resolved_ros_type(schema)
    ros_msg = ros_type()
    core_msg = from_ros(schema, ros_msg)

    assert core_msg["__typename"] == schema["__typename"]
    assert set(core_msg) == set(schema)


@pytest.mark.parametrize(
    "schema", MESSAGE_SCHEMA_PARAMS
)
def test_message_to_from_ros_roundtrip(schema: CoreSchema) -> None:
    _resolved_ros_type(schema)
    core_msg = random_message(schema)
    roundtrip = from_ros(schema, to_ros(core_msg))

    assert roundtrip == core_msg


def test_to_ros_sequence_byte_stays_bytes() -> None:
    schema = all_msgs.ParameterValue
    core_msg = {
        "__typename": "rcl_interfaces/msg/ParameterValue",
        "type": 1,
        "bool_value": False,
        "integer_value": 0,
        "double_value": 0.0,
        "string_value": "x",
        "byte_array_value": b"\x00\xeb",
        "bool_array_value": [],
        "integer_array_value": [],
        "double_array_value": [],
        "string_array_value": [],
    }
    ros_msg = to_ros(core_msg)
    assert isinstance(ros_msg.byte_array_value, (bytes, bytearray, memoryview))

    ros_bytes = serialize_message(ros_msg)
    ros_roundtrip = deserialize_message(ros_bytes, type(ros_msg))
    roundtrip = from_ros(schema, ros_roundtrip)

    assert roundtrip["byte_array_value"] == core_msg["byte_array_value"]
