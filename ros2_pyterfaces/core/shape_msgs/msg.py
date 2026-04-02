from .. import Array, BoundedString, CoreSchema, Sequence

from ..geometry_msgs.msg import Point, Polygon

MeshTriangle: CoreSchema = {
    "__typename": "shape_msgs/msg/MeshTriangle",
    "vertex_indices": Array("uint32", 3),
}

Plane: CoreSchema = {
    "__typename": "shape_msgs/msg/Plane",
    "coef": Array("float64", 4),
}

SolidPrimitive: CoreSchema = {
    "__typename": "shape_msgs/msg/SolidPrimitive",
    "type": "uint8",
    "dimensions": Sequence("float64", 3),
    "polygon": Polygon,
}

Mesh: CoreSchema = {
    "__typename": "shape_msgs/msg/Mesh",
    "triangles": Sequence(MeshTriangle),
    "vertices": Sequence(Point),
}

__all__ = [
    "MeshTriangle",
    "Plane",
    "SolidPrimitive",
    "Mesh",
]
