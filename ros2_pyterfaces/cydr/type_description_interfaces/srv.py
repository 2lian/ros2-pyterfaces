from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from .. import idl
from ..idl import IdlStruct
from ..service_msgs.msg import ServiceEventInfo
from .msg import KeyValue, TypeDescription, TypeSource

class GetTypeDescription_Request(IdlStruct):
    __idl_typename__ = 'type_description_interfaces/srv/GetTypeDescription_Request'
    type_name: types.string = b''
    type_hash: types.string = b''
    include_type_sources: types.boolean = True

class GetTypeDescription_Response(IdlStruct):
    __idl_typename__ = 'type_description_interfaces/srv/GetTypeDescription_Response'
    __unsupported_reason__ = 'type_sources is a collection of messages, which cydr does not support'
    pass

class GetTypeDescription_Event(IdlStruct):
    __idl_typename__ = 'type_description_interfaces/srv/GetTypeDescription_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class GetTypeDescription(IdlStruct):
    __idl_typename__ = 'type_description_interfaces/srv/GetTypeDescription'
    __unsupported_reason__ = 'response_message references unsupported message GetTypeDescription_Response'
    request_message: GetTypeDescription_Request = msgspec.field(default_factory=GetTypeDescription_Request)
    response_message: GetTypeDescription_Response = msgspec.field(default_factory=GetTypeDescription_Response)
    event_message: GetTypeDescription_Event = msgspec.field(default_factory=lambda: GetTypeDescription_Event())

# cydr service type bindings
GetTypeDescription = idl.make_idl_service(
    GetTypeDescription_Request,
    GetTypeDescription_Response,
    typename=GetTypeDescription_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
GetTypeDescription_Event = GetTypeDescription.Event
