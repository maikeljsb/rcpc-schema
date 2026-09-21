# Capability Map: Product Process Graph Contract

Approved 2026-09-10. This map is the index of module specs: each module id names a `SPEC-<id>.md` beside this file. Implements step 1 of `docs/ideas/linkml-product-process-graph-schema.md`.

| Module id | Responsibility | Depends on |
|---|---|---|
| `toolchain` | uv project, pyproject and lockfile, `scripts/build.py` (one JSON Schema per module with the draft 2020-12 rewrite, generated docs per module), pytest harness, one CI workflow | none |
| `common` | Position, Quantity, Interval, CapabilityType, MaterialCategory, ComponentPermanence | toolchain |
| `product` | BuildingComponent, Connector (a subclass of it), Space, Storey, Material, and their enums | common |
| `resource` | Resource as the base with id and count; RobotUnit with status, holding PhysicalProperty, OperationalRequirement, Safety, Activity; Stock with permanence | common |
| `process` | PrimitiveTask and CompoundTask with Task as their base, Method with Subtask as its list entry, TaskNetwork, CompoundTaskInstance and PrimitiveTaskInstance with TaskInstance as theirs, the keyed Parameter and ParameterBinding classes, ParameterKind, and uses on Method naming a Stock | common, product, resource |

Build order: `toolchain` → `common` → `product`, `resource` → `process`.

Rules:
- Module ids are stable; they are the file names under `schema/` and the spec names here.
- Dependencies point one way. `product` and `resource` never reference each other.
- The shape of anything a module exposes is specified in that module's spec, not in its consumers'.
- Each module runs Specify → Plan → Tasks → Implement in the order above, gated on review at each phase.

Amended 2026-09-21: `MaterialCategory` added to `common`, an enum for one day and a class with its document since (`SPEC-common.md` decision 17), and the `MaterialName` type retired; `Material` added to `product` with `made_of` replacing the component's `material` slot; both when `process` moved `applies_to` onto `Method` (`SPEC-process.md` decision 19, prerequisite 7).

Amended 2026-09-21, Phase 1 of the `Stock` extension (brief, Decisions Taken by Default; `pddl-for-process.md` Appendix C): `Resource` base and `Stock` added to `resource`, `ComponentPermanence` moves from `product` to `common`, `uses` added to `process`'s `Method`. Specified in `SPEC-stock.md`, the extension spec of `resource`, with the common and process changes as its prerequisites.

Follow-up, not scheduled: `product`'s four example files by class may merge into one self-describing file split by `record_type` for validation, as `process` does (`SPEC-process.md` decision 16, `SPEC-product.md` decision 16). Recorded 2026-09-18.
