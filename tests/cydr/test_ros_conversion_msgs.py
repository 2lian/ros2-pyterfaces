import pytest

from ros2_pyterfaces import core
from ros2_pyterfaces.cydr.idl import IdlStruct

from .utils import (
    MESSAGE_TYPE_PARAMS,
    MESSAGE_VALUE_PARAMS,
)


def _assert_entry_matches_schema(entry: core.SchemaEntry, value: object) -> None:
    if isinstance(entry, dict):
        assert isinstance(value, dict)
        _assert_message_matches_schema(entry, value)
        return

    if isinstance(entry, core.Sequence):
        if entry.subtype == "byte":
            assert isinstance(value, (bytes, bytearray, memoryview))
            if entry.max_length is not None:
                assert len(value) <= entry.max_length
            return
        assert isinstance(value, list)
        if entry.max_length is not None:
            assert len(value) <= entry.max_length
        for item in value:
            _assert_entry_matches_schema(entry.subtype, item)
        return

    if isinstance(entry, core.Array):
        if entry.subtype == "byte":
            assert isinstance(value, (bytes, bytearray, memoryview))
            assert len(value) == entry.length
            return
        assert isinstance(value, list)
        assert len(value) == entry.length
        for item in value:
            _assert_entry_matches_schema(entry.subtype, item)
        return

    if isinstance(entry, core.BoundedString):
        assert isinstance(value, str)
        assert len(value) <= entry.max_length
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
        return
    if entry == "byte":
        assert isinstance(value, (bytes, bytearray, memoryview))
        assert len(value) == 1
        return
    assert isinstance(value, int) and not isinstance(value, bool)


def _assert_message_matches_schema(
    schema: core.CoreSchema, message: dict[str, object]
) -> None:
    assert message["__typename"] == schema["__typename"]
    assert set(message.keys()) == set(schema.keys())
    for field_name, entry in schema.items():
        if field_name == "__typename":
            continue
        _assert_entry_matches_schema(entry, message[field_name])


@pytest.mark.parametrize("msg_type", MESSAGE_TYPE_PARAMS)
def test_message_to_ros_type(msg_type: type[IdlStruct]) -> None:
    ros_type = msg_type.to_ros_type()
    assert isinstance(ros_type, type)


@pytest.mark.parametrize("msg", MESSAGE_VALUE_PARAMS)
def test_message_to_ros(msg: IdlStruct) -> None:
    msg_type = type(msg)
    ros_type = msg_type.to_ros_type()
    ros_msg = msg.to_ros()

    assert isinstance(ros_msg, ros_type)


@pytest.mark.parametrize("msg_type", MESSAGE_TYPE_PARAMS)
def test_message_from_ros(msg_type: type[IdlStruct]) -> None:
    ros_type = msg_type.to_ros_type()
    ros_msg = ros_type()
    msg = msg_type.from_ros(ros_msg)

    assert isinstance(msg, msg_type)
    _assert_message_matches_schema(msg_type.to_core_schema(), msg.to_core_message())


@pytest.mark.parametrize("msg", MESSAGE_VALUE_PARAMS)
def test_message_to_from_ros_roundtrip(msg: IdlStruct) -> None:
    msg_type = type(msg)
    msg_type.to_ros_type()
    roundtrip = msg_type.from_ros(msg.to_ros())

    assert roundtrip.to_core_message() == msg.to_core_message()
