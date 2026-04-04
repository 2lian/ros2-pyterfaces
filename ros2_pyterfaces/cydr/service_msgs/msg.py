from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import IdlStruct
from ..builtin_interfaces.msg import Time

class ServiceEventInfo(IdlStruct):
    __idl_typename__ = 'service_msgs/msg/ServiceEventInfo'
    event_type: types.uint8 = np.uint8(0)
    stamp: Time = msgspec.field(default_factory=Time)
    client_gid: types.NDArray[types.Shape["16"], types.UInt8] = msgspec.field(default_factory=lambda: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8))
    sequence_number: types.int64 = np.int64(0)
