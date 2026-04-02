import hashlib
import random
import string
from typing import Any

from .schema import get_type_name
from .types import Array, BoundedString, CoreSchema, SchemaEntry, Sequence, _TYPENAME_KEY

_MAX_SEQUENCE_LEN = 3
_MAX_STRING_LEN = 12
_STRING_ALPHABET = string.ascii_letters + string.digits + "_-/"

_INTEGER_BOUNDS = {
    "byte": (0, 255),
    "char": (0, 255),
    "int8": (-128, 127),
    "uint8": (0, 255),
    "int16": (-32768, 32767),
    "uint16": (0, 65535),
    "int32": (-(2**31), 2**31 - 1),
    "uint32": (0, 2**32 - 1),
    "int64": (-(2**63), 2**63 - 1),
    "uint64": (0, 2**64 - 1),
}


def _schema_seed(schema: CoreSchema) -> int:
    digest = hashlib.sha256(get_type_name(schema).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def _random_length(rng: random.Random, max_length: int | None) -> int:
    if max_length is None:
        upper = _MAX_SEQUENCE_LEN
    else:
        upper = min(_MAX_SEQUENCE_LEN, max_length)

    if upper <= 0:
        return 0
    return rng.randint(1, upper)


def _random_string(rng: random.Random, max_length: int | None = None) -> str:
    if max_length is None:
        upper = _MAX_STRING_LEN
    else:
        upper = min(_MAX_STRING_LEN, max_length)

    if upper <= 0:
        return ""

    size = rng.randint(1, upper)
    return "".join(rng.choice(_STRING_ALPHABET) for _ in range(size))


def _random_entry(entry: SchemaEntry, rng: random.Random) -> Any:
    if isinstance(entry, dict):
        return _random_struct(entry, rng)

    if isinstance(entry, Sequence):
        size = _random_length(rng, entry.max_length)
        if entry.subtype == "byte":
            return bytes(rng.getrandbits(8) for _ in range(size))
        return [_random_entry(entry.subtype, rng) for _ in range(size)]

    if isinstance(entry, Array):
        if entry.subtype == "byte":
            return bytes(rng.getrandbits(8) for _ in range(entry.length))
        return [_random_entry(entry.subtype, rng) for _ in range(entry.length)]

    if isinstance(entry, BoundedString):
        return _random_string(rng, max_length=entry.max_length)

    if not isinstance(entry, str):
        raise TypeError(f"Unsupported schema entry: {entry!r}")

    if entry == "bool":
        return bool(rng.getrandbits(1))
    if entry in {"float32", "float64"}:
        numerator = rng.randrange(-4096, 4097)
        if numerator == 0:
            numerator = 1
        return numerator / 8.0
    if entry == "string":
        return _random_string(rng)
    if entry in {"byte"}:
        return bytes([rng.randint(0, 255)])
    if entry in _INTEGER_BOUNDS:
        lower, upper = _INTEGER_BOUNDS[entry]
        return rng.randint(lower, upper)

    raise TypeError(f"Unsupported primitive type: {entry!r}")


def _random_struct(schema: CoreSchema, rng: random.Random) -> dict[str, Any]:
    message: dict[str, Any] = {_TYPENAME_KEY: get_type_name(schema)}
    for field_name, entry in schema.items():
        if field_name == _TYPENAME_KEY:
            continue
        message[field_name] = _random_entry(entry, rng)
    return message


def random_message(schema: CoreSchema, seed: int | None = None) -> dict[str, Any]:
    if seed is None:
        rng_seed = _schema_seed(schema)
    else:
        rng_seed = seed

    rng = random.Random(rng_seed)
    return _random_struct(schema, rng)
