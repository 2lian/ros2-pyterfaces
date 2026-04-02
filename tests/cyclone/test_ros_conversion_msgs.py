import pytest

from ros2_pyterfaces.cyclone.idl import IdlStruct

from .utils import MESSAGE_TYPE_IDS, MESSAGE_TYPES, random_message_for_type


def _resolved_ros_type(msg_type: type[IdlStruct]) -> type:
    return msg_type.to_ros_type()


@pytest.mark.parametrize("msg_type", MESSAGE_TYPES, ids=MESSAGE_TYPE_IDS)
def test_message_to_ros_type(msg_type: type[IdlStruct]) -> None:
    ros_type = _resolved_ros_type(msg_type)
    assert isinstance(ros_type, type)


@pytest.mark.parametrize("msg_type", MESSAGE_TYPES, ids=MESSAGE_TYPE_IDS)
def test_message_to_ros(msg_type: type[IdlStruct]) -> None:
    ros_type = _resolved_ros_type(msg_type)
    msg = random_message_for_type(msg_type)
    ros_msg = msg.to_ros()

    assert isinstance(ros_msg, ros_type)


@pytest.mark.parametrize("msg_type", MESSAGE_TYPES, ids=MESSAGE_TYPE_IDS)
def test_message_from_ros(msg_type: type[IdlStruct]) -> None:
    ros_type = _resolved_ros_type(msg_type)
    ros_msg = ros_type()
    msg = msg_type.from_ros(ros_msg)

    assert isinstance(msg, msg_type)
    assert msg.to_core_message()["__typename"] == msg_type.get_type_name()
    assert set(msg.to_core_message()) == set(msg_type.to_core_schema())


@pytest.mark.parametrize("msg_type", MESSAGE_TYPES, ids=MESSAGE_TYPE_IDS)
def test_message_to_from_ros_roundtrip(msg_type: type[IdlStruct]) -> None:
    _resolved_ros_type(msg_type)
    msg = random_message_for_type(msg_type)
    roundtrip = msg_type.from_ros(msg.to_ros())

    assert roundtrip.to_core_message() == msg.to_core_message()
