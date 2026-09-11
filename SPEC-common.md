# Spec: common

*Module `common` of `CAPABILITY-MAP.md`. Approved 2026-09-11. Depends on `toolchain` (complete). Imported by `product`, `resource`, and `process`.*

## Objective

Define the shared vocabulary every other module imports: the two value types, `Position` and `Quantity`, the `MaterialName` string type that joins product to process, the closed set of parameter kinds, and the capability vocabulary that the process side requires and the resource side offers. Deliver it as `schema/common.yaml`, the first real module through the toolchain, with its example document, generated JSON Schema, and generated documentation.

**Users.** The three domain modules, which import it and must not redefine anything it provides. Other project teams, who read `docs/model/common/` to learn what a position, a quantity, and a capability look like before they read anything else. The schema viewer, which loads `dist/common.schema.json`.

**Success in one sentence.** `schema/common.yaml` lints clean, its capability document validates, the toolchain produces its JSON Schema and docs with no changes to the toolchain, and a person from another team can add an eleventh capability type by copying a line.

**What this module deliberately is not.** It carries no domain classes, no instance-side classes, and no graph vocabulary. If a later module wants something in common, it asks; nothing moves here by default.

## Tech Stack

Inherited from `SPEC-toolchain.md` unchanged: LinkML 1.11.1 under uv on Python 3.12, `linkml-lint`, `linkml-validate`, `gen-json-schema`, `gen-doc`, pytest. This module adds no dependency.

## Commands

```
uv run linkml-lint schema/common.yaml
uv run linkml-validate -s schema/common.yaml -C CapabilityType examples/common/capability_types.yaml
uv run python scripts/build.py          # produces dist/common.schema.json, dist/README.md, docs/model/common/
uv run pytest                           # lint, examples, drift, meta-schema, all in one
```

## Project Structure

Files this module adds. Everything else already exists.

```
schema/
  common.yaml                          the module
examples/
  common/
    capability_types.yaml              the four core capability types, migrated from the reference
    invalid/
      capability_type_missing_id.yaml  one entry without an id
dist/
  common.schema.json                   generated
  README.md                            regenerated, now lists common
docs/
  model/
    common/                            generated, one page per element
tests/
  test_examples.py                     two rows added to EXAMPLES, nothing else
```

## The Model

### Schema header

```yaml
id: https://rcpc.for5672/schema/common
name: common
version: 0.1.0
description: >-
  Shared vocabulary for the Product Process Graph: the Position and Quantity value
  types, the MaterialName type that joins product to process, the closed set of
  parameter kinds, and the capability types that primitive tasks require and robot
  types offer. Imported by every other module.
prefixes:
  rcpc: https://rcpc.for5672/schema/
  linkml: https://w3id.org/linkml/
default_prefix: rcpc
default_range: string
imports:
  - linkml:types
```

### Classes

| Class | Slots | Notes |
|---|---|---|
| `Position` | `x`, `y`, `z`, all `float`, all required | A point in the IFC project frame, metres. The one frame the model uses. Always inlined by its owner; never a document on its own. |
| `Quantity` | `value` `float` required; `unit` string required | A number with a unit. UCUM case-sensitive codes recommended in the description, not enforced. Always inlined. |
| `CapabilityType` | `id` identifier; `description` required | Something a robot can do, named by a bare verb. The id is the name; no separate label. Matching is by id, no levels or qualifiers. The only document class in this module. |

### Type

| Type | Base | Notes |
|---|---|---|
| `MaterialName` | `string` | An IFC material name exactly as it appears in the model. The product side's `material` slot and the process side's `applies_to` list both use this type, and method selection joins them by exact match. Declared once so the join is visible in the docs and neither module reaches into the other for it. In generated JSON Schema it is inlined as a plain string; its meaning is carried by the docs. |

### Enum

| Enum | Values | Notes |
|---|---|---|
| `ParameterKind` | `position`, `component_reference`, `quantity` | The closed set of value kinds a task parameter may have. Each value's description names the class or reference it binds to. |

### Shared slots

