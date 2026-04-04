import pytest

from ros2_pyterfaces.cydr.idl import IdlStruct

from .utils import (
    SERVICE_MESSAGE_TYPE_PARAMS,
    SERVICE_MESSAGE_VALUE_PARAMS,
    SERVICE_TYPE_PARAMS,
)


@pytest.mark.parametrize("service_type", SERVICE_TYPE_PARAMS)
def test_service_to_ros_type(service_type: type) -> None:
    ros_type = service_type.to_ros_type()
    assert isinstance(ros_type, type)


@pytest.mark.parametrize("service_type", SERVICE_TYPE_PARAMS)
def test_service_event_type_is_core_schema_placeholder(service_type: type) -> None:
    event_schema = service_type.Event.to_core_schema()
    assert event_schema["__typename"] == f"{service_type.get_type_name()}_Event"
    with pytest.raises(TypeError):
        service_type.Event()
    with pytest.raises(NotImplementedError):
        service_type.Event.deserialize(b"")
    with pytest.raises(NotImplementedError):
        service_type.Event.serialize(None)


@pytest.mark.parametrize(
    "service_msg_type",
    SERVICE_MESSAGE_TYPE_PARAMS,
)
def test_service_message_to_ros_type(service_msg_type: type[IdlStruct]) -> None:
    ros_type = service_msg_type.to_ros_type()
    assert isinstance(ros_type, type)


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
    roundtrip = msg_type.from_ros(service_msg.to_ros())
    assert roundtrip.to_core_message() == service_msg.to_core_message()
