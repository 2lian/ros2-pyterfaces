from .. import Array, BoundedString, CoreSchema, Sequence

from ..builtin_interfaces.msg import Duration, Time

Builtins: CoreSchema = {
    "__typename": "test_msgs/msg/Builtins",
    "duration_value": Duration,
    "time_value": Time,
}

__all__ = [
    "Builtins",
]
