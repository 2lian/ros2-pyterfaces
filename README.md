# ROS2 PyTerfaces

```json
{
  "type_description": {
    "type_name": "std_msgs/msg/Empty",
    "fields": [
      {
        "name": "structure_needs_at_least_one_member",
        "type": {
          "type_id": 3,
          "capacity": 0,
          "string_capacity": 0,
          "nested_type_name": ""
        },
        "default_value": ""
      }
    ]
  },
  "referenced_type_descriptions": []
}
{
  "type_description": {
    "type_name": "std_msgs/msg/Empty",
    "fields": [
      {
        "name": "structure_needs_at_least_one_member",
        "type": {
          "type_id": 3,
          "capacity": 0,
          "string_capacity": 0,
          "nested_type_name": ""
        },
        "default_value": ""
      }
    ]
  },
  "referenced_type_descriptions": []
}
```

A plain Python project that reimplements ROS 2 messages tools (notably the type
hash) and interfaces packages from `common_interfaces`
using `cyclonedds.idl.IdlStruct` dataclasses.

## Included packages

- builtin_interfaces
- diagnostic_msgs
- geometry_msgs
- nav_msgs
- sensor_msgs
- shape_msgs
- std_msgs
- std_srvs
- stereo_msgs
- trajectory_msgs
- visualization_msgs

## Structure

- `src/utils/*.py`: helper utilities, including the ROS 2 type hash
- `src/<package>/msg.py`: one message per file
- `src/<package>/srv.py`: one service per file

> [!NOTE]
> Services are represented as `<Name>_Request`, `<Name>_Response`, and a small `<Name>` wrapper exposing `Request` and `Response`.
