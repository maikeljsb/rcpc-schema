# Generated schemas

Generated from `schema/` by `uv run python scripts/build.py`. Do not edit.

- `common.schema.json` (JSON Schema draft 2020-12): Shared vocabulary for the Product Process Graph: value types, the material name type, the parameter kinds, and the capability types. Imported by every other module.
- `product.schema.json` (JSON Schema draft 2020-12): Building components as planning targets. BuildingComponent identified by its IFC GlobalId, with lifetime and provenance; Connector for what a robot passes through; Space and Storey as the topology they sit in.
- `resource.schema.json` (JSON Schema draft 2020-12): Robots as resources. One RobotUnit entry per robot product, holding the four Construction Robot Schema groups and the capabilities the robot offers.
