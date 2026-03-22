from dataclasses import dataclass, field
from typing import Final

from .. import idl
from ..builtin_interfaces.msg import Time


@dataclass
class ServiceEventInfo(idl.IdlStruct, typename="service_msgs/msg/ServiceEventInfo"):
    REQUEST_SENT: Final[idl.types.uint8] = 0
    REQUEST_RECEIVED: Final[idl.types.uint8] = 1
    RESPONSE_SENT: Final[idl.types.uint8] = 2
    RESPONSE_RECEIVED: Final[idl.types.uint8] = 3

    event_type: idl.types.uint8 = 0
    stamp: Time = field(default_factory=lambda *_: Time())
    client_gid: idl.types.array[idl.types.uint8, 16] = field(
        default_factory=lambda *_: [0] * 16
    )
    sequence_number: idl.types.int64 = 0
