from __future__ import annotations

import pytest

from ros2_pyterfaces.core import (
    CoreSchema,
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
AVAILABLE_MESSAGE_SCHEMAS = [
    schema for schema in MESSAGE_SCHEMAS if _RESOLVED_BY_TYPENAME[get_type_name(schema)]
]
AVAILABLE_MESSAGE_SCHEMA_IDS = [
    schema_id
    for schema, schema_id in zip(MESSAGE_SCHEMAS, MESSAGE_SCHEMA_IDS)
    if _RESOLVED_BY_TYPENAME[get_type_name(schema)]
]

if not AVAILABLE_MESSAGE_SCHEMAS:
    pytest.skip(
        "No ROS message schemas are available in this runtime",
        allow_module_level=True,
    )


def _resolved_ros_type(schema: CoreSchema) -> type:
    ros_type = _RESOLVED_BY_TYPENAME[get_type_name(schema)]
    assert ros_type is not None
    return ros_type


@pytest.mark.parametrize(
    "schema", AVAILABLE_MESSAGE_SCHEMAS, ids=AVAILABLE_MESSAGE_SCHEMA_IDS
)
def test_message_to_ros_type(schema: CoreSchema) -> None:
    ros_type = _resolved_ros_type(schema)
    assert isinstance(ros_type, type)


@pytest.mark.parametrize(
    "schema", AVAILABLE_MESSAGE_SCHEMAS, ids=AVAILABLE_MESSAGE_SCHEMA_IDS
)
def test_message_to_ros(schema: CoreSchema) -> None:
    ros_type = _resolved_ros_type(schema)
    core_msg = random_message(schema)
    ros_msg = to_ros(core_msg)

    assert isinstance(ros_msg, ros_type)


@pytest.mark.parametrize(
    "schema", AVAILABLE_MESSAGE_SCHEMAS, ids=AVAILABLE_MESSAGE_SCHEMA_IDS
)
def test_message_from_ros(schema: CoreSchema) -> None:
    ros_type = _resolved_ros_type(schema)
    ros_msg = ros_type()
    core_msg = from_ros(schema, ros_msg)

    assert core_msg["__typename"] == schema["__typename"]
    assert set(core_msg) == set(schema)


@pytest.mark.parametrize(
    "schema", AVAILABLE_MESSAGE_SCHEMAS, ids=AVAILABLE_MESSAGE_SCHEMA_IDS
)
def test_message_to_from_ros_roundtrip(schema: CoreSchema) -> None:
    _resolved_ros_type(schema)
    core_msg = random_message(schema)
    roundtrip = from_ros(schema, to_ros(core_msg))

    assert roundtrip == core_msg
