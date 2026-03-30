from dataclasses import dataclass, field
from typing import ClassVar, Literal

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
    OK: ClassVar[Literal[0]] = 0
    WARN: ClassVar[Literal[1]] = 1
    ERROR: ClassVar[Literal[2]] = 2
    STALE: ClassVar[Literal[3]] = 3

@dataclass
class DiagnosticArray(IdlStruct, typename="diagnostic_msgs/msg/DiagnosticArray"):
    header: Header = field(default_factory=Header)
    status: types.sequence[DiagnosticStatus] = field(default_factory=list)
