from dataclasses import dataclass, field
from typing import Literal

import numpy as np

from ..geometry_msgs.msg import Point, Polygon
from ..idl import IdlStruct, types


@dataclass
class MeshTriangle(IdlStruct, typename="shape_msgs/msg/MeshTriangle"):
    vertex_indices: types.array[types.uint32, 3] = field(
        default_factory=lambda: np.zeros(3, dtype=np.uint32)
    )


@dataclass
class Plane(IdlStruct, typename="shape_msgs/msg/Plane"):
    coef: types.array[types.float64, 4] = field(default_factory=lambda: np.zeros(4))


@dataclass
class SolidPrimitive(IdlStruct, typename="shape_msgs/msg/SolidPrimitive"):
    BOX: Literal[1] = 1
    SPHERE: Literal[2] = 2
    CYLINDER: Literal[3] = 3
    CONE: Literal[4] = 4
    PRISM: Literal[5] = 5
    BOX_X: Literal[0] = 0
    BOX_Y: Literal[1] = 1
    BOX_Z: Literal[2] = 2
    SPHERE_RADIUS: Literal[0] = 0
    CYLINDER_HEIGHT: Literal[0] = 0
    CYLINDER_RADIUS: Literal[1] = 1
    CONE_HEIGHT: Literal[0] = 0
    CONE_RADIUS: Literal[1] = 1
    PRISM_HEIGHT: Literal[0] = 0
    type: types.uint8 = 0
    dimensions: types.sequence[types.float64, 3] = field(default_factory=list)
    polygon: Polygon = field(default_factory=Polygon)


@dataclass
class Mesh(IdlStruct, typename="shape_msgs/msg/Mesh"):
    triangles: types.sequence[MeshTriangle] = field(default_factory=list)
    vertices: types.sequence[Point] = field(default_factory=list)
