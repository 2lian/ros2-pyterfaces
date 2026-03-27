import os
from enum import StrEnum
from importlib import util


class Distro(StrEnum):
    HUMBLE = "humble"
    JAZZY = "jazzy"
    KILTED = "kilted"


def _parse_distro(value: str | None) -> Distro | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    for distro in Distro:
        if distro.value == normalized:
            return distro
    return None


def _detect_distro() -> Distro:
    configured = _parse_distro(os.environ.get("DISTRO")) or _parse_distro(
        os.environ.get("ROS_DISTRO")
    )
    if configured is not None:
        return configured

    if _looks_like_humble():
        return Distro.HUMBLE

    return Distro.JAZZY


def _looks_like_humble() -> bool:
    if util.find_spec("service_msgs") is None:
        return True
    if util.find_spec("type_description_interfaces") is None:
        return True

    try:
        from sensor_msgs.msg import Range as RosRange
    except (ImportError, ModuleNotFoundError):
        return False

    return "variance" not in RosRange.get_fields_and_field_types()


DISTRO = _detect_distro()


__all__ = ["DISTRO", "Distro"]
