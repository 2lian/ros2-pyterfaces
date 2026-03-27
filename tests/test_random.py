import pytest
from utils import TYPES, TYPES_IDS

from ros2_pyterfaces import idl
from ros2_pyterfaces.utils.random import random_message


def test_message_to_plain_data_normalizes_ros_message_with_annotation():
    idl_msg = idl.ServiceEventInfo(
        event_type=idl.ServiceEventInfo.REQUEST_RECEIVED,
        client_gid=bytes(range(16)),
    )
    ros_msg = idl_msg.to_ros()

    assert idl.message_to_plain_data(ros_msg, idl.ServiceEventInfo) == (
        idl.message_to_plain_data(idl_msg)
    )


@pytest.mark.parametrize("msg_type", TYPES, ids=TYPES_IDS)
def test_random_message_roundtrip(msg_type: type[idl.IdlStruct]):
    msg = random_message(msg_type)
    decoded = msg_type.deserialize(msg.serialize())

    assert idl.message_to_plain_data(decoded) == idl.message_to_plain_data(msg)


@pytest.mark.parametrize("msg_type", TYPES, ids=TYPES_IDS)
def test_random_message_is_deterministic_per_type(msg_type: type[idl.IdlStruct]):
    left = random_message(msg_type)
    right = random_message(msg_type)

    assert idl.message_to_plain_data(left) == idl.message_to_plain_data(right)
