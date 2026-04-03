from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from .. import idl
from ..idl import JitStruct
from ..rcl_interfaces.msg import Parameter
from ..service_msgs.msg import ServiceEventInfo

class ListNodes_Request(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/ListNodes_Request'

class ListNodes_Response(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/ListNodes_Response'
    full_node_names: types.NDArray[Any, types.Bytes] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.bytes_))
    unique_ids: types.NDArray[Any, types.UInt64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.uint64))

class ListNodes(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/ListNodes'
    __unsupported_reason__ = 'event_message references unsupported message ListNodes_Event'
    request_message: ListNodes_Request = msgspec.field(default_factory=ListNodes_Request)
    response_message: ListNodes_Response = msgspec.field(default_factory=ListNodes_Response)
    event_message: ListNodes_Event = msgspec.field(default_factory=lambda: ListNodes_Event())

class ListNodes_Event(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/ListNodes_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class LoadNode_Request(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/LoadNode_Request'
    __unsupported_reason__ = 'parameters is a collection of messages, which cydr does not support'
    pass

class LoadNode_Response(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/LoadNode_Response'
    success: types.boolean = False
    error_message: types.string = b''
    full_node_name: types.string = b''
    unique_id: types.uint64 = np.uint64(0)

class LoadNode(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/LoadNode'
    __unsupported_reason__ = 'request_message references unsupported message LoadNode_Request'
    request_message: LoadNode_Request = msgspec.field(default_factory=LoadNode_Request)
    response_message: LoadNode_Response = msgspec.field(default_factory=LoadNode_Response)
    event_message: LoadNode_Event = msgspec.field(default_factory=lambda: LoadNode_Event())

class LoadNode_Event(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/LoadNode_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

class UnloadNode_Request(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/UnloadNode_Request'
    unique_id: types.uint64 = np.uint64(0)

class UnloadNode_Response(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/UnloadNode_Response'
    success: types.boolean = False
    error_message: types.string = b''

class UnloadNode(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/UnloadNode'
    __unsupported_reason__ = 'event_message references unsupported message UnloadNode_Event'
    request_message: UnloadNode_Request = msgspec.field(default_factory=UnloadNode_Request)
    response_message: UnloadNode_Response = msgspec.field(default_factory=UnloadNode_Response)
    event_message: UnloadNode_Event = msgspec.field(default_factory=lambda: UnloadNode_Event())

class UnloadNode_Event(JitStruct):
    __idl_typename__ = 'composition_interfaces/srv/UnloadNode_Event'
    __unsupported_reason__ = 'request is a collection of messages, which cydr does not support'
    pass

# cydr service type bindings
ListNodes = idl.make_idl_service(
    ListNodes_Request,
    ListNodes_Response,
    typename=ListNodes_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
ListNodes_Event = ListNodes.Event

LoadNode = idl.make_idl_service(
    LoadNode_Request,
    LoadNode_Response,
    typename=LoadNode_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
LoadNode_Event = LoadNode.Event

UnloadNode = idl.make_idl_service(
    UnloadNode_Request,
    UnloadNode_Response,
    typename=UnloadNode_Request.get_type_name().removesuffix("_Request"),
    _module_name=__name__,
)
UnloadNode_Event = UnloadNode.Event
