from .. import Array, BoundedString, CoreSchema, Sequence

from ..builtin_interfaces.msg import Time

StatisticDataType: CoreSchema = {
    "__typename": "statistics_msgs/msg/StatisticDataType",
}

StatisticDataPoint: CoreSchema = {
    "__typename": "statistics_msgs/msg/StatisticDataPoint",
    "data_type": "uint8",
    "data": "float64",
}

MetricsMessage: CoreSchema = {
    "__typename": "statistics_msgs/msg/MetricsMessage",
    "measurement_source_name": "string",
    "metrics_source": "string",
    "unit": "string",
    "window_start": Time,
    "window_stop": Time,
    "statistics": Sequence(StatisticDataPoint),
}

__all__ = [
    "StatisticDataType",
    "StatisticDataPoint",
    "MetricsMessage",
]
