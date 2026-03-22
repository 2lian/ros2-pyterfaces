from dataclasses import dataclass, field
from typing import ClassVar, Literal

from .. import idl
from ..builtin_interfaces.msg import Time


@dataclass
class ServiceEventInfo(idl.IdlStruct, typename="service_msgs/msg/ServiceEventInfo"):
    REQUEST_SENT: ClassVar[Literal[0]] = 0
    REQUEST_RECEIVED: ClassVar[Literal[1]] = 1
    RESPONSE_SENT: ClassVar[Literal[2]] = 2
    RESPONSE_RECEIVED: ClassVar[Literal[3]] = 3

    event_type: idl.types.uint8 = 0
    stamp: Time = field(default_factory=lambda *_: Time())
    client_gid: idl.types.array[idl.types.uint8, 16] = field(
        default_factory=lambda *_: [0] * 16
    )
    sequence_number: idl.types.int64 = 0
