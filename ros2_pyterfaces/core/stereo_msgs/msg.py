from .. import Array, BoundedString, CoreSchema, Sequence

from ..sensor_msgs.msg import Image, RegionOfInterest
from ..std_msgs.msg import Header

DisparityImage: CoreSchema = {
    "__typename": "stereo_msgs/msg/DisparityImage",
    "header": Header,
    "image": Image,
    "f": "float32",
    "t": "float32",
    "valid_window": RegionOfInterest,
    "min_disparity": "float32",
    "max_disparity": "float32",
    "delta_d": "float32",
}

__all__ = [
    "DisparityImage",
]
