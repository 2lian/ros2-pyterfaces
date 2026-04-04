from .. import Array, BoundedString, CoreSchema, Sequence

from ..builtin_interfaces.msg import Time

Clock: CoreSchema = {
    "__typename": "rosgraph_msgs/msg/Clock",
    "clock": Time,
}

__all__ = [
    "Clock",
]
