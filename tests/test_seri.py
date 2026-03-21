import inspect
from importlib import import_module
from typing import List, Tuple, Type

import numpy as np
import pytest
from rclpy.serialization import deserialize_message, serialize_message
from utils import assert_strictly_eq

from ros2_pyterfaces import all_msgs, idl
from ros2_pyterfaces.all_msgs import (
    Char,
    DiagnosticStatus,
    Empty,
    Float32,
    Imu,
    JointState,
    KeyValue,
    String,
    Trajectory,
    TrajectoryPoint,
)
from ros2_pyterfaces.builtin_interfaces.msg import Time
from ros2_pyterfaces.geometry_msgs.msg import Quaternion
from ros2_pyterfaces.std_msgs.msg import Float64, Header

TYPES: List[Type[idl.IdlStruct]] = [
    obj
    for obj in vars(all_msgs).values()
    if inspect.isclass(obj)
    and issubclass(obj, idl.IdlStruct)
    and obj is not idl.IdlStruct
]
NOT_IN_ROS = [
    # not in ROS yet
    "nav_msgs/msg/Trajectory",
    "nav_msgs/msg/TrajectoryPoint",
]
TYPES = [t for t in TYPES if t.get_type_name() not in NOT_IN_ROS]
# TYPES = [Empty, KeyValue, JointState, Char, Imu]


@pytest.mark.parametrize("my_type", TYPES)
def test_deserialize(my_type: Type[idl.IdlStruct]):
    # We cannot compare bit be bit the serialization because of padding
    ros_msg_type = my_type.get_ros_type()
    idl_from_ros = my_type.deserialize(serialize_message(ros_msg_type()))
    # easier to compare that way == doesn't work on arrays
    assert_strictly_eq(idl_from_ros, my_type())


@pytest.mark.parametrize("my_type", TYPES)
def test_serialize(my_type: Type[idl.IdlStruct]):
    # We cannot compare bit be bit the serialization because of padding
    ros_msg_type = my_type.get_ros_type()
    ros_from_idl = deserialize_message(my_type().serialize(), ros_msg_type)
    # easier to compare that way == doesn't work on arrays
    assert ros_from_idl == ros_msg_type()


VALUES = [
    String(data="hello"),
    Char(3),
    Float32(np.float32(np.pi)),
    Float64(np.pi),
    JointState(
        header=Header(stamp=Time(1, 76)),
        position=list(range(100)),
        velocity=list(range(100)),
    ),
    Empty(),
    Imu(orientation=Quaternion(1, 0, 0, 0), orientation_covariance=np.full((9,), 0.1)),
    DiagnosticStatus(
        level=DiagnosticStatus.WARN,
        name="hey",
        message="hello",
        values=[KeyValue(key="heyyo", value="yey")],
    ),
]


@pytest.mark.parametrize("my_msg", VALUES)
def test_serialize_values(my_msg: idl.IdlStruct):
    # We cannot compare bit be bit the serialization because of padding
    ros_msg_type = my_msg.get_ros_type()
    ros_from_idl = deserialize_message(my_msg.serialize(), ros_msg_type)
    # assert my_msg == my_msg.from_ros(ros_from_idl)
    assert_strictly_eq(my_msg, my_msg.from_ros(ros_from_idl))

    back_to_idl = my_msg.deserialize(serialize_message(ros_from_idl))
    # easier to compare that way == doesn't work on arrays
    assert_strictly_eq(my_msg, back_to_idl)
