# Capability Map: Product Process Graph Contract

Approved 2026-09-10. This map is the index of module specs: each module id names a `SPEC-<id>.md` beside this file. Implements step 1 of `docs/ideas/linkml-product-process-graph-schema.md`.

| Module id | Responsibility | Depends on |
|---|---|---|
| `toolchain` | uv project, pyproject and lockfile, `scripts/build.py` (one JSON Schema per module with the draft 2020-12 rewrite, generated docs per module), pytest harness, one CI workflow | none |
| `common` | Position, Quantity, Interval, ParameterKind, CapabilityType | toolchain |
| `product` | BuildingComponent, Connector (a subclass of it), Space, Storey, and their enums | common |
| `resource` | RobotUnit with id, count and status; PhysicalProperty, OperationalRequirement, Safety, Activity | common |
| `process` | PrimitiveTask, CompoundTask, Method, Subtask, Precedence, the instantiated task classes | common, product, resource |

Build order: `toolchain` → `common` → `product`, `resource` → `process`.

Rules:
- Module ids are stable; they are the file names under `schema/` and the spec names here.
- Dependencies point one way. `product` and `resource` never reference each other.
- The shape of anything a module exposes is specified in that module's spec, not in its consumers'.
- Each module runs Specify → Plan → Tasks → Implement in the order above, gated on review at each phase.
