from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import IdlStruct
from ..std_msgs.msg import Header

class Point(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Point'
    x: types.float64 = np.float64(0.0)
    y: types.float64 = np.float64(0.0)
    z: types.float64 = np.float64(0.0)

class Point32(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Point32'
    x: types.float32 = np.float32(0.0)
    y: types.float32 = np.float32(0.0)
    z: types.float32 = np.float32(0.0)

class Quaternion(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Quaternion'
    x: types.float64 = np.float64(0.0)
    y: types.float64 = np.float64(0.0)
    z: types.float64 = np.float64(0.0)
    w: types.float64 = np.float64(1.0)

class Vector3(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Vector3'
    x: types.float64 = np.float64(0.0)
    y: types.float64 = np.float64(0.0)
    z: types.float64 = np.float64(0.0)

class Accel(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Accel'
    linear: Vector3 = msgspec.field(default_factory=Vector3)
    angular: Vector3 = msgspec.field(default_factory=Vector3)

class Inertia(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Inertia'
    m: types.float64 = np.float64(0.0)
    com: Vector3 = msgspec.field(default_factory=Vector3)
    ixx: types.float64 = np.float64(0.0)
    ixy: types.float64 = np.float64(0.0)
    ixz: types.float64 = np.float64(0.0)
    iyy: types.float64 = np.float64(0.0)
    iyz: types.float64 = np.float64(0.0)
    izz: types.float64 = np.float64(0.0)

class PointStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/PointStamped'
    header: Header = msgspec.field(default_factory=Header)
    point: Point = msgspec.field(default_factory=Point)

class Polygon(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Polygon'
    __unsupported_reason__ = 'points is a collection of messages, which cydr does not support'
    pass

class Pose(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Pose'
    position: Point = msgspec.field(default_factory=Point)
    orientation: Quaternion = msgspec.field(default_factory=Quaternion)

class QuaternionStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/QuaternionStamped'
    header: Header = msgspec.field(default_factory=Header)
    quaternion: Quaternion = msgspec.field(default_factory=Quaternion)

class Transform(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Transform'
    translation: Vector3 = msgspec.field(default_factory=Vector3)
    rotation: Quaternion = msgspec.field(default_factory=Quaternion)

class Twist(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Twist'
    linear: Vector3 = msgspec.field(default_factory=Vector3)
    angular: Vector3 = msgspec.field(default_factory=Vector3)

class Vector3Stamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Vector3Stamped'
    header: Header = msgspec.field(default_factory=Header)
    vector: Vector3 = msgspec.field(default_factory=Vector3)

class Wrench(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/Wrench'
    force: Vector3 = msgspec.field(default_factory=Vector3)
    torque: Vector3 = msgspec.field(default_factory=Vector3)

class AccelStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/AccelStamped'
    header: Header = msgspec.field(default_factory=Header)
    accel: Accel = msgspec.field(default_factory=Accel)

class AccelWithCovariance(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/AccelWithCovariance'
    accel: Accel = msgspec.field(default_factory=Accel)
    covariance: types.NDArray[types.Shape["36"], types.Float64] = msgspec.field(default_factory=lambda: np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64))

class InertiaStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/InertiaStamped'
    header: Header = msgspec.field(default_factory=Header)
    inertia: Inertia = msgspec.field(default_factory=Inertia)

class PolygonInstance(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/PolygonInstance'
    __unsupported_reason__ = 'polygon references unsupported message Polygon'
    polygon: Polygon = msgspec.field(default_factory=Polygon)
    id: types.int64 = np.int64(0)

class PolygonStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/PolygonStamped'
    __unsupported_reason__ = 'polygon references unsupported message Polygon'
    header: Header = msgspec.field(default_factory=Header)
    polygon: Polygon = msgspec.field(default_factory=Polygon)

class PoseArray(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/PoseArray'
    __unsupported_reason__ = 'poses is a collection of messages, which cydr does not support'
    pass

class PoseStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/PoseStamped'
    header: Header = msgspec.field(default_factory=Header)
    pose: Pose = msgspec.field(default_factory=Pose)

class PoseWithCovariance(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/PoseWithCovariance'
    pose: Pose = msgspec.field(default_factory=Pose)
    covariance: types.NDArray[types.Shape["36"], types.Float64] = msgspec.field(default_factory=lambda: np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64))

class TransformStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/TransformStamped'
    header: Header = msgspec.field(default_factory=Header)
    child_frame_id: types.string = b''
    transform: Transform = msgspec.field(default_factory=Transform)

class TwistStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/TwistStamped'
    header: Header = msgspec.field(default_factory=Header)
    twist: Twist = msgspec.field(default_factory=Twist)

class TwistWithCovariance(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/TwistWithCovariance'
    twist: Twist = msgspec.field(default_factory=Twist)
    covariance: types.NDArray[types.Shape["36"], types.Float64] = msgspec.field(default_factory=lambda: np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64))

class VelocityStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/VelocityStamped'
    header: Header = msgspec.field(default_factory=Header)
    body_frame_id: types.string = b''
    reference_frame_id: types.string = b''
    velocity: Twist = msgspec.field(default_factory=Twist)

class WrenchStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/WrenchStamped'
    header: Header = msgspec.field(default_factory=Header)
    wrench: Wrench = msgspec.field(default_factory=Wrench)

class AccelWithCovarianceStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/AccelWithCovarianceStamped'
    header: Header = msgspec.field(default_factory=Header)
    accel: AccelWithCovariance = msgspec.field(default_factory=AccelWithCovariance)

class PolygonInstanceStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/PolygonInstanceStamped'
    __unsupported_reason__ = 'polygon references unsupported message PolygonInstance'
    header: Header = msgspec.field(default_factory=Header)
    polygon: PolygonInstance = msgspec.field(default_factory=PolygonInstance)

class PoseWithCovarianceStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/PoseWithCovarianceStamped'
    header: Header = msgspec.field(default_factory=Header)
    pose: PoseWithCovariance = msgspec.field(default_factory=PoseWithCovariance)

class TwistWithCovarianceStamped(IdlStruct):
    __idl_typename__ = 'geometry_msgs/msg/TwistWithCovarianceStamped'
    header: Header = msgspec.field(default_factory=Header)
    twist: TwistWithCovariance = msgspec.field(default_factory=TwistWithCovariance)
