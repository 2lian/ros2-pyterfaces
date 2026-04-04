from dataclasses import dataclass
from ..idl import IdlStruct, Time, types

Time.__module__ = __name__

@dataclass
class Duration(IdlStruct, typename="builtin_interfaces/msg/Duration"):
    sec: types.int32 = 0
    nanosec: types.uint32 = 0
