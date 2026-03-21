import hashlib
from dataclasses import dataclass, fields
from typing import (
    Any,
    Final,
    Literal,
    Mapping,
    Optional,
    Self,
    Sequence,
    get_args,
    get_origin,
    get_type_hints,
)

import cyclonedds_idl as _idl

from .utils.description import (
    cyclonedds_struct_to_ros_type_description_json,
    ros2_type_hash_from_json,
)

types = _idl.types


# derive from the same metaclass Cyclone already uses
class IdlMetaIgnoreFinal(type(_idl.IdlStruct)):
    def __new__(mcls, name, bases, namespace, **kwargs):
        ann = namespace.get("__annotations__")
        if ann:
            # remove only from annotations; keep the class attributes themselves
            for key in list(ann):
                if get_origin(ann[key]) is Final:
                    ann.pop(key)
                elif get_origin(ann[key]) is Literal:
                    ann.pop(key)
        return super().__new__(mcls, name, bases, namespace, **kwargs)


class IdlStruct(_idl.IdlStruct, metaclass=IdlMetaIgnoreFinal):

    def serialize(
        self,
        buffer: Optional[_idl.Buffer] = None,
        endianness: Optional[_idl.Endianness] = None,
        use_version_2: Optional[bool] = None,
    ) -> bytes:
        if len(getattr(type(self), "__annotations__", {})) == 0:
            # ROS 2 cannot send a truly empty message with only a header
            return DummyEmpty().serialize()
        return super().serialize(buffer, endianness, use_version_2)

    @classmethod
    def json_type_description(
        cls,
        *,
        root_type_name: str | None = None,
        type_name_overrides: Mapping[type, str] | None = None,
        indent: int = 2,
    ) -> str:
        return cyclonedds_struct_to_ros_type_description_json(
            cls,
            root_type_name=root_type_name,
            type_name_overrides=type_name_overrides,
            indent=indent,
        )

    @classmethod
    def _hash_rihs01_raw(cls) -> hashlib._hashlib.HASH:
        """ROS 2 RIHS01 hash"""
        return ros2_type_hash_from_json(cls.json_type_description())

    @classmethod
    def hash_rihs01(cls) -> str:
        """ROS 2 RIHS01 hash as string prepended with RIHS01_"""
        return f"RIHS01_{cls._hash_rihs01_raw().hexdigest()}"

    @classmethod
    def get_type_name(cls) -> str:
        return getattr(cls, "__idl_typename__", "")

    @classmethod
    def get_ros_type(cls) -> type:
        from importlib import import_module

        module_name, class_name = cls.get_type_name().replace("/", ".").rsplit(".", 1)
        mod = import_module(module_name)
        return getattr(mod, class_name)

    @classmethod
    def from_ros(cls, msg: object) -> Self:
        """
        Convert a ROS Python message instance into this IdlStruct subclass.
        """
        if isinstance(msg, cls):
            return msg

        ros_type = cls.get_ros_type()
        if not isinstance(msg, ros_type):
            raise TypeError(
                f"{cls.__name__}.from_ros() expected {ros_type.__module__}.{ros_type.__name__}, "
                f"got {type(msg).__module__}.{type(msg).__name__}"
            )

        type_hints = get_type_hints(cls)
        kwargs: dict[str, Any] = {}

        for f in fields(cls):
            if not hasattr(msg, f.name):
                raise AttributeError(
                    f"ROS message {type(msg).__module__}.{type(msg).__name__} "
                    f"has no field {f.name!r}"
                )

            dst_type = type_hints.get(f.name, f.type)
            src_value = getattr(msg, f.name)
            kwargs[f.name] = cls._from_ros_value(dst_type, src_value)
        final = cls()
        for k, v in kwargs.items():
            setattr(final, k, v)
        return final

    @classmethod
    def _from_ros_value(cls, dst_type: Any, value: Any) -> Any:
        if value is None:
            return None

        # Nested ROS message -> nested IdlStruct
        if isinstance(dst_type, type) and issubclass(dst_type, IdlStruct):
            return dst_type.from_ros(value)

        # sequence[...] / array[...] / list[...] style annotations
        args = get_args(dst_type) or getattr(dst_type, "__args__", ())
        if (
            args
            and isinstance(value, Sequence)
            and not isinstance(value, (str, bytes, bytearray))
        ):
            elem_type = args[0]
            return [cls._from_ros_value(elem_type, item) for item in value]

        # bytes -> int
        if isinstance(value, bytes):
            return int.from_bytes(value)

        # Primitive / already compatible
        return value


@dataclass
class DummyEmpty(IdlStruct, typename="does/not/matter/empty"):
    structure_needs_at_least_one_member: types.uint32 = 0
