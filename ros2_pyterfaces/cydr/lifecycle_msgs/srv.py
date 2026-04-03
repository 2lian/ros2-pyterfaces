from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from .. import idl
from ..idl import JitStruct
from ..service_msgs.msg import ServiceEventInfo
from .msg import State, Transition, TransitionDescription

class ChangeState_Request(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/ChangeState_Request'
    transition: Transition = msgspec.field(default_factory=Transition)

class ChangeState_Response(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/ChangeState_Response'
    success: types.boolean = False

class ChangeState(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/ChangeState'
    __unsupported_reason__ = 'event_message references unsupported message ChangeState_Event'
    request_message: ChangeState_Request = msgspec.field(default_factory=ChangeState_Request)
    response_message: ChangeState_Response = msgspec.field(default_factory=ChangeState_Response)
    event_message: ChangeState_Event = msgspec.field(default_factory=lambda: ChangeState_Event())

class ChangeState_Event(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/ChangeState_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class GetAvailableStates_Request(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetAvailableStates_Request'

class GetAvailableStates_Response(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetAvailableStates_Response'
    __unsupported_reason__ = 'available_states is a collection of messages, which cydr does not support'
    pass

class GetAvailableStates(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetAvailableStates'
    __unsupported_reason__ = 'response_message references unsupported message GetAvailableStates_Response'
    request_message: GetAvailableStates_Request = msgspec.field(default_factory=GetAvailableStates_Request)
    response_message: GetAvailableStates_Response = msgspec.field(default_factory=GetAvailableStates_Response)
    event_message: GetAvailableStates_Event = msgspec.field(default_factory=lambda: GetAvailableStates_Event())

class GetAvailableStates_Event(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetAvailableStates_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class GetAvailableTransitions_Request(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetAvailableTransitions_Request'

class GetAvailableTransitions_Response(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetAvailableTransitions_Response'
    __unsupported_reason__ = 'available_transitions is a collection of messages, which cydr does not support'
    pass

class GetAvailableTransitions(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetAvailableTransitions'
    __unsupported_reason__ = 'response_message references unsupported message GetAvailableTransitions_Response'
    request_message: GetAvailableTransitions_Request = msgspec.field(default_factory=GetAvailableTransitions_Request)
    response_message: GetAvailableTransitions_Response = msgspec.field(default_factory=GetAvailableTransitions_Response)
    event_message: GetAvailableTransitions_Event = msgspec.field(default_factory=lambda: GetAvailableTransitions_Event())

class GetAvailableTransitions_Event(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetAvailableTransitions_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class GetState_Request(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetState_Request'

class GetState_Response(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetState_Response'
    current_state: State = msgspec.field(default_factory=State)

class GetState(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetState'
    __unsupported_reason__ = 'event_message references unsupported message GetState_Event'
    request_message: GetState_Request = msgspec.field(default_factory=GetState_Request)
    response_message: GetState_Response = msgspec.field(default_factory=GetState_Response)
    event_message: GetState_Event = msgspec.field(default_factory=lambda: GetState_Event())

class GetState_Event(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/srv/GetState_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

# cydr service type bindings
ChangeState = idl.make_idl_service(
    ChangeState_Request,
    ChangeState_Response,
    typename=ChangeState_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
ChangeState_Event = ChangeState.Event

GetAvailableStates = idl.make_idl_service(
    GetAvailableStates_Request,
    GetAvailableStates_Response,
    typename=GetAvailableStates_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
GetAvailableStates_Event = GetAvailableStates.Event

GetAvailableTransitions = idl.make_idl_service(
    GetAvailableTransitions_Request,
    GetAvailableTransitions_Response,
    typename=GetAvailableTransitions_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
GetAvailableTransitions_Event = GetAvailableTransitions.Event

GetState = idl.make_idl_service(
    GetState_Request,
    GetState_Response,
    typename=GetState_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
GetState_Event = GetState.Event
