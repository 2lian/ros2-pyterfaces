from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import IdlStruct
from ..sensor_msgs.msg import Image, RegionOfInterest
from ..std_msgs.msg import Header

class DisparityImage(IdlStruct):
    __idl_typename__ = 'stereo_msgs/msg/DisparityImage'
    header: Header = msgspec.field(default_factory=Header)
    image: Image = msgspec.field(default_factory=Image)
    f: types.float32 = np.float32(0.0)
    t: types.float32 = np.float32(0.0)
    valid_window: RegionOfInterest = msgspec.field(default_factory=RegionOfInterest)
    min_disparity: types.float32 = np.float32(0.0)
    max_disparity: types.float32 = np.float32(0.0)
    delta_d: types.float32 = np.float32(0.0)
