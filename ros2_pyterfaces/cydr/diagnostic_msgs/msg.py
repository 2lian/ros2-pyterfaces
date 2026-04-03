from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..std_msgs.msg import Header

class KeyValue(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/msg/KeyValue'
    key: types.string = b''
    value: types.string = b''

class DiagnosticStatus(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/msg/DiagnosticStatus'
    __unsupported_reason__ = 'values is a collection of messages, which cydr does not support'
    pass

class DiagnosticArray(JitStruct):
    __idl_typename__ = 'diagnostic_msgs/msg/DiagnosticArray'
    __unsupported_reason__ = 'status is a collection of messages, which cydr does not support'
    pass
