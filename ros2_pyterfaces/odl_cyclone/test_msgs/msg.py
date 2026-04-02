from dataclasses import dataclass, field

from ..builtin_interfaces.msg import Duration, Time
from ..idl import IdlStruct


@dataclass
class Builtins(IdlStruct, typename="test_msgs/msg/Builtins"):
    duration_value: Duration = field(default_factory=Duration)
    time_value: Time = field(default_factory=Time)
