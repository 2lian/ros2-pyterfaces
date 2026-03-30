from typing import Tuple

import pytest

import ros2_pyterfaces
from ros2_pyterfaces.cyclone import idl
from ros2_pyterfaces.cyclone.diagnostic_msgs.msg import KeyValue
from ros2_pyterfaces.cyclone.sensor_msgs.msg import JointState
from ros2_pyterfaces.cyclone.std_msgs.msg import String


@pytest.mark.parametrize(
    "couple",
    [
        (
            String,
            "RIHS01_df668c740482bbd48fb39d76a70dfd4bd59db1288021743503259e948f6b1a18",
        ),
        (
            KeyValue,
            "RIHS01_d68081eaa540288c5440753baecef0c4e16e81a5f78ad68902ded5100413bb42",
        ),
        (
            JointState,
            "RIHS01_a13ee3a330e346c9d87b5aa18d24e11690752bd33a0350f11c5882bc9179260e",
        ),
    ],
)
def test_hashes(couple: Tuple[idl.IdlStruct, str]):
    assert couple[0].hash_rihs01() == couple[1]


def test_jit_struct_methods_match_cyclone():
    pytest.importorskip("cydr")
    from ros2_pyterfaces.jitcdr.diagnostic_msgs.msg import KeyValue as JitKeyValue
    from ros2_pyterfaces.jitcdr.std_msgs.msg import String as JitString

    assert JitString.get_type_name() == String.get_type_name()
    assert JitString.hash_rihs01() == String.hash_rihs01()
    assert JitString.json_type_description() == String.json_type_description()
    assert JitString.get_ros_type() is String.get_ros_type()
    assert JitString.to_ros_type() is String.to_ros_type()

    assert JitKeyValue.get_type_name() == KeyValue.get_type_name()
    assert JitKeyValue.hash_rihs01() == KeyValue.hash_rihs01()
    assert JitKeyValue.json_type_description() == KeyValue.json_type_description()
    assert JitKeyValue.get_ros_type() is KeyValue.get_ros_type()
    assert JitKeyValue.to_ros_type() is KeyValue.to_ros_type()

    jit_msg = JitKeyValue(key=b"mode", value=b"auto")
    cyc_msg = KeyValue(key="mode", value="auto")

    assert jit_msg.to_ros() == cyc_msg.to_ros()
    assert JitKeyValue.from_ros(cyc_msg.to_ros()) == jit_msg
