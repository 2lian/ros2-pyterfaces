from .. import Array, BoundedString, CoreSchema, Sequence

from ..builtin_interfaces.msg import Duration
from ..geometry_msgs.msg import Transform, Twist
from ..std_msgs.msg import Header

JointTrajectoryPoint: CoreSchema = {
    "__typename": "trajectory_msgs/msg/JointTrajectoryPoint",
    "positions": Sequence("float64"),
    "velocities": Sequence("float64"),
    "accelerations": Sequence("float64"),
    "effort": Sequence("float64"),
    "time_from_start": Duration,
}

MultiDOFJointTrajectoryPoint: CoreSchema = {
    "__typename": "trajectory_msgs/msg/MultiDOFJointTrajectoryPoint",
    "transforms": Sequence(Transform),
    "velocities": Sequence(Twist),
    "accelerations": Sequence(Twist),
    "time_from_start": Duration,
}

JointTrajectory: CoreSchema = {
    "__typename": "trajectory_msgs/msg/JointTrajectory",
    "header": Header,
    "joint_names": Sequence("string"),
    "points": Sequence(JointTrajectoryPoint),
}

MultiDOFJointTrajectory: CoreSchema = {
    "__typename": "trajectory_msgs/msg/MultiDOFJointTrajectory",
    "header": Header,
    "joint_names": Sequence("string"),
    "points": Sequence(MultiDOFJointTrajectoryPoint),
}

__all__ = [
    "JointTrajectoryPoint",
    "MultiDOFJointTrajectoryPoint",
    "JointTrajectory",
    "MultiDOFJointTrajectory",
]
