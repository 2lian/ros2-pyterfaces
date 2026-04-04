from dataclasses import dataclass
from typing import Literal, TypeAlias, get_args

# Canonical core message value representation.
#
# Scalar primitives:
# - bool: bool
# - byte: (bytes | bytearray | memoryview) with len == 1
# - char: int
# - int8: int
# - uint8: int
# - int16: int
# - uint16: int
# - int32: int
# - uint32: int
# - int64: int
# - uint64: int
# - float32: float
# - float64: float
# - string: str
#
# Primitive collections:
# - Sequence("byte") / Array("byte", N): (bytes | bytearray | memoryview)
# - Sequence(<primitive != "byte">) / Array(<primitive != "byte">, N):
#   list[scalar representation of that primitive]
#
# Examples:
# - Sequence("uint8") -> list[int]
# - Array("int8", 4) -> list[int]
# - Sequence("string") -> list[str]
Primitive: TypeAlias = Literal[
    "bool",
    "byte",
    "char",
    "int8",
    "uint8",
    "int16",
    "uint16",
    "int32",
    "uint32",
    "int64",
    "uint64",
    "float32",
    "float64",
    "string",
]


@dataclass(frozen=True, slots=True)
class BoundedString:
    max_length: int


@dataclass(frozen=True, slots=True)
class Sequence:
    subtype: "SchemaEntry"
    max_length: int | None = None


@dataclass(frozen=True, slots=True)
class Array:
    subtype: "SchemaEntry"
    length: int


SchemaEntry: TypeAlias = Primitive | BoundedString | Sequence | Array | "CoreSchema"
CoreSchema: TypeAlias = dict[str, SchemaEntry]

_TYPENAME_KEY = "__typename"
TYPENAME_KEY = _TYPENAME_KEY
PRIMITIVES = frozenset(get_args(Primitive))

_REQUEST_FIELD = "request_message"
_RESPONSE_FIELD = "response_message"
_EVENT_FIELD = "event_message"
_SERVICE_FIELDS = (_REQUEST_FIELD, _RESPONSE_FIELD, _EVENT_FIELD)
