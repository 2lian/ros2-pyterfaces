from dataclasses import dataclass, field

from .. import idl
from ..service_msgs.msg import ServiceEventInfo


@dataclass
class Empty_Request(idl.IdlStruct, typename="std_srvs/srv/Empty_Request"):
    pass


@dataclass
class Empty_Response(idl.IdlStruct, typename="std_srvs/srv/Empty_Response"):
    pass


@dataclass
class Empty_Event(
    idl.IdlStruct,
    typename="std_srvs/srv/Empty_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[Empty_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[Empty_Response, 1] = field(default_factory=list)


Empty: idl.IdlServiceType[Empty_Request, Empty_Response, Empty_Event] = (
    idl.make_idl_service(
        Empty_Request,
        Empty_Response,
        _event_type=Empty_Event,
    )
)


@dataclass
class SetBool_Request(idl.IdlStruct, typename="std_srvs/srv/SetBool_Request"):
    data: bool = False


@dataclass
class SetBool_Response(idl.IdlStruct, typename="std_srvs/srv/SetBool_Response"):
    success: bool = False
    message: str = ""


@dataclass
class SetBool_Event(
    idl.IdlStruct,
    typename="std_srvs/srv/SetBool_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[SetBool_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[SetBool_Response, 1] = field(default_factory=list)


SetBool: idl.IdlServiceType[SetBool_Request, SetBool_Response, SetBool_Event] = (
    idl.make_idl_service(
        SetBool_Request,
        SetBool_Response,
        _event_type=SetBool_Event,
    )
)

@dataclass
class Trigger_Request(idl.IdlStruct, typename="std_srvs/srv/Trigger_Request"):
    pass


@dataclass
class Trigger_Response(idl.IdlStruct, typename="std_srvs/srv/Trigger_Response"):
    success: bool = False
    message: str = ""


@dataclass
class Trigger_Event(
    idl.IdlStruct,
    typename="std_srvs/srv/Trigger_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[Trigger_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[Trigger_Response, 1] = field(default_factory=list)


Trigger: idl.IdlServiceType[Trigger_Request, Trigger_Response, Trigger_Event] = (
    idl.make_idl_service(
        Trigger_Request,
        Trigger_Response,
        _event_type=Trigger_Event,
    )
)
