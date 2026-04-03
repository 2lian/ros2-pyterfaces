from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..builtin_interfaces.msg import Time

class Clock(JitStruct):
    __idl_typename__ = 'rosgraph_msgs/msg/Clock'
    clock: Time = msgspec.field(default_factory=Time)
