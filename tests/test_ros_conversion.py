import inspect
from typing import List, Type

import numpy as np
import pytest
from utils import assert_msg_equal_as_lists, assert_strictly_eq

from ros2_pyterfaces import all_msgs, idl
from ros2_pyterfaces.all_msgs import DiagnosticStatus, Empty, Float32, KeyValue, String
from ros2_pyterfaces.builtin_interfaces.msg import Time
from ros2_pyterfaces.geometry_msgs.msg import Quaternion, Vector3
from ros2_pyterfaces.sensor_msgs.msg import Imu, JointState
from ros2_pyterfaces.std_msgs.msg import Float64, Header

TYPES: List[Type[idl.IdlStruct]] = [
    obj
    for obj in vars(all_msgs).values()
    if inspect.isclass(obj)
    and issubclass(obj, idl.IdlStruct)
    and obj is not idl.IdlStruct
]
NOT_IN_ROS = [
    "nav_msgs/msg/Trajectory",
    "nav_msgs/msg/TrajectoryPoint",
]
TYPES = [t for t in TYPES if t.get_type_name() not in NOT_IN_ROS]

VALUES = [
    KeyValue(key="mode", value="auto"),
    String(data="hello"),
    Float32(data=np.float32(np.pi)),
    Float64(data=np.pi),
    JointState(
        header=Header(stamp=Time(1, 76)),
        name=["left", "right"],
        position=list(range(5)),
        velocity=[0.1, 0.2, 0.3],
    ),
    Empty(),
    Vector3(1, 2, 3),
    Imu(
        orientation=Quaternion(1, 0, 0, 0),
        orientation_covariance=np.full((9,), 0.1),
    ),
    DiagnosticStatus(
        level=DiagnosticStatus.WARN,
        name="status",
        message="hello",
        values=[KeyValue(key="mode", value="auto")],
    ),
]


@pytest.mark.parametrize("my_type", TYPES)
def test_to_ros_defaults(my_type: Type[idl.IdlStruct]):
    ros_msg_type = my_type.to_ros_type()
    ros_msg = my_type().to_ros()

    assert isinstance(ros_msg, ros_msg_type)
    assert_msg_equal_as_lists(ros_msg, ros_msg_type())


@pytest.mark.parametrize("my_type", TYPES)
def test_from_ros_defaults(my_type: Type[idl.IdlStruct]):
    ros_msg = my_type.to_ros_type()()
    idl_msg = my_type.from_ros(ros_msg)

    assert_strictly_eq(idl_msg, my_type())


@pytest.mark.parametrize("my_msg", VALUES)
def test_to_ros_from_ros_values_roundtrip(my_msg: idl.IdlStruct):
    ros_msg = my_msg.to_ros()

    assert isinstance(ros_msg, type(my_msg).to_ros_type())
    assert_strictly_eq(type(my_msg).from_ros(ros_msg), my_msg)


def test_to_ros_coerces_scalar_float_fields():
    float32_msg = Float32(data=1).to_ros()
    float64_msg = Float64(data=1).to_ros()
    vector3_msg = Vector3(1, 2, 3).to_ros()

    assert isinstance(float32_msg.data, float)
    assert isinstance(float64_msg.data, float)
    assert isinstance(vector3_msg.x, float)
    assert isinstance(vector3_msg.y, float)
    assert isinstance(vector3_msg.z, float)
