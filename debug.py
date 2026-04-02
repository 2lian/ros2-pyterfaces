from pprint import pprint
from typing import Any, ClassVar, Literal

import msgspec
import numpy as np
from nptyping import Bytes, Float64, NDArray, Shape

from ros2_pyterfaces.jitcdr import idl
from ros2_pyterfaces.jitcdr.idl import JitStruct as Struct


class Time(Struct):
    __idl_typename__: ClassVar[Literal["builtin_interfaces/msg/Time"]] = (
        "builtin_interfaces/msg/Time"
    )
    sec: np.int32 = np.int32(0)
    nanosec: np.uint32 = np.uint32(0)


class Header(Struct):
    __idl_typename__: ClassVar[Literal["std_msgs/msg/Header"]] = "std_msgs/msg/Header"
    stamp: Time = msgspec.field(default_factory=Time)
    frame_id: bytes = b""


class JointState(Struct):
    __idl_typename__: ClassVar[Literal["sensor_msgs/msg/JointState"]] = (
        "sensor_msgs/msg/JointState"
    )
    header: Header = msgspec.field(default_factory=Header)
    name: NDArray[Any, Bytes] = msgspec.field(
        default_factory=lambda: np.empty(0, Bytes)
    )
    position: NDArray[Any, Float64] = msgspec.field(
        default_factory=lambda: np.empty(0, Float64)
    )
    velocity: NDArray[Any, Float64] = msgspec.field(
        default_factory=lambda: np.empty(0, Float64)
    )
    effort: NDArray[Any, Float64] = msgspec.field(
        default_factory=lambda: np.empty(0, Float64)
    )


my_msg: JointState = JointState(
    header=Header(
        stamp=Time(sec=np.int32(17000), nanosec=np.uint32(1234)),
        frame_id=b"base_link",
    ),
    name=np.array([b"joint_a", b"joint_b", b"joint_c"]),
    position=np.array([0.5, 1.5, 2.5], dtype=np.float64),
)

# serialization
blob_bytes: bytearray = my_msg.serialize()
pprint(blob_bytes)
my_msg_again: JointState = JointState.deserialize(blob_bytes)
pprint(my_msg_again)

# ROS 2 metadata
json_type_description = JointState.json_type_description()
pprint(json_type_description)
ros_hash = JointState.hash_rihs01()

# ROS 2 conversion
ros_msg_type = JointState.to_ros_type()
ros_msg = my_msg.to_ros()
our_msg: JointState = JointState.from_ros(ros_msg)
