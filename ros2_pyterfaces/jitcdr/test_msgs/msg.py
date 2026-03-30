from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..builtin_interfaces.msg import Duration, Time

class Builtins(JitStruct):
    __idl_typename__ = 'test_msgs/msg/Builtins'
    duration_value: Duration = msgspec.field(default_factory=Duration)
    time_value: Time = msgspec.field(default_factory=Time)
