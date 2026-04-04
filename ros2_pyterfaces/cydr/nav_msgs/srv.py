from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from .. import idl
from ..idl import IdlStruct
from ..geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from ..service_msgs.msg import ServiceEventInfo
from .msg import OccupancyGrid, Path

class GetMap_Request(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/GetMap_Request'

class GetMap_Response(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/GetMap_Response'
    map: OccupancyGrid = msgspec.field(default_factory=OccupancyGrid)

class GetMap_Event(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/GetMap_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class GetMap(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/GetMap'
    __unsupported_reason__ = 'event_message references unsupported message GetMap_Event'
    request_message: GetMap_Request = msgspec.field(default_factory=GetMap_Request)
    response_message: GetMap_Response = msgspec.field(default_factory=GetMap_Response)
    event_message: GetMap_Event = msgspec.field(default_factory=lambda: GetMap_Event())

class GetPlan_Request(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/GetPlan_Request'
    start: PoseStamped = msgspec.field(default_factory=PoseStamped)
    goal: PoseStamped = msgspec.field(default_factory=PoseStamped)
    tolerance: types.float32 = np.float32(0.0)

class GetPlan_Response(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/GetPlan_Response'
    __unsupported_reason__ = 'plan references unsupported message Path'
    plan: Path = msgspec.field(default_factory=Path)

class GetPlan_Event(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/GetPlan_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class GetPlan(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/GetPlan'
    __unsupported_reason__ = 'response_message references unsupported message GetPlan_Response'
    request_message: GetPlan_Request = msgspec.field(default_factory=GetPlan_Request)
    response_message: GetPlan_Response = msgspec.field(default_factory=GetPlan_Response)
    event_message: GetPlan_Event = msgspec.field(default_factory=lambda: GetPlan_Event())

class LoadMap_Request(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/LoadMap_Request'
    map_url: types.string = b''

class LoadMap_Response(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/LoadMap_Response'
    map: OccupancyGrid = msgspec.field(default_factory=OccupancyGrid)
    result: types.uint8 = np.uint8(0)

class LoadMap_Event(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/LoadMap_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class LoadMap(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/LoadMap'
    __unsupported_reason__ = 'event_message references unsupported message LoadMap_Event'
    request_message: LoadMap_Request = msgspec.field(default_factory=LoadMap_Request)
    response_message: LoadMap_Response = msgspec.field(default_factory=LoadMap_Response)
    event_message: LoadMap_Event = msgspec.field(default_factory=lambda: LoadMap_Event())

class SetMap_Request(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/SetMap_Request'
    map: OccupancyGrid = msgspec.field(default_factory=OccupancyGrid)
    initial_pose: PoseWithCovarianceStamped = msgspec.field(default_factory=PoseWithCovarianceStamped)

class SetMap_Response(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/SetMap_Response'
    success: types.boolean = False

class SetMap_Event(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/SetMap_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class SetMap(IdlStruct):
    __idl_typename__ = 'nav_msgs/srv/SetMap'
    __unsupported_reason__ = 'event_message references unsupported message SetMap_Event'
    request_message: SetMap_Request = msgspec.field(default_factory=SetMap_Request)
    response_message: SetMap_Response = msgspec.field(default_factory=SetMap_Response)
    event_message: SetMap_Event = msgspec.field(default_factory=lambda: SetMap_Event())

# cydr service type bindings
GetMap = idl.make_idl_service(
    GetMap_Request,
    GetMap_Response,
    typename=GetMap_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
GetMap_Event = GetMap.Event

GetPlan = idl.make_idl_service(
    GetPlan_Request,
    GetPlan_Response,
    typename=GetPlan_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
GetPlan_Event = GetPlan.Event

LoadMap = idl.make_idl_service(
    LoadMap_Request,
    LoadMap_Response,
    typename=LoadMap_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
LoadMap_Event = LoadMap.Event

SetMap = idl.make_idl_service(
    SetMap_Request,
    SetMap_Response,
    typename=SetMap_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
SetMap_Event = SetMap.Event
