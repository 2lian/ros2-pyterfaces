from dataclasses import dataclass, field
from typing import Literal

from ..geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from ..idl import IdlService, IdlStruct, types
from ..nav_msgs.msg import OccupancyGrid, Path

__all__ = [
    "GetMap",
    "GetMap_Request",
    "GetMap_Response",
    "GetPlan",
    "GetPlan_Request",
    "GetPlan_Response",
    "LoadMap",
    "LoadMap_Request",
    "LoadMap_Response",
    "SetMap",
    "SetMap_Request",
    "SetMap_Response",
]


@dataclass
class GetMap_Request(IdlStruct, typename="nav_msgs/srv/GetMap_Request"):
    pass


@dataclass
class GetMap_Response(IdlStruct, typename="nav_msgs/srv/GetMap_Response"):
    map: OccupancyGrid = field(default_factory=OccupancyGrid)


class GetMap(IdlService, typename="nav_msgs/srv/GetMap"):
    Request = GetMap_Request
    Response = GetMap_Response


@dataclass
class GetPlan_Request(IdlStruct, typename="nav_msgs/srv/GetPlan_Request"):
    start: PoseStamped = field(default_factory=PoseStamped)
    goal: PoseStamped = field(default_factory=PoseStamped)
    tolerance: types.float32 = 0.0


@dataclass
class GetPlan_Response(IdlStruct, typename="nav_msgs/srv/GetPlan_Response"):
    plan: Path = field(default_factory=Path)


class GetPlan(IdlService, typename="nav_msgs/srv/GetPlan"):
    Request = GetPlan_Request
    Response = GetPlan_Response


@dataclass
class LoadMap_Request(IdlStruct, typename="nav_msgs/srv/LoadMap_Request"):
    map_url: str = ""


@dataclass
class LoadMap_Response(IdlStruct, typename="nav_msgs/srv/LoadMap_Response"):
    RESULT_SUCCESS: Literal[0] = 0
    RESULT_MAP_DOES_NOT_EXIST: Literal[1] = 1
    RESULT_INVALID_MAP_DATA: Literal[2] = 2
    RESULT_INVALID_MAP_METADATA: Literal[3] = 3
    RESULT_UNDEFINED_FAILURE: Literal[255] = 255
    map: OccupancyGrid = field(default_factory=OccupancyGrid)
    result: types.uint8 = 0


class LoadMap(IdlService, typename="nav_msgs/srv/LoadMap"):
    Request = LoadMap_Request
    Response = LoadMap_Response


@dataclass
class SetMap_Request(IdlStruct, typename="nav_msgs/srv/SetMap_Request"):
    map: OccupancyGrid = field(default_factory=OccupancyGrid)
    initial_pose: PoseWithCovarianceStamped = field(
        default_factory=PoseWithCovarianceStamped
    )


@dataclass
class SetMap_Response(IdlStruct, typename="nav_msgs/srv/SetMap_Response"):
    success: bool = False


class SetMap(IdlService, typename="nav_msgs/srv/SetMap"):
    Request = SetMap_Request
    Response = SetMap_Response
