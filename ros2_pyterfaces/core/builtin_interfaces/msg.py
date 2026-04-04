from .. import Array, BoundedString, CoreSchema, Sequence

Time: CoreSchema = {
    "__typename": "builtin_interfaces/msg/Time",
    "sec": "int32",
    "nanosec": "uint32",
}

Duration: CoreSchema = {
    "__typename": "builtin_interfaces/msg/Duration",
    "sec": "int32",
    "nanosec": "uint32",
}

__all__ = [
    "Time",
    "Duration",
]
