# Spec: stock

*Extension of module `resource` of `CAPABILITY-MAP.md`; Phase 1 decided 2026-09-21, spec for review. A quick demo, not a full module: the plainest mechanism that makes Appendix C of `docs/research/pddl-for-process.md` reproducible from the documents. Changes `resource`, with one prerequisite change each in `common` and `process`.*

## Objective

Let a planner see the stock a method draws on, so that two components run side by side when the stock suffices and one after the other when it does not, with no order imposed between them. A `Stock` beside `RobotUnit` under one `Resource` base, and `uses` on `Method` naming the stocks it holds.

**Success in one sentence.** The stock and catalogue examples validate, every `uses` id resolves to a stock record, and Appendix C shows a planner sequencing two walls on one formwork set and running them side by side on two, from exactly these fields.

**Not in this spec.** No parameter kind, no binding of a unit on an instance, no amount per use, no position within the method, no robot state, no export code, no scheduler. Units are interchangeable, so the plan never says which unit a component got.

## Tech Stack and Commands

Inherited from `SPEC-toolchain.md`, nothing added.

```
uv run linkml-lint schema/common.yaml schema/resource.yaml schema/process.yaml
uv run linkml-validate -s schema/resource.yaml -C Stock examples/resource/stocks.yaml
uv run python scripts/build.py
uv run pytest
```

## Project Structure

```
schema/common.yaml                     gains ComponentPermanence and permanence, from product
schema/product.yaml                    loses both; behaviour unchanged
schema/resource.yaml                   Resource base, RobotUnit is_a Resource, Stock
schema/process.yaml                    uses on Method
examples/common/capability_types.yaml  gains shutter, tie, pour
examples/resource/stocks.yaml          formwork_panels and rebar
examples/resource/robot_units.yaml     gains concreter_k1 offering the three words and locomote
examples/resource/invalid/stock_missing_permanence.yaml
examples/process/catalogue.yaml        gains Formwork, Reinforce, Concrete, m_insitu
examples/process/plan.yaml             the network gains two Level 1 slabs as an unordered pair, undecomposed
tests/test_examples.py                 two rows added
tests/test_references.py               one row added: catalogue uses -> stocks.yaml
dist/, docs/model/                     regenerated
```

## Prerequisite change to common

`ComponentPermanence` and the slot `permanence` move from `product` to `common` unchanged, because `resource` uses them too and `product` and `resource` never import each other, the rule the four dimension slots followed (`SPEC-resource.md` decision 9). `BuildingComponent` keeps `permanence` required. Product's JSON Schema does not change in content.

## The Model

| Element | Module | Shape |
|---|---|---|
| `Resource` | resource | Base class with `id` and `count`. `RobotUnit` and `Stock` are `is_a` it. Never written as a record. No `record_type`: no file mixes the two classes. |
| `count` | resource | Moves to `Resource`. How many identical units the entry stands for: machines, or units of a stock, one unit being what one method use takes. The export mints `<id>_<n>`. |
| `Stock` | resource | `is_a: Resource`, adds `permanence`, required. `id` matches `^[A-Za-z][A-Za-z0-9_]*$`, an HDDL name. `temporary`: a unit a method takes comes back when the method ends. `permanent`: it is consumed. |
| `uses` | process | On `Method`, optional, multivalued, range `Stock`: the stocks the method holds one unit of each for its whole span. A plain string in JSON Schema, resolved against `stocks.yaml` by `tests/test_references.py`. |

Case collisions checked: no slot named `stock` or `resource`.

Documents:

```yaml
# examples/resource/stocks.yaml
- id: formwork_panels
  count: 2
  permanence: temporary
- id: rebar
  count: 20
  permanence: permanent
```

```yaml
# added to examples/process/catalogue.yaml; Formwork, Reinforce, Concrete are primitives
# with parameters {r: robot, c: component, at: location}, requiring shutter, tie, pour
- record_type: Method
  id: m_insitu
  description: Cast a component in place: shutter it, tie its reinforcement, pour.
  compound_task: ConstructComponent
  applies_to: concrete
  parameters: {c: component, r: robot, at: location}
  subtasks:
    - {primitive_task: Formwork, arguments: [r, c, at]}
    - {primitive_task: Reinforce, arguments: [r, c, at]}
    - {primitive_task: Concrete, arguments: [r, c, at]}
  ordering: [[1, 2], [2, 3]]
  uses: [formwork_panels, rebar]
```

