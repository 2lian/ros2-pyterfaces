import pytest
from rclpy.serialization import deserialize_message, serialize_message
from ros2_pyterfaces.utils.random import random_message
from utils import TYPES, TYPES_IDS, VALUES, VALUES_IDS, assert_strictly_eq

from ros2_pyterfaces import idl


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
def test_deserialize(my_type: type[idl.IdlStruct]):
    # We cannot compare bit be bit the serialization because of padding
    ros_msg_type = my_type.get_ros_type()
    idl_from_ros = my_type.deserialize(serialize_message(ros_msg_type()))
    # easier to compare that way == doesn't work on arrays
    assert idl.message_to_plain_data(idl_from_ros) == idl.message_to_plain_data(my_type())


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
def test_serialize(my_type: type[idl.IdlStruct]):
    # We cannot compare bit be bit the serialization because of padding
    ros_msg_type = my_type.get_ros_type()
    ros_from_idl = deserialize_message(my_type().serialize(), ros_msg_type)
    # easier to compare that way == doesn't work on arrays
    assert ros_from_idl == ros_msg_type()


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
def test_deserialize_values(my_type: type[idl.IdlStruct]):
    # We cannot compare bit be bit the serialization because of padding
    for my_msg in [random_message(my_type, seed) for seed in range(10)]:
        ros_msg = my_msg.to_ros()
        idl_from_ros = my_msg.deserialize(serialize_message(ros_msg))
        assert idl.message_to_plain_data(my_msg) == idl.message_to_plain_data(idl_from_ros)


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
def test_serialize_values(my_type: type[idl.IdlStruct]):
    # We cannot compare bit be bit the serialization because of padding
    ros_msg_type = my_type.get_ros_type()
    for my_msg in [random_message(my_type, seed) for seed in range(10)]:
        ros_from_idl = deserialize_message(my_msg.serialize(), ros_msg_type)
        # assert my_msg == my_msg.from_ros(ros_from_idl)
        assert idl.message_to_plain_data(my_msg) == idl.message_to_plain_data(my_msg.from_ros(ros_from_idl))

        back_to_idl = my_msg.deserialize(serialize_message(ros_from_idl))
        # easier to compare that way == doesn't work on arrays
        assert idl.message_to_plain_data(my_msg) == idl.message_to_plain_data(back_to_idl)
