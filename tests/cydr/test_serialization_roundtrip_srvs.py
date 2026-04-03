import pytest
from rclpy.serialization import deserialize_message, serialize_message

from ros2_pyterfaces.cydr.idl import IdlStruct

from .utils import SERVICE_MESSAGE_VALUE_PARAMS


@pytest.mark.parametrize(
    "service_msg", SERVICE_MESSAGE_VALUE_PARAMS
)
def test_ros_serialize_cydr_deserialize_service_messages(
    service_msg: IdlStruct,
) -> None:
    expected_core = service_msg.to_core_message()

    msg_type = type(service_msg)
    ros_bytes = serialize_message(service_msg.to_ros())
    cydr_from_ros_bytes = msg_type.deserialize(ros_bytes)

    assert cydr_from_ros_bytes.to_core_message() == expected_core


@pytest.mark.parametrize(
    "service_msg", SERVICE_MESSAGE_VALUE_PARAMS
)
def test_cydr_serialize_ros_deserialize_service_messages(
    service_msg: IdlStruct,
) -> None:
    expected_core = service_msg.to_core_message()

    msg_type = type(service_msg)
    ros_type = msg_type.to_ros_type()

    cydr_bytes = bytes(service_msg.serialize())
    ros_from_cydr_bytes = deserialize_message(cydr_bytes, ros_type)
    result_core = msg_type.from_ros(ros_from_cydr_bytes).to_core_message()

    assert result_core == expected_core
