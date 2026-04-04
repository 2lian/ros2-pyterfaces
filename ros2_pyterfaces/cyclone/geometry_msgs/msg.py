from dataclasses import dataclass, field

import numpy as np

from ..idl import IdlStruct, types
from ..std_msgs.msg import Header


@dataclass
class Point(IdlStruct, typename="geometry_msgs/msg/Point"):
    x: types.float64 = 0.0
    y: types.float64 = 0.0
    z: types.float64 = 0.0


@dataclass
class Point32(IdlStruct, typename="geometry_msgs/msg/Point32"):
    x: types.float32 = 0.0
    y: types.float32 = 0.0
    z: types.float32 = 0.0


@dataclass
class Quaternion(IdlStruct, typename="geometry_msgs/msg/Quaternion"):
    x: types.float64 = 0.0
    y: types.float64 = 0.0
    z: types.float64 = 0.0
    w: types.float64 = 1.0


@dataclass
class Vector3(IdlStruct, typename="geometry_msgs/msg/Vector3"):
    x: types.float64 = 0.0
    y: types.float64 = 0.0
    z: types.float64 = 0.0


@dataclass
class Accel(IdlStruct, typename="geometry_msgs/msg/Accel"):
    linear: Vector3 = field(default_factory=Vector3)
    angular: Vector3 = field(default_factory=Vector3)


@dataclass
class Inertia(IdlStruct, typename="geometry_msgs/msg/Inertia"):
    m: types.float64 = 0.0
    com: Vector3 = field(default_factory=Vector3)
    ixx: types.float64 = 0.0
    ixy: types.float64 = 0.0
    ixz: types.float64 = 0.0
    iyy: types.float64 = 0.0
    iyz: types.float64 = 0.0
    izz: types.float64 = 0.0


@dataclass
class PointStamped(IdlStruct, typename="geometry_msgs/msg/PointStamped"):
    header: Header = field(default_factory=Header)
    point: Point = field(default_factory=Point)


@dataclass
class Polygon(IdlStruct, typename="geometry_msgs/msg/Polygon"):
    points: types.sequence[Point32] = field(default_factory=list)


@dataclass
class Pose(IdlStruct, typename="geometry_msgs/msg/Pose"):
    position: Point = field(default_factory=Point)
    orientation: Quaternion = field(default_factory=Quaternion)


@dataclass
class QuaternionStamped(IdlStruct, typename="geometry_msgs/msg/QuaternionStamped"):
    header: Header = field(default_factory=Header)
    quaternion: Quaternion = field(default_factory=Quaternion)


@dataclass
class Transform(IdlStruct, typename="geometry_msgs/msg/Transform"):
    translation: Vector3 = field(default_factory=Vector3)
    rotation: Quaternion = field(default_factory=Quaternion)


@dataclass
class Twist(IdlStruct, typename="geometry_msgs/msg/Twist"):
    linear: Vector3 = field(default_factory=Vector3)
    angular: Vector3 = field(default_factory=Vector3)


@dataclass
class Vector3Stamped(IdlStruct, typename="geometry_msgs/msg/Vector3Stamped"):
    header: Header = field(default_factory=Header)
    vector: Vector3 = field(default_factory=Vector3)


@dataclass
class Wrench(IdlStruct, typename="geometry_msgs/msg/Wrench"):
    force: Vector3 = field(default_factory=Vector3)
    torque: Vector3 = field(default_factory=Vector3)


@dataclass
class AccelStamped(IdlStruct, typename="geometry_msgs/msg/AccelStamped"):
    header: Header = field(default_factory=Header)
    accel: Accel = field(default_factory=Accel)


@dataclass
class AccelWithCovariance(IdlStruct, typename="geometry_msgs/msg/AccelWithCovariance"):
    accel: Accel = field(default_factory=Accel)
    covariance: types.array[types.float64, 36] = field(
        default_factory=lambda: np.zeros(36)
    )


@dataclass
class InertiaStamped(IdlStruct, typename="geometry_msgs/msg/InertiaStamped"):
    header: Header = field(default_factory=Header)
    inertia: Inertia = field(default_factory=Inertia)


@dataclass
class PolygonInstance(IdlStruct, typename="geometry_msgs/msg/PolygonInstance"):
    polygon: Polygon = field(default_factory=Polygon)
    id: types.int64 = 0


@dataclass
class PolygonStamped(IdlStruct, typename="geometry_msgs/msg/PolygonStamped"):
    header: Header = field(default_factory=Header)
    polygon: Polygon = field(default_factory=Polygon)


@dataclass
class PoseArray(IdlStruct, typename="geometry_msgs/msg/PoseArray"):
    header: Header = field(default_factory=Header)
    poses: types.sequence[Pose] = field(default_factory=list)


@dataclass
class PoseStamped(IdlStruct, typename="geometry_msgs/msg/PoseStamped"):
    header: Header = field(default_factory=Header)
    pose: Pose = field(default_factory=Pose)


@dataclass
class PoseWithCovariance(IdlStruct, typename="geometry_msgs/msg/PoseWithCovariance"):
    pose: Pose = field(default_factory=Pose)
    covariance: types.array[types.float64, 36] = field(
        default_factory=lambda: np.zeros(36)
    )


@dataclass
class TransformStamped(IdlStruct, typename="geometry_msgs/msg/TransformStamped"):
    header: Header = field(default_factory=Header)
    child_frame_id: str = ""
    transform: Transform = field(default_factory=Transform)


@dataclass
class TwistStamped(IdlStruct, typename="geometry_msgs/msg/TwistStamped"):
    header: Header = field(default_factory=Header)
    twist: Twist = field(default_factory=Twist)


@dataclass
class TwistWithCovariance(IdlStruct, typename="geometry_msgs/msg/TwistWithCovariance"):
    twist: Twist = field(default_factory=Twist)
    covariance: types.array[types.float64, 36] = field(
        default_factory=lambda: np.zeros(36)
    )


@dataclass
class VelocityStamped(IdlStruct, typename="geometry_msgs/msg/VelocityStamped"):
    header: Header = field(default_factory=Header)
    body_frame_id: str = ""
    reference_frame_id: str = ""
    velocity: Twist = field(default_factory=Twist)


@dataclass
class WrenchStamped(IdlStruct, typename="geometry_msgs/msg/WrenchStamped"):
    header: Header = field(default_factory=Header)
    wrench: Wrench = field(default_factory=Wrench)


@dataclass
class AccelWithCovarianceStamped(
    IdlStruct, typename="geometry_msgs/msg/AccelWithCovarianceStamped"
):
    header: Header = field(default_factory=Header)
    accel: AccelWithCovariance = field(default_factory=AccelWithCovariance)


@dataclass
class PolygonInstanceStamped(
    IdlStruct, typename="geometry_msgs/msg/PolygonInstanceStamped"
):
    header: Header = field(default_factory=Header)
    polygon: PolygonInstance = field(default_factory=PolygonInstance)


@dataclass
class PoseWithCovarianceStamped(
    IdlStruct, typename="geometry_msgs/msg/PoseWithCovarianceStamped"
):
    header: Header = field(default_factory=Header)
    pose: PoseWithCovariance = field(default_factory=PoseWithCovariance)


@dataclass
class TwistWithCovarianceStamped(
    IdlStruct, typename="geometry_msgs/msg/TwistWithCovarianceStamped"
):
    header: Header = field(default_factory=Header)
    twist: TwistWithCovariance = field(default_factory=TwistWithCovariance)
