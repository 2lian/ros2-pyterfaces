from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from .. import idl
from ..idl import JitStruct
from ..service_msgs.msg import ServiceEventInfo
from .msg import CameraInfo

class SetCameraInfo_Request(JitStruct):
    __idl_typename__ = 'sensor_msgs/srv/SetCameraInfo_Request'
    camera_info: CameraInfo = msgspec.field(default_factory=CameraInfo)

class SetCameraInfo_Response(JitStruct):
    __idl_typename__ = 'sensor_msgs/srv/SetCameraInfo_Response'
    success: types.boolean = False
    status_message: types.string = b''

class SetCameraInfo_Event(JitStruct):
    __idl_typename__ = 'sensor_msgs/srv/SetCameraInfo_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class SetCameraInfo(JitStruct):
    __idl_typename__ = 'sensor_msgs/srv/SetCameraInfo'
    __unsupported_reason__ = 'event_message references unsupported message SetCameraInfo_Event'
    request_message: SetCameraInfo_Request = msgspec.field(default_factory=SetCameraInfo_Request)
    response_message: SetCameraInfo_Response = msgspec.field(default_factory=SetCameraInfo_Response)
    event_message: SetCameraInfo_Event = msgspec.field(default_factory=lambda: SetCameraInfo_Event())

# cydr service type bindings
SetCameraInfo = idl.make_idl_service(
    SetCameraInfo_Request,
    SetCameraInfo_Response,
    typename=SetCameraInfo_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
SetCameraInfo_Event = SetCameraInfo.Event
