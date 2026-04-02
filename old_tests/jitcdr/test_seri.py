import pytest

from .utils import TYPES, TYPES_IDS, assert_strictly_eq, random_jit_message


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
def test_deserialize(my_type):
    back_to_idl = my_type.deserialize(bytes(my_type().serialize()))
    assert_strictly_eq(back_to_idl, my_type())


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
def test_serialize(my_type):
    ros_from_idl = my_type().to_ros()
    assert_strictly_eq(my_type.from_ros(ros_from_idl), my_type())


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
def test_deserialize_values(my_type):
    for my_msg in [random_jit_message(my_type, seed) for seed in range(10)]:
        back_to_idl = my_msg.deserialize(bytes(my_msg.serialize()))
        assert_strictly_eq(my_msg, back_to_idl)


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
def test_serialize_values(my_type):
    for my_msg in [random_jit_message(my_type, seed) for seed in range(10)]:
        ros_from_idl = my_msg.to_ros()
        assert_strictly_eq(my_msg, my_msg.from_ros(ros_from_idl))

        back_to_idl = my_msg.deserialize(bytes(my_msg.serialize()))
        assert_strictly_eq(my_msg, back_to_idl)