`id` (`identifier: true`), `label`, `description`, `x`, `y`, `z`, `value`, `unit`. Defined here once with descriptions; domain modules reuse `id`, `label`, and `description` and never redeclare them. `id` is unique among instances of its class, not across the document set: every reference slot declares its range, so the class is always known and the id carries no namespace. `label` is for classes whose id is not readable on its own, such as a robot type; classes whose id is the name, such as CapabilityType, do not use it.

### Foreseen additions

Not in this module now. Listed so they land here, and nowhere else, when they arrive.

- **Rotation, or a Pose combining Position and Rotation.** The parameter-kinds research notes that `Detach` as a bare position drops orientation, and the product side has a rotation. Arrives with the first task that needs placement orientation, possibly as a fourth `ParameterKind`.
- **Provenance.** Dropped from `Quantity` here and deferred with Plan and Run. Arrives with execution records as a value type shared by everything that records where a fact came from.
- **Further `ParameterKind` values.** `enumeration` and `resource_reference` were deferred by the research note. Adding a value is additive.

Other shared classes are added as the project identifies them, by amending this spec first.

### Fixed by the brief

Closed parameter kinds are Position, ComponentReference, Quantity (research note `parameter-kinds-mapping.md`). Duration is a Quantity-typed slot, not a kind. CapabilityType lives here because process `requires` it and resource `offers` it. `offers` is a flat set, so CapabilityType carries no level or qualifier. One coordinate frame, no frame slot. No graph vocabulary or annotations. Every element has a description.

## Code Style

The module follows the conventions in `SPEC-toolchain.md` and the snippet in the brief. One class in full, as it will appear:

```yaml
classes:
  CapabilityType:
    description: >-
      Something a robot can do, named by a bare verb, that a PrimitiveTask requires
      and a RobotType offers. The id is the name; matching is by id and there are no
      levels or qualifiers. Type-level allocation asks whether a robot type offers
      every capability a task requires.
    slots:
      - id
      - description
    slot_usage:
      description:
        required: true
```

Conventions specific to this module:

- **Value objects state that they are inlined** in their description, so a reader of `docs/model/common/Position.md` knows it is never a document on its own. The `inlined: true` itself is set by the owning slot in the consuming module, because inlining is a property of the slot in LinkML.
- **Descriptions state the decision, not the history.** "Matching is by identifier; there are no levels" rather than the reasoning that led there.
- **Capability descriptions are migrated from the reference, with "element" replaced by "component"** and nothing else changed unless a sentence no longer makes sense. The vocabulary is a starting point, open to revision; capabilities are added when a method needs them.
- **Capability ids are bare verbs**, `locomote`, `grip`, `lift`, `align`, and every future capability follows: a capability is something a robot can *do*. The id is the name, so there is no label; descriptions open with the verb.
- **No `tree_root`.** See Decisions Made Here.

## Testing Strategy

No new test files. This module lights up the tests the toolchain left waiting and adds two rows to one table.

| Test | What it proves for common | Change |
|---|---|---|
| `test_lint.py` | `schema/common.yaml` lints clean | none, it collects the file |
| `test_examples.py` | `capability_types.yaml` validates against `CapabilityType`; `capability_type_missing_id.yaml` fails naming `id` | two rows in `EXAMPLES` |
| `test_dist.py` | committed `dist/common.schema.json` and `docs/model/common/` equal a fresh build; the schema passes the 2020-12 meta-schema | none, it collects the files |
| `test_build.py` | unchanged; still runs on the fixture | none |

`Position` and `Quantity` have no example document because they are never top-level. They are exercised by the first consumer module's examples. If that feels like a gap, the mitigation is a fixture-style probe, not a container class.

## Boundaries

**Always.** Every class, slot, enum, and permissible value has a description. Rebuild `dist/` and `docs/model/` in the same commit as the YAML. `uv run pytest` passes before committing. Conventional Commits. LF.

**Ask first.** Adding a class, type, slot, or enum value beyond the ones listed under The Model, including the foreseen additions before their trigger arrives. Adding a fourth parameter kind. Making `unit` an enum. Changing the schema `id` or prefix. Moving anything into common from another module.

