from dataclasses import dataclass, field

from .. import idl
from ..rcl_interfaces.msg import Parameter


@dataclass
class ListNodes_Request(
    idl.IdlStruct, typename="composition_interfaces/srv/ListNodes_Request"
):
    pass


@dataclass
class ListNodes_Response(
    idl.IdlStruct, typename="composition_interfaces/srv/ListNodes_Response"
):
    full_node_names: idl.types.sequence[str] = field(default_factory=list)
    unique_ids: idl.types.sequence[idl.types.uint64] = field(default_factory=list)


ListNodes = idl.make_idl_service(ListNodes_Request, ListNodes_Response)
ListNodes_Event = ListNodes.Event


@dataclass
class LoadNode_Request(
    idl.IdlStruct, typename="composition_interfaces/srv/LoadNode_Request"
):
    package_name: str = ""
    plugin_name: str = ""
    node_name: str = ""
    node_namespace: str = ""
    log_level: idl.types.uint8 = 0
    remap_rules: idl.types.sequence[str] = field(default_factory=list)
    parameters: idl.types.sequence[Parameter] = field(default_factory=list)
    extra_arguments: idl.types.sequence[Parameter] = field(default_factory=list)


@dataclass
class LoadNode_Response(
    idl.IdlStruct, typename="composition_interfaces/srv/LoadNode_Response"
):
    success: bool = False
    error_message: str = ""
    full_node_name: str = ""
    unique_id: idl.types.uint64 = 0


LoadNode = idl.make_idl_service(LoadNode_Request, LoadNode_Response)
LoadNode_Event = LoadNode.Event


@dataclass
class UnloadNode_Request(
    idl.IdlStruct, typename="composition_interfaces/srv/UnloadNode_Request"
):
    unique_id: idl.types.uint64 = 0


@dataclass
class UnloadNode_Response(
    idl.IdlStruct, typename="composition_interfaces/srv/UnloadNode_Response"
):
    success: bool = False
    error_message: str = ""


UnloadNode = idl.make_idl_service(UnloadNode_Request, UnloadNode_Response)
UnloadNode_Event = UnloadNode.Event
