from dataclasses import dataclass, field

from ..idl import IdlStruct, types


@dataclass
class UUID(IdlStruct, typename="unique_identifier_msgs/msg/UUID"):
    uuid: types.array[types.uint8, 16] = field(default_factory=lambda: bytes(16))