**Never.** `tree_root: true` on any class. Graph vocabulary or annotations. Hand edits under `dist/` or `docs/model/`. Redefining `id`, `label`, or `description` in another module. A container or payload class.

## Success Criteria

1. `uv run pytest` passes with `test_lint.py` and `test_dist.py` no longer skipped: 1 lint test, 1 meta-schema test, and 2 new example rows collected and passing.
2. `dist/common.schema.json` exists, declares draft 2020-12, passes the meta-schema check, and its `$defs` contain exactly `Position`, `Quantity`, `CapabilityType`, and `ParameterKind`. `MaterialName` does not appear: LinkML inlines types onto the slots that use them by default, so a `MaterialName` slot renders as a plain string, which is the preferred rendering for the viewer. Its root has no `properties` of its own, confirming the no-`tree_root` decision. Both behaviours verified on a probe, 2026-09-11.
3. `dist/README.md` lists `common.schema.json` with the module description.
4. `docs/model/common/index.md` lists three classes, eight slots (`label` among them, defined for later modules), one enum, and one type, `MaterialName`. Every page has a description.
5. `examples/common/capability_types.yaml` contains the four core capability types, `locomote`, `grip`, `lift`, `align`, with `id` and `description` only; every id is a bare verb and the word "element" appears in none of them.
6. Another team's check: given only `docs/model/common/`, a person adds an eleventh capability type to the example file and `uv run pytest` still passes. Recorded as done when it has happened once; not blocking.
7. The toolchain was not changed. `git log -- scripts tests/test_build.py tests/test_lint.py tests/test_dist.py` shows no commit from this module.

## Decisions Made Here (for review)

1. **Position is an object, not an array.** The reference used a three-number array. An object flattens to `x`, `y`, `z` properties in the graph and is unambiguous in YAML.
2. **Quantity drops `provenance`.** Deferred to Plan and Run with the rest of provenance.
3. **`unit` is a free string, UCUM recommended.** Enforcing a unit vocabulary is a later decision that the graph would inherit; nothing in step 1 needs it.
4. **The four core capabilities migrate; the other six reference entries do not.** Revised 2026-09-11: the vocabulary is open for improvement, so the example holds only what the reference primitives require and the brief's allocation example names. Others return one at a time when a method needs them.
5. **`description` required on CapabilityType; no `label`.** Revised 2026-09-11: the id is the verb and a label would repeat it. `label` stays a shared slot for classes such as RobotType whose id is not a readable name.
6. **Capability ids are bare verbs.** Decided 2026-09-11: the reference's noun ids (`locomotion`, `gripper`, `lifting`, `alignment`) become `locomote`, `grip`, `lift`, `align`, because a capability names something a robot can do. Bare verbs over gerunds for brevity and because `requires: [lift, align]` reads naturally.
7. **`id` is unique among instances of its class, with no namespace prefix.** Decided 2026-09-11. In the graph the node label is the namespace, and in documents every reference slot declares its range, so the class is always known. Namespaced ids such as `capability.lift` would state the class twice; opaque ids would make the hand-authored catalogue unreadable. The projection's one uniqueness constraint per label enforces exactly this promise.
8. **`MaterialName` as a shared string type.** Product's `material` and process's `applies_to` are joined by exact match; one declared type makes that visible and keeps the two modules independent of each other.
9. **No `tree_root` anywhere, and no container classes.** LinkML recommends a `tree_root` container for serialisation, and that is right for a single self-contained schema. Here modules merge on import, and a probe on 2026-09-11 showed the consequence: with a container in common and another in product, product's generated schema took common's root and rejected a product document as having unexpected properties. So documents are top-level lists, validation always names the class with `-C`, and the `dist/` files are definition libraries with no root properties. Container classes without `tree_root` were considered and declined to avoid a wrapper class per module and an extra projection rule.

## Open Questions

- Does the schema viewer need a root `properties` block to render, or does it read `$defs` directly? The generated root has `$id`, `$schema`, `title`, `type`, `version`, `additionalProperties`, and `$defs`, and no `properties`. If the viewer needs a root, the fix is in the toolchain build, not in this module.
