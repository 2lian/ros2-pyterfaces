from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from .. import idl
from ..idl import IdlStruct
from ..service_msgs.msg import ServiceEventInfo


class Empty_Request(IdlStruct):
    __idl_typename__ = "std_srvs/srv/Empty_Request"


class Empty_Response(IdlStruct):
    __idl_typename__ = "std_srvs/srv/Empty_Response"


class Empty_Event(IdlStruct):
    __idl_typename__ = "std_srvs/srv/Empty_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass


class Empty(IdlStruct):
    __idl_typename__ = "std_srvs/srv/Empty"
    __unsupported_reason__ = "event_message references unsupported message Empty_Event"
    request_message: Empty_Request = msgspec.field(default_factory=Empty_Request)
    response_message: Empty_Response = msgspec.field(default_factory=Empty_Response)
    event_message: Empty_Event = msgspec.field(default_factory=lambda: Empty_Event())


class SetBool_Request(IdlStruct):
    __idl_typename__ = "std_srvs/srv/SetBool_Request"
    data: types.boolean = False


class SetBool_Response(IdlStruct):
    __idl_typename__ = "std_srvs/srv/SetBool_Response"
    success: types.boolean = False
    message: types.string = b""


class SetBool_Event(IdlStruct):
    __idl_typename__ = "std_srvs/srv/SetBool_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass


class SetBool(IdlStruct):
    __idl_typename__ = "std_srvs/srv/SetBool"
    __unsupported_reason__ = (
        "event_message references unsupported message SetBool_Event"
    )
    request_message: SetBool_Request = msgspec.field(default_factory=SetBool_Request)
    response_message: SetBool_Response = msgspec.field(default_factory=SetBool_Response)
    event_message: SetBool_Event = msgspec.field(
        default_factory=lambda: SetBool_Event()
    )


class Trigger_Request(IdlStruct):
    __idl_typename__ = "std_srvs/srv/Trigger_Request"


class Trigger_Response(IdlStruct):
    __idl_typename__ = "std_srvs/srv/Trigger_Response"
    success: types.boolean = False
    message: types.string = b""


class Trigger_Event(IdlStruct):
    __idl_typename__ = "std_srvs/srv/Trigger_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass


class Trigger(IdlStruct):
    __idl_typename__ = "std_srvs/srv/Trigger"
    __unsupported_reason__ = (
        "event_message references unsupported message Trigger_Event"
    )
    request_message: Trigger_Request = msgspec.field(default_factory=Trigger_Request)
    response_message: Trigger_Response = msgspec.field(default_factory=Trigger_Response)
    event_message: Trigger_Event = msgspec.field(
        default_factory=lambda: Trigger_Event()
    )

# cydr service type bindings
Empty = idl.make_idl_service(
    Empty_Request,
    Empty_Response,
    typename=Empty_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
Empty_Event = Empty.Event

SetBool = idl.make_idl_service(
    SetBool_Request,
    SetBool_Response,
    typename=SetBool_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
SetBool_Event = SetBool.Event

Trigger = idl.make_idl_service(
    Trigger_Request,
    Trigger_Response,
    typename=Trigger_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
Trigger_Event = Trigger.Event
