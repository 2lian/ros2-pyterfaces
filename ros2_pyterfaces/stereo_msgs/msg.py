from dataclasses import dataclass, field
from ..idl import IdlStruct, types
from ..sensor_msgs.msg import Image, RegionOfInterest
from ..std_msgs.msg import Header

@dataclass
class DisparityImage(IdlStruct, typename="stereo_msgs/msg/DisparityImage"):
    header: Header = field(default_factory=Header)
    image: Image = field(default_factory=Image)
    f: types.float32 = 0.0
    t: types.float32 = 0.0
    valid_window: RegionOfInterest = field(default_factory=RegionOfInterest)
    min_disparity: types.float32 = 0.0
    max_disparity: types.float32 = 0.0
    delta_d: types.float32 = 0.0
