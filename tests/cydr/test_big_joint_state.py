"""Tests for JointState serialization with large element counts.

Reproduces a bug where cydr fails to deserialize JointState messages
serialized by ROS2 when the payload includes trailing alignment padding
bytes from the DDS/RTPS transport layer (up to 7 bytes for 8-byte
alignment).  Non-CycloneDDS RMW implementations (e.g. FastRTPS) are
known to add such padding.
"""

import numpy as np
import pytest
from rclpy.serialization import deserialize_message, serialize_message
from sensor_msgs.msg import JointState as RosJointState

from ros2_pyterfaces.cydr.sensor_msgs.msg import JointState


def _make_joint_state(n_joints: int) -> JointState:
    """Build a cydr JointState with *n_joints* populated entries."""
    names = np.array([f"joint_{i}".encode() for i in range(n_joints)], dtype=np.bytes_)
    positions = np.arange(n_joints, dtype=np.float64)
    velocities = np.arange(n_joints, dtype=np.float64) * 0.1
    efforts = np.arange(n_joints, dtype=np.float64) * 0.01
    return JointState(
        name=names,
        position=positions,
        velocity=velocities,
        effort=efforts,
    )


JOINT_COUNTS = [2**n for n in range(15)]


@pytest.mark.parametrize("n_joints", JOINT_COUNTS, ids=[f"{n}j" for n in JOINT_COUNTS])
class TestBigJointStateRoundtrip:
    """Roundtrip tests for JointState at various joint counts."""

    def test_cydr_roundtrip(self, n_joints: int) -> None:
        """cydr serialize -> cydr deserialize."""
        msg = _make_joint_state(n_joints)
        raw = msg.serialize()
        roundtrip = JointState.deserialize(raw)
        assert roundtrip.to_core_message() == msg.to_core_message()

    def test_ros_serialize_cydr_deserialize(self, n_joints: int) -> None:
        """ROS2 serialize -> cydr deserialize."""
        msg = _make_joint_state(n_joints)
        ros_bytes = serialize_message(msg.to_ros())
        cydr_roundtrip = JointState.deserialize(ros_bytes)
        assert cydr_roundtrip.to_core_message() == msg.to_core_message()

    def test_cydr_serialize_ros_deserialize(self, n_joints: int) -> None:
        """cydr serialize -> ROS2 deserialize."""
        msg = _make_joint_state(n_joints)
        cydr_bytes = bytes(msg.serialize())
        ros_roundtrip = deserialize_message(cydr_bytes, RosJointState)
        cydr_from_ros = JointState.from_ros(ros_roundtrip)
        assert cydr_from_ros.to_core_message() == msg.to_core_message()


TRAILING_PAD_SIZES = [1, 2, 3, 4, 5, 6, 7]


@pytest.mark.parametrize("n_joints", JOINT_COUNTS, ids=[f"{n}j" for n in JOINT_COUNTS])
@pytest.mark.parametrize("pad", TRAILING_PAD_SIZES, ids=[f"pad{p}" for p in TRAILING_PAD_SIZES])
class TestBigJointStateTrailingPadding:
    """Deserialize ROS-serialized JointState with trailing padding bytes.

    DDS/RTPS transports (notably non-CycloneDDS RMW implementations)
    may append up to 7 zero bytes to align the serialized payload within
    RTPS submessages.  cydr must tolerate these trailing bytes.
    """

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
