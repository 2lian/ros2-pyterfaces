from .. import Array, BoundedString, CoreSchema, Sequence

from ..builtin_interfaces.msg import Time

ServiceEventInfo: CoreSchema = {
    "__typename": "service_msgs/msg/ServiceEventInfo",
    "event_type": "uint8",
    "stamp": Time,
    "client_gid": Array("uint8", 16),
    "sequence_number": "int64",
}

__all__ = [
    "ServiceEventInfo",
]
