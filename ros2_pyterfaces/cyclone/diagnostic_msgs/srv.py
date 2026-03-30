from dataclasses import dataclass, field

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


AddDiagnostics: idl.IdlServiceType[
    AddDiagnostics_Request,
    AddDiagnostics_Response,
    AddDiagnostics_Event,
] = idl.make_idl_service(
    AddDiagnostics_Request,
    AddDiagnostics_Response,
    event_type=AddDiagnostics_Event,
)


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


SelfTest: idl.IdlServiceType[SelfTest_Request, SelfTest_Response, SelfTest_Event] = (
    idl.make_idl_service(
        SelfTest_Request,
        SelfTest_Response,
        event_type=SelfTest_Event,
    )
)
