from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ros2_pyterfaces.cydr.idl import IdlStruct


class Time(IdlStruct):
    __idl_typename__ = "builtin_interfaces/msg/Time"
    sec: types.int32 = np.int32(0)
    nanosec: types.uint32 = np.uint32(0)


class Header(IdlStruct):
    __idl_typename__ = "std_msgs/msg/Header"
    stamp: Time = msgspec.field(default_factory=Time)
    frame_id: types.string = b""


class JointState(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/JointState"
    header: Header = msgspec.field(default_factory=Header)
    name: types.NDArray[Any, types.Bytes] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.bytes_)
    )
    position: types.NDArray[Any, types.Float64] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float64)
    )
    velocity: types.NDArray[Any, types.Float64] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float64)
    )
    effort: types.NDArray[Any, types.Float64] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float64)
    )


my_msg: JointState = JointState(
    header=Header(
        stamp=Time(sec=np.int32(1), nanosec=np.uint32(2)),
        frame_id=b"base_link",
    ),
    name=np.array([b"joint_1", b"joint_2"], dtype=np.bytes_),
    position=np.array([1.0, 2.0], dtype=np.float64),
    velocity=np.array([0.1, 0.2], dtype=np.float64),
    effort=np.array([0.0, 0.0], dtype=np.float64),
)

# serialization
blob_bytes: bytearray = my_msg.serialize()
my_msg_again: JointState = JointState.deserialize(blob_bytes)

# ROS 2 metadata
json_type_description = JointState.json_type_description()
ros_hash = JointState.hash_rihs01()

# ROS 2 conversion
ros_msg_type = JointState.to_ros_type()
ros_msg = my_msg.to_ros()
our_msg: JointState = JointState.from_ros(ros_msg)
