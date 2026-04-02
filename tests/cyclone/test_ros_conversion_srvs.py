import pytest

from ros2_pyterfaces.cyclone.idl import IdlStruct

from .utils import (
    SERVICE_MESSAGE_TYPE_IDS,
    SERVICE_MESSAGE_TYPES,
    SERVICE_MESSAGE_VALUE_IDS,
    SERVICE_MESSAGE_VALUES,
    SERVICE_TYPE_IDS,
    SERVICE_TYPES,
)


@pytest.mark.parametrize("service_type", SERVICE_TYPES, ids=SERVICE_TYPE_IDS)
def test_service_to_ros_type(service_type: type) -> None:
    ros_type = service_type.to_ros_type()
    return


@pytest.mark.parametrize(
    "service_msg_type",
    SERVICE_MESSAGE_TYPES,
    ids=SERVICE_MESSAGE_TYPE_IDS,
)
def test_service_message_to_ros_type(service_msg_type: type[IdlStruct]) -> None:
    ros_type = service_msg_type.to_ros_type()
    return


@pytest.mark.parametrize("service_msg", SERVICE_MESSAGE_VALUES, ids=SERVICE_MESSAGE_VALUE_IDS)
def test_service_message_to_ros(service_msg: IdlStruct) -> None:
    ros_type = type(service_msg).to_ros_type()
    ros_msg = service_msg.to_ros()
    assert isinstance(ros_msg, ros_type)


@pytest.mark.parametrize(
    "service_msg", SERVICE_MESSAGE_VALUES, ids=SERVICE_MESSAGE_VALUE_IDS
)
def test_service_message_to_from_ros_roundtrip_values(service_msg: IdlStruct) -> None:
    msg_type = type(service_msg)
    msg_type.to_ros_type()
    roundtrip = msg_type.from_ros(service_msg.to_ros())
    assert roundtrip.to_core_message() == service_msg.to_core_message()
