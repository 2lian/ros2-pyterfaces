"""
Deterministic pseudo-random generators for IDL messages.
"""

import hashlib
import inspect
import random
import string
from typing import Any, TypeVar, get_args, get_origin

from .. import idl
from .idl import message_field_annotations, message_field_names, unwrap_annotated

T = TypeVar("T", bound=idl.IdlStruct)
__all__ = ["msg_seed", "random_message"]

MAX_SEQUENCE_LEN = 3
MAX_STRING_LEN = 12
STRING_ALPHABET = string.ascii_letters + string.digits + "_-/"
INTEGER_BOUNDS = {
    "byte": (0, 255),
    "int8": (-128, 127),
    "uint8": (0, 255),
    "int16": (-32768, 32767),
    "uint16": (0, 65535),
    "int32": (-(2**31), 2**31 - 1),
    "uint32": (0, 2**32 - 1),
    "int64": (-(2**63), 2**63 - 1),
    "uint64": (0, 2**64 - 1),
}


def msg_seed(msg_type: type[idl.IdlStruct]) -> int:
    """
    Build a stable default seed for a message type.

    Args:
        msg_type: IDL struct type to seed from.

    Returns:
        Deterministic integer seed derived from the ROS type name.
    """
    digest = hashlib.sha256(msg_type.get_type_name().encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def random_message(msg_type: type[T], seed: int | None = None) -> T:
    """
    Generate a deterministic pseudo-random instance of an IDL struct type.

    If ``seed`` is omitted, a stable seed derived from the message type name is
    used. The same type therefore produces the same random value by default,
    which is useful for repeatable tests.

    Args:
        msg_type: IDL struct type to instantiate.
        seed: Optional explicit random seed override.

    Returns:
        A populated IDL struct instance.
    """
    rng = random.Random(msg_seed(msg_type) if seed is None else seed)
    return _random_struct(msg_type, rng)


def _random_struct(msg_type: type[T], rng: random.Random) -> T:
    type_hints = message_field_annotations(msg_type, include_extras=True)
    kwargs = {
        field_name: _random_value(type_hints[field_name], rng)
        for field_name in message_field_names(msg_type)
    }
    return msg_type(**kwargs)


def _random_value(annotation: Any, rng: random.Random) -> Any:
    base_type, metadata = unwrap_annotated(annotation)

    sequence_meta = next(
        (item for item in metadata if hasattr(item, "subtype")),
        None,
    )
    if sequence_meta is not None:
        elem_type = sequence_meta.subtype
        fixed_length = getattr(sequence_meta, "length", None)
        max_length = getattr(sequence_meta, "max_length", None)
        size = (
            fixed_length
            if fixed_length is not None
            else _random_length(rng, max_length)
        )
        values = [_random_value(elem_type, rng) for _ in range(size)]
        if _is_uint8_scalar_annotation(elem_type):
            return bytes(values)
        return values

    bounded_str_meta = next(
        (item for item in metadata if hasattr(item, "max_length")),
        None,
    )
    if bounded_str_meta is not None:
        return _random_string(rng, max_length=bounded_str_meta.max_length)

    scalar_marker = next((item for item in metadata if isinstance(item, str)), None)
    if scalar_marker is not None:
        return _random_scalar(base_type, scalar_marker, rng)

    origin = get_origin(base_type)
    if origin is not None:
        args = get_args(base_type)
        if origin is list and args:
            return [
                _random_value(args[0], rng) for _ in range(_random_length(rng, None))
            ]

    if inspect.isclass(base_type) and issubclass(base_type, idl.IdlStruct):
        return _random_struct(base_type, rng)
    if base_type is str:
        return _random_string(rng)
    if base_type is bool:
        return bool(rng.getrandbits(1))
    if base_type is int:
        return rng.randint(-1024, 1024)
    if base_type is float:
        return _random_float(rng)
    raise TypeError(f"Unsupported annotation: {annotation!r}")


def _random_length(rng: random.Random, max_length: int | None) -> int:
    upper = (
        MAX_SEQUENCE_LEN if max_length is None else min(MAX_SEQUENCE_LEN, max_length)
    )
    return rng.randint(1, upper)


def _random_string(rng: random.Random, max_length: int | None = None) -> str:
    upper = MAX_STRING_LEN if max_length is None else min(MAX_STRING_LEN, max_length)
    size = rng.randint(1, upper)
    return "".join(rng.choice(STRING_ALPHABET) for _ in range(size))


def _random_scalar(base_type: Any, scalar_type: str, rng: random.Random) -> Any:
    if base_type is bool:
        return bool(rng.getrandbits(1))
    if base_type is float or scalar_type.startswith("float"):
        return _random_float(rng)
    if base_type is int or scalar_type in INTEGER_BOUNDS:
        lower, upper = INTEGER_BOUNDS.get(scalar_type, (-1024, 1024))
        return rng.randint(lower, upper)
    raise TypeError(f"Unsupported scalar annotation: {base_type!r}, {scalar_type!r}")


def _random_float(rng: random.Random) -> float:
    numerator = rng.randrange(-4096, 4097)
    if numerator == 0:
        numerator = 1
    return numerator / 8.0


def _is_uint8_scalar_annotation(annotation: Any) -> bool:
    base_type, metadata = unwrap_annotated(annotation)
    return base_type is int and "uint8" in metadata
