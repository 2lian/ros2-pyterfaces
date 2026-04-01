from __future__ import annotations

from typing import Any, ClassVar, Literal, Mapping, Optional, Self, cast

from cydr import idl, structs
from cydr.idl import StringCollectionMode

from ..idl import IdlStruct as CoreStruct
from ..utils.idl import message_field_names


class JitStruct(structs.XcdrStruct, CoreStruct):
    __unsupported_reason__: ClassVar[str | None] = None

    @classmethod
    def _core_type(cls) -> type[CoreStruct]:
        from .converter import to_core_struct

        return cast(type[CoreStruct], to_core_struct(cls))

    @classmethod
    def json_type_description(
        cls,
        root_type_name: str | None = None,
        type_name_overrides: Mapping[type, str] | None = None,
        indent: int = 2,
    ) -> str:
        from .converter import to_core_type_name_overrides

        return cls._core_type().json_type_description(
            root_type_name=root_type_name,
            type_name_overrides=to_core_type_name_overrides(
                dict(type_name_overrides) if type_name_overrides is not None else None
            ),
            indent=indent,
        )

    @classmethod
    def _hash_rihs01_raw(cls) -> Any:
        return cls._core_type()._hash_rihs01_raw()

    @classmethod
    def hash_rihs01(cls) -> str:
        return cls._core_type().hash_rihs01()

    @classmethod
    def get_type_name(cls) -> str:
        return cls._core_type().get_type_name()

    @classmethod
    def get_ros_type(cls) -> type:
        return cls._core_type().get_ros_type()

    @classmethod
    def has_ros_type(cls) -> bool:
        return cls._core_type().has_ros_type()

    @classmethod
    def to_ros_type(cls) -> type:
        return cls._core_type().to_ros_type()

    def to_ros(self) -> object:
        from .converter import to_core_struct

        return cast(CoreStruct, to_core_struct(self)).to_ros()

    @classmethod
    def from_ros(cls, msg: object) -> Self:
        from .converter import from_core_struct

        core_value = cls._core_type().from_ros(msg)
        return cast(Self, from_core_struct(core_value, cls))

    @classmethod
    def _from_ros_value(cls, dst_type: Any, value: Any) -> Any:
        from .converter import core_value_to_jit_value, jit_annotation_to_core_annotation

        core_annotation = jit_annotation_to_core_annotation(dst_type)
        core_value = CoreStruct._from_ros_value(core_annotation, value)
        return core_value_to_jit_value(core_value, dst_type)

    @classmethod
    def _to_ros_value(cls, src_type: Any, value: Any, dst_value: Any = None) -> Any:
        from .converter import jit_annotation_to_core_annotation, jit_value_to_core_value

        core_annotation = jit_annotation_to_core_annotation(src_type)
        core_value = jit_value_to_core_value(value, core_annotation)
        return CoreStruct._to_ros_value(core_annotation, core_value, dst_value)

    @classmethod
    def deserialize(
        cls,
        data: object,
        string_collections: Optional[StringCollectionMode] = None,
    ) -> Self:
        # if len(message_field_names(cls)) == 0:
        #     DummyEmpty.deserialize(data, string_collections=string_collections)
        #     return cast(Self, cls())
        return super().deserialize(data, string_collections=string_collections)

    def serialize(self) -> bytearray:
        # if len(message_field_names(type(self))) == 0:
        #     return DummyEmpty().serialize()
        return super().serialize()


class DummyEmpty(structs.XcdrStruct):
    __idl_typename__: ClassVar[Literal["does/not/matter/empty"]] = (
        "does/not/matter/empty"
    )
    structure_needs_at_least_one_member: idl.uint8 = idl.uint8(0)
