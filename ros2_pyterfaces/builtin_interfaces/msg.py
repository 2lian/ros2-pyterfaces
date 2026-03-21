from dataclasses import dataclass
from ..idl import IdlStruct, types

@dataclass
class Duration(IdlStruct, typename="builtin_interfaces/msg/Duration"):
    sec: types.int32 = 0
    nanosec: types.uint32 = 0


@dataclass
class Time(IdlStruct, typename="builtin_interfaces/msg/Time"):
    sec: types.int32 = 0
    nanosec: types.uint32 = 0
