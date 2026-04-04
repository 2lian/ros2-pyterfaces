from .. import Array, BoundedString, CoreSchema, Sequence

from ..std_msgs.msg import Header

KeyValue: CoreSchema = {
    "__typename": "diagnostic_msgs/msg/KeyValue",
    "key": "string",
    "value": "string",
}

DiagnosticStatus: CoreSchema = {
    "__typename": "diagnostic_msgs/msg/DiagnosticStatus",
    "level": "byte",
    "name": "string",
    "message": "string",
    "hardware_id": "string",
    "values": Sequence(KeyValue),
}

DiagnosticArray: CoreSchema = {
    "__typename": "diagnostic_msgs/msg/DiagnosticArray",
    "header": Header,
    "status": Sequence(DiagnosticStatus),
}

__all__ = [
    "KeyValue",
    "DiagnosticStatus",
    "DiagnosticArray",
]
