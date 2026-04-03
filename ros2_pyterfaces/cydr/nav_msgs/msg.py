from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..builtin_interfaces.msg import Time
from ..geometry_msgs.msg import Accel, Point, Pose, PoseStamped, PoseWithCovariance, Twist, TwistWithCovariance, Wrench
from ..std_msgs.msg import Header

class Goals(JitStruct):
    __idl_typename__ = 'nav_msgs/msg/Goals'
    __unsupported_reason__ = 'goals is a collection of messages, which cydr does not support'
    pass

class GridCells(JitStruct):
    __idl_typename__ = 'nav_msgs/msg/GridCells'
    __unsupported_reason__ = 'cells is a collection of messages, which cydr does not support'
    pass

class MapMetaData(JitStruct):
    __idl_typename__ = 'nav_msgs/msg/MapMetaData'
    map_load_time: Time = msgspec.field(default_factory=Time)
    resolution: types.float32 = np.float32(0.0)
    width: types.uint32 = np.uint32(0)
    height: types.uint32 = np.uint32(0)
    origin: Pose = msgspec.field(default_factory=Pose)

class Odometry(JitStruct):
    __idl_typename__ = 'nav_msgs/msg/Odometry'
    header: Header = msgspec.field(default_factory=Header)
    child_frame_id: types.string = b''
    pose: PoseWithCovariance = msgspec.field(default_factory=PoseWithCovariance)
    twist: TwistWithCovariance = msgspec.field(default_factory=TwistWithCovariance)

class Path(JitStruct):
    __idl_typename__ = 'nav_msgs/msg/Path'
    __unsupported_reason__ = 'poses is a collection of messages, which cydr does not support'
    pass

class TrajectoryPoint(JitStruct):
    __idl_typename__ = 'nav_msgs/msg/TrajectoryPoint'
    header: Header = msgspec.field(default_factory=Header)
    pose: Pose = msgspec.field(default_factory=Pose)
    velocity: Twist = msgspec.field(default_factory=Twist)
    acceleration: Accel = msgspec.field(default_factory=Accel)
    effort: Wrench = msgspec.field(default_factory=Wrench)

class OccupancyGrid(JitStruct):
    __idl_typename__ = 'nav_msgs/msg/OccupancyGrid'
    header: Header = msgspec.field(default_factory=Header)
    info: MapMetaData = msgspec.field(default_factory=MapMetaData)
    data: types.NDArray[Any, types.Int8] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.int8))

class Trajectory(JitStruct):
    __idl_typename__ = 'nav_msgs/msg/Trajectory'
    __unsupported_reason__ = 'points is a collection of messages, which cydr does not support'
    pass
