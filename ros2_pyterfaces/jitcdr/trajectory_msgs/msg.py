from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..builtin_interfaces.msg import Duration
from ..geometry_msgs.msg import Transform, Twist
from ..std_msgs.msg import Header

class JointTrajectoryPoint(JitStruct):
    __idl_typename__ = 'trajectory_msgs/msg/JointTrajectoryPoint'
    positions: types.NDArray[Any, types.Float64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.float64))
    velocities: types.NDArray[Any, types.Float64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.float64))
    accelerations: types.NDArray[Any, types.Float64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.float64))
    effort: types.NDArray[Any, types.Float64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.float64))
    time_from_start: Duration = msgspec.field(default_factory=Duration)

class MultiDOFJointTrajectoryPoint(JitStruct):
    __idl_typename__ = 'trajectory_msgs/msg/MultiDOFJointTrajectoryPoint'
    __unsupported_reason__ = 'transforms is a collection of messages, which cydr does not support'
    pass

class JointTrajectory(JitStruct):
    __idl_typename__ = 'trajectory_msgs/msg/JointTrajectory'
    __unsupported_reason__ = 'points is a collection of messages, which cydr does not support'
    pass

class MultiDOFJointTrajectory(JitStruct):
    __idl_typename__ = 'trajectory_msgs/msg/MultiDOFJointTrajectory'
    __unsupported_reason__ = 'points is a collection of messages, which cydr does not support'
    pass
