from dataclasses import dataclass, field
from typing import ClassVar, Literal

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


GetMap: idl.IdlServiceType[GetMap_Request, GetMap_Response, GetMap_Event] = (
    idl.make_idl_service(
        GetMap_Request,
        GetMap_Response,
        _event_type=GetMap_Event,
    )
)


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


GetPlan: idl.IdlServiceType[GetPlan_Request, GetPlan_Response, GetPlan_Event] = (
    idl.make_idl_service(
        GetPlan_Request,
        GetPlan_Response,
        _event_type=GetPlan_Event,
    )
)


@dataclass
class LoadMap_Request(idl.IdlStruct, typename="nav_msgs/srv/LoadMap_Request"):
    map_url: str = ""


@dataclass
class LoadMap_Response(idl.IdlStruct, typename="nav_msgs/srv/LoadMap_Response"):
    RESULT_SUCCESS: ClassVar[Literal[0]] = 0
    RESULT_MAP_DOES_NOT_EXIST: ClassVar[Literal[1]] = 1
    RESULT_INVALID_MAP_DATA: ClassVar[Literal[2]] = 2
    RESULT_INVALID_MAP_METADATA: ClassVar[Literal[3]] = 3
    RESULT_UNDEFINED_FAILURE: ClassVar[Literal[255]] = 255
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


LoadMap: idl.IdlServiceType[LoadMap_Request, LoadMap_Response, LoadMap_Event] = (
    idl.make_idl_service(
        LoadMap_Request,
        LoadMap_Response,
        _event_type=LoadMap_Event,
    )
)


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


SetMap: idl.IdlServiceType[SetMap_Request, SetMap_Response, SetMap_Event] = (
    idl.make_idl_service(
        SetMap_Request,
        SetMap_Response,
        _event_type=SetMap_Event,
    )
)
