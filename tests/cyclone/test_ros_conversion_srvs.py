import pytest

from ros2_pyterfaces.cyclone.idl import IdlStruct

from .utils import (
    SERVICE_MESSAGE_TYPE_PARAMS,
    SERVICE_MESSAGE_VALUE_PARAMS,
    SERVICE_TYPE_PARAMS,
)


@pytest.mark.parametrize("service_type", SERVICE_TYPE_PARAMS)
def test_service_to_ros_type(service_type: type) -> None:
    ros_type = service_type.to_ros_type()
    return


@pytest.mark.parametrize(
    "service_msg_type",
    SERVICE_MESSAGE_TYPE_PARAMS,
)
def test_service_message_to_ros_type(service_msg_type: type[IdlStruct]) -> None:
    ros_type = service_msg_type.to_ros_type()
    return


@pytest.mark.parametrize("service_msg", SERVICE_MESSAGE_VALUE_PARAMS)
def test_service_message_to_ros(service_msg: IdlStruct) -> None:
    ros_type = type(service_msg).to_ros_type()
    ros_msg = service_msg.to_ros()
    assert isinstance(ros_msg, ros_type)


@pytest.mark.parametrize(
    "service_msg", SERVICE_MESSAGE_VALUE_PARAMS
)
def test_service_message_to_from_ros_roundtrip_values(service_msg: IdlStruct) -> None:
    msg_type = type(service_msg)
    msg_type.to_ros_type()
    roundtrip = msg_type.from_ros(service_msg.to_ros())
    assert roundtrip.to_core_message() == service_msg.to_core_message()