`plan.yaml`: the network, renamed `level_1`, lists the two Level 1 slabs `2O2Fr$t4X7Zf8NOew3FK4F` and `2O2Fr$t4X7Zf8NOew3FKcz` as tasks 3 and 4, no ordering pair between them, each an undecomposed `CompoundTaskInstance` like `construct_138062`.

**What the export writes** (Appendix C.3, verified): per stock an HDDL type named by its id, `count` objects, a `free` predicate, all free in `:init`; per method and stock a variable, an instantaneous take before the method's first subtask, and for a temporary stock a release after its last. The catalogue's actions are exported unchanged. One formwork set sequences two walls, two sets run them side by side, one rebar unit for two walls is unsolvable. For `m_insitu` this is the run of C.3 exactly: its take was at subtask 1 and its release at subtask 3, the method's span.

## Testing Strategy

Rows before schema, RED first. `test_examples.py`: `stocks.yaml` against `Stock` passes; `stock_missing_permanence.yaml` fails naming `permanence`. `test_references.py`: `catalogue.yaml` `uses` against `stocks.yaml`, RED with a planted unknown stock. Tests that count `$defs` or rows move to the new numbers in the same commit.

## Boundaries

**Always.** RED first. Descriptions on everything. One module per commit, common, resource, process. Rebuild `dist/` and `docs/model/` with the YAML. `uv run pytest` before committing. Conventional Commits. LF.

**Ask first.** An amount, a position, a parameter kind, a binding, a second slot on `Stock`, robot state, `record_type` in resource, an export script, a test file.

**Never.** A `stock` or `resource` slot. `abstract`, `mixins`, `union_of`, `designates_type`. Hand edits under `dist/` or `docs/model/`. Real product names.

## Success Criteria

1. `uv run pytest` passes with two example rows and one reference row added.
2. `dist/resource.schema.json` `$defs` gains `Resource`, `Stock`, `ComponentPermanence`; `dist/process.schema.json` gains `Resource` and `Stock`, 34 entries; `Stock.required` is `count`, `id`, `permanence`; `Method.properties.uses` is an array of strings and not in `Method.required`; no `"null"` added.
3. `docs/model/resource/index.md` indents `RobotUnit` and `Stock` under `Resource`; no case collision in `schema/process.yaml` with imports.
4. `catalogue.yaml` holds twelve records, `plan.yaml` eleven with a four-task network and one ordering pair; every `uses`, `requires`, and `offers` resolves, and `concreter_k1` offers what the three new primitives require.
5. `schema/product.yaml` changed only by the removal; `scripts/` and the toolchain tests did not change.

## Decisions Made Here (for review)

Decided 2026-09-21 with the author, from Appendix C.

1. **Stock is a resource, not a parameter.** Units are interchangeable; there is no optimal panel as there is an optimal robot. The export mints the variable.
2. **`uses` is a list of stock ids held for the method's whole span.** The first draft placed a take and a release at subtask positions. The author asked why; for `m_insitu` the positions equal the span, and elsewhere they only save idle stock time, never a wrong plan. Positions are additive later as an object form of the entry.
3. **One `Stock` with `permanence`, from product's own distinction.** Formwork is temporary and comes back; rebar is permanent and is consumed. The export branches on the value, which is what enums are for (`SPEC-common.md` decision 17).
4. **`Resource` is the base with `id` and `count`.** The author's shape; `status` stays on `RobotUnit`.
5. **`ComponentPermanence` and `permanence` move to common.** Two modules use them.
6. **Robots keep their treatment.** Appendix C.1 shows one machine doing two formworks at once; the author judged machine allocation orchestration's question, not a count the planner consumes.
7. **One catalogue, one plan.** In-situ concreting joins the masonry catalogue so `applies_to` selects between two method families for one compound task; the network gains an unordered pair beside its ordered one.
8. **Product and resource stay separate; a stock is not joined to the component it becomes.** A formwork component would be a derived temporary `BuildingComponent`, `derived_from` its wall; rebar the same, permanent. The author decided that nothing joins such a component to the `Stock` it comes from: product and resource never reference each other, and a vocabulary in common that both name, as `MaterialCategory` joins product to process, would say what a wall consumes rather than what it is made of, a second vocabulary for a demo. The path, where a query needs it, is method `uses` stock, method decomposes the task for the wall, component `derived_from` the wall.

## Open Questions

None.
