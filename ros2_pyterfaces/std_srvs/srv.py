from dataclasses import dataclass

from ..idl import IdlService, IdlStruct

__all__ = [
    "Empty",
    "Empty_Request",
    "Empty_Response",
    "SetBool",
    "SetBool_Request",
    "SetBool_Response",
    "Trigger",
    "Trigger_Request",
    "Trigger_Response",
]


@dataclass
class Empty_Request(IdlStruct, typename="std_srvs/srv/Empty_Request"):
    pass


@dataclass
class Empty_Response(IdlStruct, typename="std_srvs/srv/Empty_Response"):
    pass


class Empty(IdlService, typename="std_srvs/srv/Empty"):
    Request = Empty_Request
    Response = Empty_Response


@dataclass
class SetBool_Request(IdlStruct, typename="std_srvs/srv/SetBool_Request"):
    data: bool = False


@dataclass
class SetBool_Response(IdlStruct, typename="std_srvs/srv/SetBool_Response"):
    success: bool = False
    message: str = ""


class SetBool(IdlService, typename="std_srvs/srv/SetBool"):
    Request = SetBool_Request
    Response = SetBool_Response


@dataclass
class Trigger_Request(IdlStruct, typename="std_srvs/srv/Trigger_Request"):
    pass


@dataclass
class Trigger_Response(IdlStruct, typename="std_srvs/srv/Trigger_Response"):
    success: bool = False
    message: str = ""


class Trigger(IdlService, typename="std_srvs/srv/Trigger"):
    Request = Trigger_Request
    Response = Trigger_Response
