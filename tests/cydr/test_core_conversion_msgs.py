import pytest

from ros2_pyterfaces.cydr.idl import IdlStruct

from .utils import MESSAGE_VALUE_PARAMS


@pytest.mark.parametrize("msg", MESSAGE_VALUE_PARAMS)
def test_message_to_from_core_roundtrip(msg: IdlStruct) -> None:
    msg_type = type(msg)
    core_msg = msg.to_core_message()
    roundtrip = msg_type.from_core_message(core_msg)

    assert isinstance(roundtrip, msg_type)
    assert roundtrip.to_core_message() == core_msg
