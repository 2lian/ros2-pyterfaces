import inspect
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple, Type

import pytest

from ros2_pyterfaces import all_msgs, idl
from ros2_pyterfaces.all_msgs import (
    DiagnosticStatus,
    JointState,
    KeyValue,
    String,
    Trajectory,
    TrajectoryPoint,
)
from ros2_pyterfaces.std_msgs.msg import Char, Empty, Float32

TYPES: List[Type[idl.IdlStruct]] = sorted(
    {
        obj
        for obj in vars(all_msgs).values()
        if inspect.isclass(obj)
        and issubclass(obj, idl.IdlStruct)
        and obj is not idl.IdlStruct
    },
    key=lambda cls: cls.__name__,
)

# TYPES = [
#     Empty,
#     Float32,
#     TrajectoryPoint,
#     Trajectory,
#     Char,
#     DiagnosticStatus,
# ]


def get_name_hash(my_type: Type[idl.IdlStruct]) -> Tuple[str, str]:
    topic = f"/get_hash/{my_type.get_type_name()}"
    psub = subprocess.Popen(
        [
            "ros2",
            "topic",
            "echo",
            topic,
            my_type.get_type_name(),  # type: ignore
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    try:
        pinfo: subprocess.CompletedProcess[str]
        start = time.time()
        while 1:
            now = time.time()
            if now - start > 10:
                raise TimeoutError(f"Did not hear topic info for {my_type}")
            pinfo = subprocess.run(
                ["ros2", "topic", "info", topic, "-vv"],
                text=True,
                timeout=3,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if pinfo.stdout is None:
                continue
            if "Topic type: " in pinfo.stdout and "Topic type hash: " in pinfo.stdout:
                out = pinfo.stdout
                name: str = out.split("Topic type: ")[1].split("\n")[0]
                hash: str = out.split("Topic type hash: ")[1].split("\n")[0]
                if name == "" or hash == "":
                    continue
                if name is None or hash is None:
                    continue
                return name, hash
            time.sleep(0.10)
    except TimeoutError:
        psub.terminate()
        psub.wait()
        out = psub.stdout.read()
        print(out)
        if "The passed message type is invalid" in out:
            return (
                my_type.get_type_name(),
                f"Message {my_type.get_type_name()} doesn't exist in ROS 2",
            )
    finally:
        psub.terminate()
        psub.wait()
    return "we shouldn't be here", "we shouldn't be here"


@pytest.fixture(scope="module")
def restart_daemon():
    subprocess.run(
        [
            "ros2",
            "daemon",
            "stop",
        ],
    )
    subprocess.run(
        [
            "ros2",
            "daemon",
            "start",
        ],
    )


HASH_FILE = Path("./tests/ros_type_hashes.json")


@pytest.fixture(scope="module")
def save_hashes(restart_daemon) -> Dict[str, str]:
    if HASH_FILE.exists():
        with open(HASH_FILE) as f:
            return json.load(f)
    dic: Dict[str, str] = {}
    for my_type in TYPES:
        try:
            name, hash = get_name_hash(my_type)
        except TimeoutError as e:
            name, hash = get_name_hash(my_type)
        dic[name] = hash
        print(name, hash)
    print(f"Saving hashes to {HASH_FILE}")
    with open(HASH_FILE, "w") as f:
        json.dump(dic, f)
        print(f"Hashes saved at {HASH_FILE}")
    return dic


@pytest.mark.parametrize("my_type", TYPES)
def test_hashes(my_type: Type[idl.IdlStruct], save_hashes: Dict[str, str]):
    hash = save_hashes.get(my_type.get_type_name())
    if hash is None:
        pytest.fail(
            f"Message {my_type.get_type_name()} doesn't exists in hash file: {HASH_FILE}"
        )
    if "doesn't exist in ROS 2" in hash:
        pytest.xfail(
            f"Message {my_type.get_type_name()} doesn't exist in ROS 2",
        )

    assert my_type.hash_rihs01() == hash
