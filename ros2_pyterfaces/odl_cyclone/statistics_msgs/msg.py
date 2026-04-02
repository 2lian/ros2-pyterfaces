from dataclasses import dataclass, field
from typing import ClassVar, Literal

from ..builtin_interfaces.msg import Time
from ..idl import IdlStruct, types


@dataclass
class StatisticDataType(IdlStruct, typename="statistics_msgs/msg/StatisticDataType"):
    STATISTICS_DATA_TYPE_UNINITIALIZED: ClassVar[Literal[0]] = 0
    STATISTICS_DATA_TYPE_AVERAGE: ClassVar[Literal[1]] = 1
    STATISTICS_DATA_TYPE_MINIMUM: ClassVar[Literal[2]] = 2
    STATISTICS_DATA_TYPE_MAXIMUM: ClassVar[Literal[3]] = 3
    STATISTICS_DATA_TYPE_STDDEV: ClassVar[Literal[4]] = 4
    STATISTICS_DATA_TYPE_SAMPLE_COUNT: ClassVar[Literal[5]] = 5


@dataclass
class StatisticDataPoint(IdlStruct, typename="statistics_msgs/msg/StatisticDataPoint"):
    data_type: types.uint8 = 0
    data: types.float64 = 0.0


@dataclass
class MetricsMessage(IdlStruct, typename="statistics_msgs/msg/MetricsMessage"):
    measurement_source_name: str = ""
    metrics_source: str = ""
    unit: str = ""
    window_start: Time = field(default_factory=Time)
    window_stop: Time = field(default_factory=Time)
    statistics: types.sequence[StatisticDataPoint] = field(default_factory=list)
