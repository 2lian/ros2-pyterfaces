from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct

class UUID(JitStruct):
    __idl_typename__ = 'unique_identifier_msgs/msg/UUID'
    uuid: types.NDArray[types.Shape["16"], types.UInt8] = msgspec.field(default_factory=lambda: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8))
