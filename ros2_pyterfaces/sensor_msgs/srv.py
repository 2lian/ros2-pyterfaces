from dataclasses import dataclass, field

from .. import idl
from ..service_msgs.msg import ServiceEventInfo
from ..sensor_msgs.msg import CameraInfo

@dataclass
class SetCameraInfo_Request(
    idl.IdlStruct, typename="sensor_msgs/srv/SetCameraInfo_Request"
):
    camera_info: CameraInfo = field(default_factory=CameraInfo)


@dataclass
class SetCameraInfo_Response(
    idl.IdlStruct, typename="sensor_msgs/srv/SetCameraInfo_Response"
):
    success: bool = False
    status_message: str = ""


@dataclass
class SetCameraInfo_Event(
    idl.IdlStruct,
    typename="sensor_msgs/srv/SetCameraInfo_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[SetCameraInfo_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[SetCameraInfo_Response, 1] = field(default_factory=list)


@dataclass
class SetCameraInfo(
    idl.IdlServiceStruct,
    typename="sensor_msgs/srv/SetCameraInfo",
):
    request_message: SetCameraInfo_Request = field(default_factory=SetCameraInfo_Request)
    response_message: SetCameraInfo_Response = field(default_factory=SetCameraInfo_Response)
    event_message: SetCameraInfo_Event = field(default_factory=SetCameraInfo_Event)
