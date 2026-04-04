from .. import Array, BoundedString, CoreSchema, Sequence

from ..std_msgs.msg import Header

Point: CoreSchema = {
    "__typename": "geometry_msgs/msg/Point",
    "x": "float64",
    "y": "float64",
    "z": "float64",
}

Point32: CoreSchema = {
    "__typename": "geometry_msgs/msg/Point32",
    "x": "float32",
    "y": "float32",
    "z": "float32",
}

Quaternion: CoreSchema = {
    "__typename": "geometry_msgs/msg/Quaternion",
    "x": "float64",
    "y": "float64",
    "z": "float64",
    "w": "float64",
}

Vector3: CoreSchema = {
    "__typename": "geometry_msgs/msg/Vector3",
    "x": "float64",
    "y": "float64",
    "z": "float64",
}

PointStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/PointStamped",
    "header": Header,
    "point": Point,
}

Polygon: CoreSchema = {
    "__typename": "geometry_msgs/msg/Polygon",
    "points": Sequence(Point32),
}

Pose: CoreSchema = {
    "__typename": "geometry_msgs/msg/Pose",
    "position": Point,
    "orientation": Quaternion,
}

QuaternionStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/QuaternionStamped",
    "header": Header,
    "quaternion": Quaternion,
}

Accel: CoreSchema = {
    "__typename": "geometry_msgs/msg/Accel",
    "linear": Vector3,
    "angular": Vector3,
}

Inertia: CoreSchema = {
    "__typename": "geometry_msgs/msg/Inertia",
    "m": "float64",
    "com": Vector3,
    "ixx": "float64",
    "ixy": "float64",
    "ixz": "float64",
    "iyy": "float64",
    "iyz": "float64",
    "izz": "float64",
}

Transform: CoreSchema = {
    "__typename": "geometry_msgs/msg/Transform",
    "translation": Vector3,
    "rotation": Quaternion,
}

Twist: CoreSchema = {
    "__typename": "geometry_msgs/msg/Twist",
    "linear": Vector3,
    "angular": Vector3,
}

Vector3Stamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/Vector3Stamped",
    "header": Header,
    "vector": Vector3,
}

Wrench: CoreSchema = {
    "__typename": "geometry_msgs/msg/Wrench",
    "force": Vector3,
    "torque": Vector3,
}

PolygonInstance: CoreSchema = {
    "__typename": "geometry_msgs/msg/PolygonInstance",
    "polygon": Polygon,
    "id": "int64",
}

PolygonStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/PolygonStamped",
    "header": Header,
    "polygon": Polygon,
}

PoseArray: CoreSchema = {
    "__typename": "geometry_msgs/msg/PoseArray",
    "header": Header,
    "poses": Sequence(Pose),
}

PoseStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/PoseStamped",
    "header": Header,
    "pose": Pose,
}

PoseWithCovariance: CoreSchema = {
    "__typename": "geometry_msgs/msg/PoseWithCovariance",
    "pose": Pose,
    "covariance": Array("float64", 36),
}

AccelStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/AccelStamped",
    "header": Header,
    "accel": Accel,
}

AccelWithCovariance: CoreSchema = {
    "__typename": "geometry_msgs/msg/AccelWithCovariance",
    "accel": Accel,
    "covariance": Array("float64", 36),
}

InertiaStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/InertiaStamped",
    "header": Header,
    "inertia": Inertia,
}

TransformStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/TransformStamped",
    "header": Header,
    "child_frame_id": "string",
    "transform": Transform,
}

TwistStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/TwistStamped",
    "header": Header,
    "twist": Twist,
}

TwistWithCovariance: CoreSchema = {
    "__typename": "geometry_msgs/msg/TwistWithCovariance",
    "twist": Twist,
    "covariance": Array("float64", 36),
}

VelocityStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/VelocityStamped",
    "header": Header,
    "body_frame_id": "string",
    "reference_frame_id": "string",
    "velocity": Twist,
}

WrenchStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/WrenchStamped",
    "header": Header,
    "wrench": Wrench,
}

PolygonInstanceStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/PolygonInstanceStamped",
    "header": Header,
    "polygon": PolygonInstance,
}

PoseWithCovarianceStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/PoseWithCovarianceStamped",
    "header": Header,
    "pose": PoseWithCovariance,
}

AccelWithCovarianceStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/AccelWithCovarianceStamped",
    "header": Header,
    "accel": AccelWithCovariance,
}

TwistWithCovarianceStamped: CoreSchema = {
    "__typename": "geometry_msgs/msg/TwistWithCovarianceStamped",
    "header": Header,
    "twist": TwistWithCovariance,
}

__all__ = [
    "Point",
    "Point32",
    "Quaternion",
    "Vector3",
    "PointStamped",
    "Polygon",
    "Pose",
    "QuaternionStamped",
    "Accel",
    "Inertia",
    "Transform",
    "Twist",
    "Vector3Stamped",
    "Wrench",
    "PolygonInstance",
    "PolygonStamped",
    "PoseArray",
    "PoseStamped",
    "PoseWithCovariance",
    "AccelStamped",
    "AccelWithCovariance",
    "InertiaStamped",
    "TransformStamped",
    "TwistStamped",
    "TwistWithCovariance",
    "VelocityStamped",
    "WrenchStamped",
    "PolygonInstanceStamped",
    "PoseWithCovarianceStamped",
    "AccelWithCovarianceStamped",
    "TwistWithCovarianceStamped",
]
