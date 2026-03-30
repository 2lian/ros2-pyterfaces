from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct

class Time(JitStruct):
    __idl_typename__ = 'builtin_interfaces/msg/Time'
    sec: types.int32 = np.int32(0)
    nanosec: types.uint32 = np.uint32(0)

class Duration(JitStruct):
    __idl_typename__ = 'builtin_interfaces/msg/Duration'
    sec: types.int32 = np.int32(0)
    nanosec: types.uint32 = np.uint32(0)
