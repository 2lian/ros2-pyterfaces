from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..service_msgs.msg import ServiceEventInfo
from .msg import DiagnosticStatus

class AddDiagnostics_Request(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/srv/AddDiagnostics_Request'
    load_namespace: types.string = b''

class AddDiagnostics_Response(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/srv/AddDiagnostics_Response'
    success: types.boolean = False
    message: types.string = b''

class AddDiagnostics_Event(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/srv/AddDiagnostics_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class AddDiagnostics(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/srv/AddDiagnostics'
    __unsupported_reason__ = 'event_message references unsupported message AddDiagnostics_Event'
    request_message: AddDiagnostics_Request = msgspec.field(default_factory=AddDiagnostics_Request)
    response_message: AddDiagnostics_Response = msgspec.field(default_factory=AddDiagnostics_Response)
    event_message: AddDiagnostics_Event = msgspec.field(default_factory=lambda: AddDiagnostics_Event())

class SelfTest_Request(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/srv/SelfTest_Request'

class SelfTest_Response(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/srv/SelfTest_Response'
    __unsupported_reason__ = 'status is a collection of messages, which cydr does not support'
    pass

class SelfTest_Event(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/srv/SelfTest_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class SelfTest(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/srv/SelfTest'
    __unsupported_reason__ = 'response_message references unsupported message SelfTest_Response'
    request_message: SelfTest_Request = msgspec.field(default_factory=SelfTest_Request)
    response_message: SelfTest_Response = msgspec.field(default_factory=SelfTest_Response)
    event_message: SelfTest_Event = msgspec.field(default_factory=lambda: SelfTest_Event())
