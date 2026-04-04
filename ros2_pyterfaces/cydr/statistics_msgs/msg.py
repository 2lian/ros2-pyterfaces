from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import IdlStruct
from ..builtin_interfaces.msg import Time

class StatisticDataType(IdlStruct):
    __idl_typename__ = 'statistics_msgs/msg/StatisticDataType'

class StatisticDataPoint(IdlStruct):
    __idl_typename__ = 'statistics_msgs/msg/StatisticDataPoint'
    data_type: types.uint8 = np.uint8(0)
    data: types.float64 = np.float64(0.0)

class MetricsMessage(IdlStruct):
    __idl_typename__ = 'statistics_msgs/msg/MetricsMessage'
    __unsupported_reason__ = 'statistics is a collection of messages, which cydr does not support'
    pass
