import pytest
from rclpy.serialization import deserialize_message, serialize_message

from ros2_pyterfaces.cydr.idl import IdlStruct

from .utils import MESSAGE_VALUE_IDS, MESSAGE_VALUES

@pytest.mark.parametrize("msg", MESSAGE_VALUES, ids=MESSAGE_VALUE_IDS)
def test_cydr_serialize_deserialize(msg: IdlStruct) -> None:
    msg_type = type(msg)
    expected_core = msg.to_core_message()

    raw = msg.serialize()
    roundtrip = msg_type.deserialize(raw)

    assert roundtrip.to_core_message() == expected_core


@pytest.mark.parametrize("msg", MESSAGE_VALUES, ids=MESSAGE_VALUE_IDS)
def test_ros_serialize_cydr_deserialize(msg: IdlStruct) -> None:
    msg_type = type(msg)
    expected_core = msg.to_core_message()

    ros_bytes = serialize_message(msg.to_ros())
    cydr_from_ros_bytes = msg_type.deserialize(ros_bytes)

    assert cydr_from_ros_bytes.to_core_message() == expected_core


@pytest.mark.parametrize("msg", MESSAGE_VALUES, ids=MESSAGE_VALUE_IDS)
def test_cydr_serialize_ros_deserialize(msg: IdlStruct) -> None:
    msg_type = type(msg)
    ros_type = msg_type.to_ros_type()
    expected_core = msg.to_core_message()

    cydr_bytes = bytes(msg.serialize())
    ros_from_cydr_bytes = deserialize_message(cydr_bytes, ros_type)

    actual_core = msg_type.from_ros(ros_from_cydr_bytes).to_core_message()

    assert actual_core == expected_core
