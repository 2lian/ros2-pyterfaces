# Testing

`ros2_pyterfaces` is tested in a few short but important layers:

- Import and generation checks make sure the replicated interfaces and service wrappers load correctly.
- Hash and type-description tests verify the ROS-facing metadata stays aligned.
- Conversion tests check `to_ros()`, `from_ros()`, and plain-data normalization on defaults and populated values.
- Serialization tests compare raw IDL serialization and ROS serialization/deserialization for message and service types.
- Randomized fuzz-style tests generate deterministic random messages across all supported types and roundtrip them repeatedly.
- Raw pub/sub interoperability tests exercise actual ROS-side send/receive paths, including raw payload transport.

The goal is simple: ensure the library stays reliable and interoperable with ROS 2, not just internally consistent.
