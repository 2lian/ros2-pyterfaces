from .. import Array, BoundedString, CoreSchema, Sequence

from ..builtin_interfaces.msg import Time
from ..geometry_msgs.msg import Accel, Point, Pose, PoseStamped, PoseWithCovariance, Twist, TwistWithCovariance, Wrench
from ..std_msgs.msg import Header

Goals: CoreSchema = {
    "__typename": "nav_msgs/msg/Goals",
    "header": Header,
    "goals": Sequence(PoseStamped),
}

GridCells: CoreSchema = {
    "__typename": "nav_msgs/msg/GridCells",
    "header": Header,
    "cell_width": "float32",
    "cell_height": "float32",
    "cells": Sequence(Point),
}

MapMetaData: CoreSchema = {
    "__typename": "nav_msgs/msg/MapMetaData",
    "map_load_time": Time,
    "resolution": "float32",
    "width": "uint32",
    "height": "uint32",
    "origin": Pose,
}

Odometry: CoreSchema = {
    "__typename": "nav_msgs/msg/Odometry",
    "header": Header,
    "child_frame_id": "string",
    "pose": PoseWithCovariance,
    "twist": TwistWithCovariance,
}

Path: CoreSchema = {
    "__typename": "nav_msgs/msg/Path",
    "header": Header,
    "poses": Sequence(PoseStamped),
}

TrajectoryPoint: CoreSchema = {
    "__typename": "nav_msgs/msg/TrajectoryPoint",
    "header": Header,
    "pose": Pose,
    "velocity": Twist,
    "acceleration": Accel,
    "effort": Wrench,
}

OccupancyGrid: CoreSchema = {
    "__typename": "nav_msgs/msg/OccupancyGrid",
    "header": Header,
    "info": MapMetaData,
    "data": Sequence("int8"),
}

Trajectory: CoreSchema = {
    "__typename": "nav_msgs/msg/Trajectory",
    "header": Header,
    "points": Sequence(TrajectoryPoint),
}

__all__ = [
    "Goals",
    "GridCells",
    "MapMetaData",
    "Odometry",
    "Path",
    "TrajectoryPoint",
    "OccupancyGrid",
    "Trajectory",
]
