"""Tests for JointState serialization with large element counts.

Reproduces bugs where cydr fails to deserialize JointState messages
serialized by ROS2 when:
- The payload includes trailing alignment padding from DDS/RTPS transports.
- Some float64 sequences are empty while others are populated, causing
  ROS serializers to emit extra per-sequence alignment padding that
  cydr must tolerate.
"""

import numpy as np
import pytest
from rclpy.serialization import deserialize_message, serialize_message
from sensor_msgs.msg import JointState as RosJointState

from ros2_pyterfaces.cydr.sensor_msgs.msg import JointState


def _make_joint_state(
    n_joints: int,
    *,
    position: bool = True,
    velocity: bool = True,
    effort: bool = True,
) -> JointState:
    """Build a cydr JointState with *n_joints* name entries.

    Each of *position*, *velocity*, *effort* controls whether that
    sequence is populated (length *n_joints*) or left empty.
    """
    names = np.array([f"joint_{i}".encode() for i in range(n_joints)], dtype=np.bytes_)
    return JointState(
        name=names,
        position=np.arange(n_joints, dtype=np.float64) if position else np.empty(0, dtype=np.float64),
        velocity=np.arange(n_joints, dtype=np.float64) * 0.1 if velocity else np.empty(0, dtype=np.float64),
        effort=np.arange(n_joints, dtype=np.float64) * 0.01 if effort else np.empty(0, dtype=np.float64),
    )


JOINT_COUNTS = [2**n for n in range(15)]

# Every combination of which float64 sequences are present vs empty.
FIELD_COMBOS = [
    {"position": True, "velocity": True, "effort": True},
    {"position": True, "velocity": True, "effort": False},
    {"position": True, "velocity": False, "effort": True},
    {"position": True, "velocity": False, "effort": False},
    {"position": False, "velocity": True, "effort": True},
    {"position": False, "velocity": True, "effort": False},
    {"position": False, "velocity": False, "effort": True},
    {"position": False, "velocity": False, "effort": False},
]

FIELD_COMBO_IDS = [
    "".join(k[0] for k, v in combo.items() if v) or "none"
    for combo in FIELD_COMBOS
]


@pytest.mark.parametrize("n_joints", JOINT_COUNTS, ids=[f"{n}j" for n in JOINT_COUNTS])
@pytest.mark.parametrize("fields", FIELD_COMBOS, ids=FIELD_COMBO_IDS)
class TestBigJointStateRoundtrip:
    """Roundtrip tests for JointState at various sizes and empty-field combos."""

    def test_cydr_roundtrip(self, n_joints: int, fields: dict) -> None:
        """cydr serialize -> cydr deserialize."""
        msg = _make_joint_state(n_joints, **fields)
        raw = msg.serialize()
        roundtrip = JointState.deserialize(raw)
        assert roundtrip.to_core_message() == msg.to_core_message()

    def test_ros_serialize_cydr_deserialize(self, n_joints: int, fields: dict) -> None:
        """ROS2 serialize -> cydr deserialize."""
        msg = _make_joint_state(n_joints, **fields)
        ros_bytes = serialize_message(msg.to_ros())
        cydr_roundtrip = JointState.deserialize(ros_bytes)
        assert cydr_roundtrip.to_core_message() == msg.to_core_message()

    def test_cydr_serialize_ros_deserialize(self, n_joints: int, fields: dict) -> None:
        """cydr serialize -> ROS2 deserialize."""
        msg = _make_joint_state(n_joints, **fields)
        cydr_bytes = bytes(msg.serialize())
        ros_roundtrip = deserialize_message(cydr_bytes, RosJointState)
        cydr_from_ros = JointState.from_ros(ros_roundtrip)
        assert cydr_from_ros.to_core_message() == msg.to_core_message()


TRAILING_PAD_SIZES = [1, 2, 3, 4, 5, 6, 7]


@pytest.mark.parametrize("n_joints", JOINT_COUNTS, ids=[f"{n}j" for n in JOINT_COUNTS])
@pytest.mark.parametrize("pad", TRAILING_PAD_SIZES, ids=[f"pad{p}" for p in TRAILING_PAD_SIZES])
class TestBigJointStateTrailingPadding:
    """Deserialize with trailing padding bytes appended by DDS/RTPS transports."""

    def test_ros_serialize_with_trailing_padding_cydr_deserialize(
        self, n_joints: int, pad: int
    ) -> None:
        msg = _make_joint_state(n_joints)
        expected_core = msg.to_core_message()

        ros_bytes = bytes(serialize_message(msg.to_ros()))
        padded = ros_bytes + b"\x00" * pad

        roundtrip = JointState.deserialize(padded)
        assert roundtrip.to_core_message() == expected_core

    def test_cydr_serialize_with_trailing_padding_cydr_deserialize(
        self, n_joints: int, pad: int
    ) -> None:
        msg = _make_joint_state(n_joints)
        expected_core = msg.to_core_message()

        cydr_bytes = bytes(msg.serialize())
        padded = cydr_bytes + b"\x00" * pad

        roundtrip = JointState.deserialize(padded)
        assert roundtrip.to_core_message() == expected_core
