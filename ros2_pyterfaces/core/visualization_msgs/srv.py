from .. import Array, BoundedString, CoreSchema, Sequence, make_srv_schema

from ..visualization_msgs.msg import InteractiveMarker

GetInteractiveMarkers_Request: CoreSchema = {
    "__typename": "visualization_msgs/srv/GetInteractiveMarkers_Request",
}

GetInteractiveMarkers_Response: CoreSchema = {
    "__typename": "visualization_msgs/srv/GetInteractiveMarkers_Response",
    "sequence_number": "uint64",
    "markers": Sequence(InteractiveMarker),
}

GetInteractiveMarkers: CoreSchema = make_srv_schema(GetInteractiveMarkers_Request, GetInteractiveMarkers_Response, typename="visualization_msgs/srv/GetInteractiveMarkers")
GetInteractiveMarkers_Event: CoreSchema = GetInteractiveMarkers["event_message"]

__all__ = [
    "GetInteractiveMarkers_Request",
    "GetInteractiveMarkers_Response",
    "GetInteractiveMarkers_Event",
    "GetInteractiveMarkers",
]
