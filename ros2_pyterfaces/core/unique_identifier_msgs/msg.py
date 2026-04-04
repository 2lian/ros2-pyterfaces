from .. import Array, BoundedString, CoreSchema, Sequence

UUID: CoreSchema = {
    "__typename": "unique_identifier_msgs/msg/UUID",
    "uuid": Array("uint8", 16),
}

__all__ = [
    "UUID",
]
