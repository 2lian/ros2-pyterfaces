from dataclasses import dataclass, field

from .. import idl
from ..service_msgs.msg import ServiceEventInfo
from .msg import KeyValue, TypeDescription, TypeSource


@dataclass
class GetTypeDescription_Request(
    idl.IdlStruct, typename="type_description_interfaces/srv/GetTypeDescription_Request"
):
    type_name: str = ""
    type_hash: str = ""
    include_type_sources: bool = True


@dataclass
class GetTypeDescription_Response(
    idl.IdlStruct, typename="type_description_interfaces/srv/GetTypeDescription_Response"
):
    successful: bool = False
    failure_reason: str = ""
    type_description: TypeDescription = field(default_factory=TypeDescription)
    type_sources: idl.types.sequence[TypeSource] = field(default_factory=list)
    extra_information: idl.types.sequence[KeyValue] = field(default_factory=list)


@dataclass
class GetTypeDescription_Event(
    idl.IdlStruct,
    typename="type_description_interfaces/srv/GetTypeDescription_Event"
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[GetTypeDescription_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[GetTypeDescription_Response, 1] = field(
        default_factory=list
    )


GetTypeDescription: idl.IdlServiceType[
    GetTypeDescription_Request,
    GetTypeDescription_Response,
    GetTypeDescription_Event,
] = idl.make_idl_service(
    GetTypeDescription_Request,
    GetTypeDescription_Response,
    _event_type=GetTypeDescription_Event,
)
