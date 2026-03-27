import pytest
from utils import (
    TYPES,
    TYPES_IDS,
    VALUES,
    VALUES_IDS,
    assert_msg_equal_as_lists,
    assert_strictly_eq,
)

from ros2_pyterfaces import idl
from ros2_pyterfaces.geometry_msgs.msg import Vector3
from ros2_pyterfaces.std_msgs.msg import Float32, Float64


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
def test_to_ros_defaults(my_type: type[idl.IdlStruct]):
    ros_msg_type = my_type.to_ros_type()
    ros_msg = my_type().to_ros()

    assert isinstance(ros_msg, ros_msg_type)
    assert_msg_equal_as_lists(ros_msg, ros_msg_type())


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
def test_from_ros_defaults(my_type: type[idl.IdlStruct]):
    ros_msg = my_type.to_ros_type()()
    idl_msg = my_type.from_ros(ros_msg)

    assert idl.message_to_plain_data(idl_msg) == idl.message_to_plain_data(my_type())


@pytest.mark.parametrize("my_msg", VALUES, ids=VALUES_IDS)
def test_to_ros_from_ros_values_roundtrip(my_msg: idl.IdlStruct):
    ros_msg = my_msg.to_ros()

    assert isinstance(ros_msg, type(my_msg).to_ros_type())
    assert idl.message_to_plain_data(
        type(my_msg).from_ros(ros_msg)
    ) == idl.message_to_plain_data(my_msg)


def test_to_ros_coerces_scalar_float_fields():
    float32_msg = Float32(data=1).to_ros()
    float64_msg = Float64(data=1).to_ros()
    vector3_msg = Vector3(1, 2, 3).to_ros()

    assert isinstance(float32_msg.data, float)
    assert isinstance(float64_msg.data, float)
    assert isinstance(vector3_msg.x, float)
    assert isinstance(vector3_msg.y, float)
    assert isinstance(vector3_msg.z, float)
