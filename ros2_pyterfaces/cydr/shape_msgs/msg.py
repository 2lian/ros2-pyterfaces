from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..geometry_msgs.msg import Point, Polygon

class MeshTriangle(JitStruct):
    __idl_typename__ = 'shape_msgs/msg/MeshTriangle'
    vertex_indices: types.NDArray[types.Shape["3"], types.UInt32] = msgspec.field(default_factory=lambda: np.array([0, 0, 0], dtype=np.uint32))

class Plane(JitStruct):
    __idl_typename__ = 'shape_msgs/msg/Plane'
    coef: types.NDArray[types.Shape["4"], types.Float64] = msgspec.field(default_factory=lambda: np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float64))

class SolidPrimitive(JitStruct):
    __idl_typename__ = 'shape_msgs/msg/SolidPrimitive'
    __unsupported_reason__ = 'polygon references unsupported message Polygon'
    type: types.uint8 = np.uint8(0)
    dimensions: types.NDArray[Any, types.Float64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.float64))
    polygon: Polygon = msgspec.field(default_factory=Polygon)

class Mesh(JitStruct):
    __idl_typename__ = 'shape_msgs/msg/Mesh'
    __unsupported_reason__ = 'triangles is a collection of messages, which cydr does not support'
    pass
