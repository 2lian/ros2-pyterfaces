from dataclasses import dataclass, field
from typing import Literal

from ..idl import IdlStruct, types
from ..std_msgs.msg import Header


@dataclass
class KeyValue(IdlStruct, typename="diagnostic_msgs/msg/KeyValue"):
    key: str = ""
    value: str = ""


@dataclass
class DiagnosticStatus(IdlStruct, typename="diagnostic_msgs/msg/DiagnosticStatus"):
    level: types.byte = 0
    name: str = ""
    message: str = ""
    hardware_id: str = ""
    values: types.sequence[KeyValue] = field(default_factory=list)
    OK: Literal[0] = 0
    WARN: Literal[1] = 1
    ERROR: Literal[2] = 2
    STALE: Literal[3] = 3

@dataclass
class DiagnosticArray(IdlStruct, typename="diagnostic_msgs/msg/DiagnosticArray"):
    header: Header = field(default_factory=Header)
    status: types.sequence[DiagnosticStatus] = field(default_factory=list)
