from .. import Array, BoundedString, CoreSchema, Sequence, make_srv_schema

from ..sensor_msgs.msg import CameraInfo

SetCameraInfo_Request: CoreSchema = {
    "__typename": "sensor_msgs/srv/SetCameraInfo_Request",
    "camera_info": CameraInfo,
}

SetCameraInfo_Response: CoreSchema = {
    "__typename": "sensor_msgs/srv/SetCameraInfo_Response",
    "success": "bool",
    "status_message": "string",
}

SetCameraInfo: CoreSchema = make_srv_schema(SetCameraInfo_Request, SetCameraInfo_Response, typename="sensor_msgs/srv/SetCameraInfo")
SetCameraInfo_Event: CoreSchema = SetCameraInfo["event_message"]

__all__ = [
    "SetCameraInfo_Request",
    "SetCameraInfo_Response",
    "SetCameraInfo_Event",
    "SetCameraInfo",
]
