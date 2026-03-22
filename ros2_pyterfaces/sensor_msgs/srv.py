from dataclasses import dataclass, field

from ..idl import IdlService, IdlStruct
from ..sensor_msgs.msg import CameraInfo

__all__ = [
    "SetCameraInfo",
    "SetCameraInfo_Request",
    "SetCameraInfo_Response",
]


@dataclass
class SetCameraInfo_Request(IdlStruct, typename="sensor_msgs/srv/SetCameraInfo_Request"):
    camera_info: CameraInfo = field(default_factory=CameraInfo)


@dataclass
class SetCameraInfo_Response(
    IdlStruct, typename="sensor_msgs/srv/SetCameraInfo_Response"
):
    success: bool = False
    status_message: str = ""


class SetCameraInfo(IdlService, typename="sensor_msgs/srv/SetCameraInfo"):
    Request = SetCameraInfo_Request
    Response = SetCameraInfo_Response
