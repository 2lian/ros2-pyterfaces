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

from .utils import (
    SERVICE_MESSAGE_SCHEMA_IDS,
    SERVICE_MESSAGE_SCHEMAS,
    SERVICE_SCHEMA_IDS,
    SERVICE_SCHEMAS,
)


def _try_resolve_ros_type(schema: CoreSchema) -> type | None:
    try:
        return to_ros_type(schema)
    except (ImportError, ModuleNotFoundError, AttributeError, ValueError):
        return None


_RESOLVED_BY_TYPENAME = {
    get_type_name(schema): _try_resolve_ros_type(schema)
    for schema in [*SERVICE_SCHEMAS, *SERVICE_MESSAGE_SCHEMAS]
}
AVAILABLE_SERVICE_SCHEMAS = [
    schema for schema in SERVICE_SCHEMAS if _RESOLVED_BY_TYPENAME[get_type_name(schema)]
]
AVAILABLE_SERVICE_SCHEMA_IDS = [
    schema_id
    for schema, schema_id in zip(SERVICE_SCHEMAS, SERVICE_SCHEMA_IDS)
    if _RESOLVED_BY_TYPENAME[get_type_name(schema)]
]
AVAILABLE_SERVICE_MESSAGE_SCHEMAS = [
    schema
    for schema in SERVICE_MESSAGE_SCHEMAS
    if _RESOLVED_BY_TYPENAME[get_type_name(schema)]
]
AVAILABLE_SERVICE_MESSAGE_SCHEMA_IDS = [
    schema_id
    for schema, schema_id in zip(SERVICE_MESSAGE_SCHEMAS, SERVICE_MESSAGE_SCHEMA_IDS)
    if _RESOLVED_BY_TYPENAME[get_type_name(schema)]
]

if not AVAILABLE_SERVICE_SCHEMAS and not AVAILABLE_SERVICE_MESSAGE_SCHEMAS:
    pytest.skip(
        "No ROS service schemas are available in this runtime",
        allow_module_level=True,
    )


def _resolved_ros_type(schema: CoreSchema) -> type:
    ros_type = _RESOLVED_BY_TYPENAME[get_type_name(schema)]
    assert ros_type is not None
    return ros_type


@pytest.mark.parametrize(
    "schema", AVAILABLE_SERVICE_SCHEMAS, ids=AVAILABLE_SERVICE_SCHEMA_IDS
)
def test_service_to_ros_type(schema: CoreSchema) -> None:
    ros_type = _resolved_ros_type(schema)
    assert isinstance(ros_type, type)


@pytest.mark.parametrize(
    "schema", AVAILABLE_SERVICE_SCHEMAS, ids=AVAILABLE_SERVICE_SCHEMA_IDS
)
def test_service_to_ros(schema: CoreSchema) -> None:
    _resolved_ros_type(schema)
    core_msg = random_message(schema)
    ros_payload = to_ros(core_msg)

    assert isinstance(ros_payload, dict)
    assert set(ros_payload) == {"request_message", "response_message", "event_message"}
    assert isinstance(ros_payload["request_message"], to_ros_type(schema["request_message"]))
    assert isinstance(
        ros_payload["response_message"], to_ros_type(schema["response_message"])
    )
    assert isinstance(ros_payload["event_message"], to_ros_type(schema["event_message"]))


@pytest.mark.parametrize(
    "schema", AVAILABLE_SERVICE_SCHEMAS, ids=AVAILABLE_SERVICE_SCHEMA_IDS
)
def test_service_from_ros(schema: CoreSchema) -> None:
    _resolved_ros_type(schema)
    ros_payload = to_ros(random_message(schema, seed=1))
    core_msg = from_ros(schema, ros_payload)

    assert core_msg["__typename"] == schema["__typename"]
    assert set(core_msg) == set(schema)


@pytest.mark.parametrize(
    "schema", AVAILABLE_SERVICE_SCHEMAS, ids=AVAILABLE_SERVICE_SCHEMA_IDS
)
def test_service_to_from_ros_roundtrip(schema: CoreSchema) -> None:
    _resolved_ros_type(schema)
    core_msg = random_message(schema)
    roundtrip = from_ros(schema, to_ros(core_msg))

    assert roundtrip == core_msg


@pytest.mark.parametrize(
    "schema",
    AVAILABLE_SERVICE_MESSAGE_SCHEMAS,
    ids=AVAILABLE_SERVICE_MESSAGE_SCHEMA_IDS,
)
def test_service_message_to_ros_type(schema: CoreSchema) -> None:
    ros_type = _resolved_ros_type(schema)
    assert isinstance(ros_type, type)


@pytest.mark.parametrize(
    "schema",
    AVAILABLE_SERVICE_MESSAGE_SCHEMAS,
    ids=AVAILABLE_SERVICE_MESSAGE_SCHEMA_IDS,
)
def test_service_message_to_from_ros_roundtrip(schema: CoreSchema) -> None:
    _resolved_ros_type(schema)
    core_msg = random_message(schema)
    roundtrip = from_ros(schema, to_ros(core_msg))

    assert roundtrip == core_msg
