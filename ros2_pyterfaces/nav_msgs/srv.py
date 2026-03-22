from dataclasses import dataclass, field
from typing import Literal

from .. import idl
from ..geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from ..nav_msgs.msg import OccupancyGrid, Path
from ..service_msgs.msg import ServiceEventInfo

@dataclass
class GetMap_Request(idl.IdlStruct, typename="nav_msgs/srv/GetMap_Request"):
    pass


@dataclass
class GetMap_Response(idl.IdlStruct, typename="nav_msgs/srv/GetMap_Response"):
    map: OccupancyGrid = field(default_factory=OccupancyGrid)


@dataclass
class GetMap_Event(
    idl.IdlStruct,
    typename="nav_msgs/srv/GetMap_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[GetMap_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[GetMap_Response, 1] = field(default_factory=list)


@dataclass
class GetMap(
    idl.IdlServiceStruct,
    typename="nav_msgs/srv/GetMap",
):
    request_message: GetMap_Request = field(default_factory=GetMap_Request)
    response_message: GetMap_Response = field(default_factory=GetMap_Response)
    event_message: GetMap_Event = field(default_factory=GetMap_Event)


@dataclass
class GetPlan_Request(idl.IdlStruct, typename="nav_msgs/srv/GetPlan_Request"):
    start: PoseStamped = field(default_factory=PoseStamped)
    goal: PoseStamped = field(default_factory=PoseStamped)
    tolerance: idl.types.float32 = 0.0


@dataclass
class GetPlan_Response(idl.IdlStruct, typename="nav_msgs/srv/GetPlan_Response"):
    plan: Path = field(default_factory=Path)


@dataclass
class GetPlan_Event(
    idl.IdlStruct,
    typename="nav_msgs/srv/GetPlan_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[GetPlan_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[GetPlan_Response, 1] = field(default_factory=list)


@dataclass
class GetPlan(
    idl.IdlServiceStruct,
    typename="nav_msgs/srv/GetPlan",
):
    request_message: GetPlan_Request = field(default_factory=GetPlan_Request)
    response_message: GetPlan_Response = field(default_factory=GetPlan_Response)
    event_message: GetPlan_Event = field(default_factory=GetPlan_Event)


@dataclass
class LoadMap_Request(idl.IdlStruct, typename="nav_msgs/srv/LoadMap_Request"):
    map_url: str = ""


@dataclass
class LoadMap_Response(idl.IdlStruct, typename="nav_msgs/srv/LoadMap_Response"):
    RESULT_SUCCESS: Literal[0] = 0
    RESULT_MAP_DOES_NOT_EXIST: Literal[1] = 1
    RESULT_INVALID_MAP_DATA: Literal[2] = 2
    RESULT_INVALID_MAP_METADATA: Literal[3] = 3
    RESULT_UNDEFINED_FAILURE: Literal[255] = 255
    map: OccupancyGrid = field(default_factory=OccupancyGrid)
    result: idl.types.uint8 = 0


@dataclass
class LoadMap_Event(
    idl.IdlStruct,
    typename="nav_msgs/srv/LoadMap_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[LoadMap_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[LoadMap_Response, 1] = field(default_factory=list)


@dataclass
class LoadMap(
    idl.IdlServiceStruct,
    typename="nav_msgs/srv/LoadMap",
):
    request_message: LoadMap_Request = field(default_factory=LoadMap_Request)
    response_message: LoadMap_Response = field(default_factory=LoadMap_Response)
    event_message: LoadMap_Event = field(default_factory=LoadMap_Event)


@dataclass
class SetMap_Request(idl.IdlStruct, typename="nav_msgs/srv/SetMap_Request"):
    map: OccupancyGrid = field(default_factory=OccupancyGrid)
    initial_pose: PoseWithCovarianceStamped = field(
        default_factory=PoseWithCovarianceStamped
    )


@dataclass
class SetMap_Response(idl.IdlStruct, typename="nav_msgs/srv/SetMap_Response"):
    success: bool = False


@dataclass
class SetMap_Event(
    idl.IdlStruct,
    typename="nav_msgs/srv/SetMap_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[SetMap_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[SetMap_Response, 1] = field(default_factory=list)


@dataclass
class SetMap(
    idl.IdlServiceStruct,
    typename="nav_msgs/srv/SetMap",
):
    request_message: SetMap_Request = field(default_factory=SetMap_Request)
    response_message: SetMap_Response = field(default_factory=SetMap_Response)
    event_message: SetMap_Event = field(default_factory=SetMap_Event)
