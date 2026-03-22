from dataclasses import dataclass, field
from typing import ClassVar, Type

from .. import idl
from ..diagnostic_msgs.msg import DiagnosticStatus
from ..service_msgs.msg import ServiceEventInfo

@dataclass
class AddDiagnostics_Request(
    idl.IdlStruct, typename="diagnostic_msgs/srv/AddDiagnostics_Request"
):
    load_namespace: str = ""


@dataclass
class AddDiagnostics_Response(
    idl.IdlStruct, typename="diagnostic_msgs/srv/AddDiagnostics_Response"
):
    success: bool = False
    message: str = ""


@dataclass
class AddDiagnostics_Event(
    idl.IdlStruct,
    typename="diagnostic_msgs/srv/AddDiagnostics_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[AddDiagnostics_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[AddDiagnostics_Response, 1] = field(default_factory=list)


@dataclass
class AddDiagnostics(
    idl.IdlServiceStruct,
    typename="diagnostic_msgs/srv/AddDiagnostics",
):
    Request: ClassVar[Type[AddDiagnostics_Request]] = AddDiagnostics_Request
    Response: ClassVar[Type[AddDiagnostics_Response]] = AddDiagnostics_Response
    request_message: AddDiagnostics_Request = field(default_factory=AddDiagnostics_Request)
    response_message: AddDiagnostics_Response = field(default_factory=AddDiagnostics_Response)
    event_message: AddDiagnostics_Event = field(default_factory=AddDiagnostics_Event)


@dataclass
class SelfTest_Request(idl.IdlStruct, typename="diagnostic_msgs/srv/SelfTest_Request"):
    pass


@dataclass
class SelfTest_Response(idl.IdlStruct, typename="diagnostic_msgs/srv/SelfTest_Response"):
    id: str = ""
    passed: idl.types.byte = 0
    status: idl.types.sequence[DiagnosticStatus] = field(default_factory=list)


@dataclass
class SelfTest_Event(
    idl.IdlStruct,
    typename="diagnostic_msgs/srv/SelfTest_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[SelfTest_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[SelfTest_Response, 1] = field(default_factory=list)


@dataclass
class SelfTest(
    idl.IdlServiceStruct,
    typename="diagnostic_msgs/srv/SelfTest",
):
    Request: ClassVar[Type[SelfTest_Request]] = SelfTest_Request
    Response: ClassVar[Type[SelfTest_Response]] = SelfTest_Response
    request_message: SelfTest_Request = field(default_factory=SelfTest_Request)
    response_message: SelfTest_Response = field(default_factory=SelfTest_Response)
    event_message: SelfTest_Event = field(default_factory=SelfTest_Event)
