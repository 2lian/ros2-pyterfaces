from dataclasses import dataclass, field
from typing import ClassVar, Type

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


@dataclass
class Empty(
    idl.IdlServiceStruct,
    typename="std_srvs/srv/Empty",
):
    Request: ClassVar[Type[Empty_Request]] = Empty_Request
    Response: ClassVar[Type[Empty_Response]] = Empty_Response
    request_message: Empty_Request = field(default_factory=Empty_Request)
    response_message: Empty_Response = field(default_factory=Empty_Response)
    event_message: Empty_Event = field(default_factory=Empty_Event)


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


@dataclass
class SetBool(
    idl.IdlServiceStruct,
    typename="std_srvs/srv/SetBool",
):
    Request: ClassVar[Type[SetBool_Request]] = SetBool_Request
    Response: ClassVar[Type[SetBool_Response]] = SetBool_Response
    request_message: SetBool_Request = field(default_factory=SetBool_Request)
    response_message: SetBool_Response = field(default_factory=SetBool_Response)
    event_message: SetBool_Event = field(default_factory=SetBool_Event)


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


@dataclass
class Trigger(
    idl.IdlServiceStruct,
    typename="std_srvs/srv/Trigger",
):
    Request: ClassVar[Type[Trigger_Request]] = Trigger_Request
    Response: ClassVar[Type[Trigger_Response]] = Trigger_Response
    request_message: Trigger_Request = field(default_factory=Trigger_Request)
    response_message: Trigger_Response = field(default_factory=Trigger_Response)
    event_message: Trigger_Event = field(default_factory=Trigger_Event)
