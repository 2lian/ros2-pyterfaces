from .. import Array, BoundedString, CoreSchema, Sequence, make_srv_schema

from ..geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from ..nav_msgs.msg import OccupancyGrid, Path

GetMap_Request: CoreSchema = {
    "__typename": "nav_msgs/srv/GetMap_Request",
}

GetMap_Response: CoreSchema = {
    "__typename": "nav_msgs/srv/GetMap_Response",
    "map": OccupancyGrid,
}

GetPlan_Request: CoreSchema = {
    "__typename": "nav_msgs/srv/GetPlan_Request",
    "start": PoseStamped,
    "goal": PoseStamped,
    "tolerance": "float32",
}

GetPlan_Response: CoreSchema = {
    "__typename": "nav_msgs/srv/GetPlan_Response",
    "plan": Path,
}

LoadMap_Request: CoreSchema = {
    "__typename": "nav_msgs/srv/LoadMap_Request",
    "map_url": "string",
}

LoadMap_Response: CoreSchema = {
    "__typename": "nav_msgs/srv/LoadMap_Response",
    "map": OccupancyGrid,
    "result": "uint8",
}

SetMap_Request: CoreSchema = {
    "__typename": "nav_msgs/srv/SetMap_Request",
    "map": OccupancyGrid,
    "initial_pose": PoseWithCovarianceStamped,
}

SetMap_Response: CoreSchema = {
    "__typename": "nav_msgs/srv/SetMap_Response",
    "success": "bool",
}

GetMap: CoreSchema = make_srv_schema(GetMap_Request, GetMap_Response, typename="nav_msgs/srv/GetMap")
GetMap_Event: CoreSchema = GetMap["event_message"]

GetPlan: CoreSchema = make_srv_schema(GetPlan_Request, GetPlan_Response, typename="nav_msgs/srv/GetPlan")
GetPlan_Event: CoreSchema = GetPlan["event_message"]

LoadMap: CoreSchema = make_srv_schema(LoadMap_Request, LoadMap_Response, typename="nav_msgs/srv/LoadMap")
LoadMap_Event: CoreSchema = LoadMap["event_message"]

SetMap: CoreSchema = make_srv_schema(SetMap_Request, SetMap_Response, typename="nav_msgs/srv/SetMap")
SetMap_Event: CoreSchema = SetMap["event_message"]

__all__ = [
    "GetMap_Request",
    "GetMap_Response",
    "GetPlan_Request",
    "GetPlan_Response",
    "LoadMap_Request",
    "LoadMap_Response",
    "SetMap_Request",
    "SetMap_Response",
    "GetMap_Event",
    "GetMap",
    "GetPlan_Event",
    "GetPlan",
    "LoadMap_Event",
    "LoadMap",
    "SetMap_Event",
    "SetMap",
]
