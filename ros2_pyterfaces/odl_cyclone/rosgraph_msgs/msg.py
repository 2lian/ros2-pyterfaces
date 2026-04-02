from dataclasses import dataclass, field

from ..builtin_interfaces.msg import Time
from ..idl import IdlStruct


@dataclass
class Clock(IdlStruct, typename="rosgraph_msgs/msg/Clock"):
    clock: Time = field(default_factory=Time)
