from typing import Any

from ros2_pyterfaces.core import (
    Array,
    BoundedString,
    CoreSchema,
    Sequence,
    make_srv_schema,
    random_message,
)


def _assert_matches_schema(schema: CoreSchema, value: dict[str, Any]) -> None:
    assert value["__typename"] == schema["__typename"]

    for field_name, entry in schema.items():
        if field_name == "__typename":
            continue
        assert field_name in value
        _assert_entry_matches(entry, value[field_name])


def _assert_entry_matches(entry: Any, value: Any) -> None:
    if isinstance(entry, dict):
        assert isinstance(value, dict)
        _assert_matches_schema(entry, value)
        return

    if isinstance(entry, Sequence):
        assert isinstance(value, list)
        if entry.max_length is not None:
            assert len(value) <= entry.max_length
        assert len(value) >= 1
        for item in value:
            _assert_entry_matches(entry.subtype, item)
        return

    if isinstance(entry, Array):
        assert isinstance(value, list)
        assert len(value) == entry.length
        for item in value:
            _assert_entry_matches(entry.subtype, item)
        return

    if isinstance(entry, BoundedString):
        assert isinstance(value, str)
        assert 1 <= len(value) <= entry.max_length
        return

    assert isinstance(entry, str)
    if entry == "bool":
        assert isinstance(value, bool)
        return
    if entry in {"float32", "float64"}:
        assert isinstance(value, float)
        return
    if entry == "string":
        assert isinstance(value, str)
        assert len(value) >= 1
        return
    assert isinstance(value, int)


TIME_SCHEMA: CoreSchema = {
    "__typename": "builtin_interfaces/msg/Time",
    "sec": "int32",
    "nanosec": "uint32",
}

HEADER_SCHEMA: CoreSchema = {
    "__typename": "std_msgs/msg/Header",
    "stamp": TIME_SCHEMA,
    "frame_id": "string",
}

JOINT_STATE_SCHEMA: CoreSchema = {
    "__typename": "sensor_msgs/msg/JointState",
    "header": HEADER_SCHEMA,
    "name": Sequence("string"),
    "position": Sequence("float64"),
    "velocity": Sequence("float64"),
    "effort": Sequence("float64"),
}


def test_random_message_is_deterministic_with_default_seed() -> None:
    first = random_message(JOINT_STATE_SCHEMA)
    second = random_message(JOINT_STATE_SCHEMA)

    assert first == second


def test_random_message_uses_explicit_seed() -> None:
    first = random_message(JOINT_STATE_SCHEMA, seed=7)
    second = random_message(JOINT_STATE_SCHEMA, seed=7)
    third = random_message(JOINT_STATE_SCHEMA, seed=11)

    assert first == second
    assert first != third


def test_random_message_matches_message_schema_shape() -> None:
    random_joint_state = random_message(JOINT_STATE_SCHEMA, seed=3)
    _assert_matches_schema(JOINT_STATE_SCHEMA, random_joint_state)


def test_random_message_supports_bounded_string_and_array() -> None:
    custom_schema: CoreSchema = {
        "__typename": "pkg/msg/Custom",
        "name": BoundedString(4),
        "data": Array("uint8", 5),
        "values": Sequence("float32", 2),
    }
    random_custom = random_message(custom_schema, seed=4)

    _assert_matches_schema(custom_schema, random_custom)


def test_random_message_supports_service_schema() -> None:
    request_schema: CoreSchema = {
        "__typename": "pkg/srv/SetBool_Request",
        "data": "bool",
    }
    response_schema: CoreSchema = {
        "__typename": "pkg/srv/SetBool_Response",
        "success": "bool",
        "message": "string",
    }
    service_schema = make_srv_schema(request_schema, response_schema)

    random_service_message = random_message(service_schema, seed=9)
    _assert_matches_schema(service_schema, random_service_message)
