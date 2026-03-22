from dataclasses import dataclass, field

from .. import idl
from ..service_msgs.msg import ServiceEventInfo
from ..visualization_msgs.msg import InteractiveMarker

@dataclass
class GetInteractiveMarkers_Request(
    idl.IdlStruct, typename="visualization_msgs/srv/GetInteractiveMarkers_Request"
):
    pass


@dataclass
class GetInteractiveMarkers_Response(
    idl.IdlStruct, typename="visualization_msgs/srv/GetInteractiveMarkers_Response"
):
    sequence_number: idl.types.uint64 = 0
    markers: idl.types.sequence[InteractiveMarker] = field(default_factory=list)


@dataclass
class GetInteractiveMarkers_Event(
    idl.IdlStruct,
    typename="visualization_msgs/srv/GetInteractiveMarkers_Event"
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[GetInteractiveMarkers_Request, 1] = field(
        default_factory=list
    )
    response: idl.types.sequence[GetInteractiveMarkers_Response, 1] = field(
        default_factory=list
    )


@dataclass
class GetInteractiveMarkers(
    idl.IdlServiceStruct,
    typename="visualization_msgs/srv/GetInteractiveMarkers"
):
    request_message: GetInteractiveMarkers_Request = field(
        default_factory=GetInteractiveMarkers_Request
    )
    response_message: GetInteractiveMarkers_Response = field(
        default_factory=GetInteractiveMarkers_Response
    )
    event_message: GetInteractiveMarkers_Event = field(
        default_factory=GetInteractiveMarkers_Event
    )
