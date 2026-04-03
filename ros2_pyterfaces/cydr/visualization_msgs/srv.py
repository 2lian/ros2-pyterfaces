from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..service_msgs.msg import ServiceEventInfo
from .msg import InteractiveMarker

class GetInteractiveMarkers_Request(JitStruct):
    __idl_typename__ = 'visualization_msgs/srv/GetInteractiveMarkers_Request'

class GetInteractiveMarkers_Response(JitStruct):
    __idl_typename__ = 'visualization_msgs/srv/GetInteractiveMarkers_Response'
    __unsupported_reason__ = 'markers is a collection of messages, which cydr does not support'
    pass

class GetInteractiveMarkers_Event(JitStruct):
    __idl_typename__ = 'visualization_msgs/srv/GetInteractiveMarkers_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class GetInteractiveMarkers(JitStruct):
    __idl_typename__ = 'visualization_msgs/srv/GetInteractiveMarkers'
    __unsupported_reason__ = 'response_message references unsupported message GetInteractiveMarkers_Response'
    request_message: GetInteractiveMarkers_Request = msgspec.field(default_factory=GetInteractiveMarkers_Request)
    response_message: GetInteractiveMarkers_Response = msgspec.field(default_factory=GetInteractiveMarkers_Response)
    event_message: GetInteractiveMarkers_Event = msgspec.field(default_factory=lambda: GetInteractiveMarkers_Event())
