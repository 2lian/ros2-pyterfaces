from dataclasses import dataclass, field
from ..idl import IdlStruct, types
from ..std_msgs.msg import Header
from ..builtin_interfaces.msg import Duration
from ..geometry_msgs.msg import Transform, Twist

@dataclass
class JointTrajectoryPoint(IdlStruct, typename="trajectory_msgs/msg/JointTrajectoryPoint"):
    positions: types.sequence[types.float64] = field(default_factory=list)
    velocities: types.sequence[types.float64] = field(default_factory=list)
    accelerations: types.sequence[types.float64] = field(default_factory=list)
    effort: types.sequence[types.float64] = field(default_factory=list)
    time_from_start: Duration = field(default_factory=Duration)


@dataclass
class MultiDOFJointTrajectoryPoint(IdlStruct, typename="trajectory_msgs/msg/MultiDOFJointTrajectoryPoint"):
    transforms: types.sequence[Transform] = field(default_factory=list)
    velocities: types.sequence[Twist] = field(default_factory=list)
    accelerations: types.sequence[Twist] = field(default_factory=list)
    time_from_start: Duration = field(default_factory=Duration)


@dataclass
class JointTrajectory(IdlStruct, typename="trajectory_msgs/msg/JointTrajectory"):
    header: Header = field(default_factory=Header)
    joint_names: types.sequence[str] = field(default_factory=list)
    points: types.sequence[JointTrajectoryPoint] = field(default_factory=list)


@dataclass
class MultiDOFJointTrajectory(IdlStruct, typename="trajectory_msgs/msg/MultiDOFJointTrajectory"):
    header: Header = field(default_factory=Header)
    joint_names: types.sequence[str] = field(default_factory=list)
    points: types.sequence[MultiDOFJointTrajectoryPoint] = field(default_factory=list)
