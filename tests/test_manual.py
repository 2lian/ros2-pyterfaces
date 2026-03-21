from typing import Tuple

import pytest

import ros2_pyterfaces
from ros2_pyterfaces import idl
from ros2_pyterfaces.diagnostic_msgs.msg import KeyValue
from ros2_pyterfaces.sensor_msgs.msg import JointState
from ros2_pyterfaces.std_msgs.msg import String


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


