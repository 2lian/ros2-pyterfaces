import pytest
from rclpy.serialization import deserialize_message, serialize_message

from ros2_pyterfaces.cyclone.idl import IdlStruct

from .utils import MESSAGE_TYPE_PARAMS, random_message_for_type


@pytest.mark.parametrize("msg_type", MESSAGE_TYPE_PARAMS)
def test_ros_serialize_cyclone_deserialize(msg_type: type[IdlStruct]) -> None:
    cyclone_msg = random_message_for_type(msg_type)
    ros_bytes = serialize_message(cyclone_msg.to_ros())
    cyclone_from_ros_bytes = msg_type.deserialize(ros_bytes)

    expected_core = cyclone_from_ros_bytes.to_core_message()
    assert cyclone_from_ros_bytes.to_core_message() == expected_core


@pytest.mark.parametrize("msg_type", MESSAGE_TYPE_PARAMS)
def test_cyclone_serialize_ros_deserialize(msg_type: type[IdlStruct]) -> None:
    ros_type = msg_type.to_ros_type()
    cyclone_msg = random_message_for_type(msg_type)
    expected_core = cyclone_msg.to_core_message()

    cyclone_bytes = cyclone_msg.serialize()
    ros_from_cyclone_bytes = deserialize_message(cyclone_bytes, ros_type)

    actual_core = msg_type.from_ros(ros_from_cyclone_bytes).to_core_message()

    assert actual_core == expected_core
