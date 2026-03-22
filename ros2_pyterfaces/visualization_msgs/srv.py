from dataclasses import dataclass, field

from ..idl import IdlService, IdlStruct, types
from ..visualization_msgs.msg import InteractiveMarker

__all__ = [
    "GetInteractiveMarkers",
    "GetInteractiveMarkers_Request",
    "GetInteractiveMarkers_Response",
]


@dataclass
class GetInteractiveMarkers_Request(
    IdlStruct, typename="visualization_msgs/srv/GetInteractiveMarkers_Request"
):
    pass


@dataclass
class GetInteractiveMarkers_Response(
    IdlStruct, typename="visualization_msgs/srv/GetInteractiveMarkers_Response"
):
    sequence_number: types.uint64 = 0
    markers: types.sequence[InteractiveMarker] = field(default_factory=list)


class GetInteractiveMarkers(
    IdlService, typename="visualization_msgs/srv/GetInteractiveMarkers"
):
    Request = GetInteractiveMarkers_Request
    Response = GetInteractiveMarkers_Response
