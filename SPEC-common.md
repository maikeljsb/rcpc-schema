# Spec: common

*Module `common` of `CAPABILITY-MAP.md`. Approved 2026-09-11; `MaterialCategory` added and `MaterialName` retired 2026-09-21 (decisions 15 and 16), and `MaterialCategory` made a class with its document the same day, with the vocabulary rule and the resolution test (decision 17); `ComponentPermanence` and `permanence` arrived from product 2026-09-22 for the `Stock` extension (decision 18). Depends on `toolchain` (complete). Imported by `product`, `resource`, and `process`.*

## Objective

Define the shared vocabulary every other module imports: the three value types, `Position`, `Quantity`, and `Interval`, and the two vocabularies two modules share: the capability types that process requires and resource offers, a class, and the material categories that a product `Material` carries and process's methods name, an enum. Deliver it as `schema/common.yaml`, the first real module through the toolchain, with its example document, generated JSON Schema, and generated documentation.

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
    material_categories.yaml           the three material categories methods are written for (2026-09-21)
    invalid/
      capability_type_missing_id.yaml  one entry without an id
      material_category_missing_description.yaml  one category without a description (2026-09-21)
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
  Shared vocabulary for the Product Process Graph: value types, the material name
  type, and the capability types. Imported by every other module.
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
| `Position` | `x_coord`, `y_coord`, `z_coord`, all `float`; `unit` string; all required | Three cartesian coordinates and their unit: a point, or an extent along each axis. Site positions are in the IFC project coordinate frame, the one frame the model resolves to a Space; an owning slot may say its value is in another frame, such as a robot's own, or is an extent rather than a point. Always inlined by its owner; never a document on its own. Amended 2026-09-14, see decisions 12 and 13. |
| `Quantity` | `value` `float` required; `unit` string required | A number with a unit. UCUM case-sensitive codes are the recommended convention; not enforced and not stated in the schema. Always inlined. |
| `Interval` | `minimum`, `maximum`, both `float`; `unit` string; all required | A lower and an upper bound with their unit. Always inlined. |
| `CapabilityType` | `id` identifier; `description` required | Something a robot can do, named by a bare verb. The id is the name; no separate label. Matching is by id, no levels or qualifiers. A vocabulary class: process `requires` it, resource `offers` it, both by id. |
| `MaterialCategory` | `id` identifier; `description` required | A category of material a construction method is written for, IFC's `IfcMaterial.Category` as this project's vocabulary: `masonry`, `timber`, `concrete`. A product `Material` names one in `category`, `""` until a mapping step assigns it; a method names one in `applies_to`. Cut at the granularity methods distinguish, so every method has exactly one; a category is added to the document when a method needs it. Added 2026-09-21, decisions 15 and 17. |

### Enum

| Enum | Values | Notes |
|---|---|---|
| `ComponentPermanence` | `permanent`, `temporary` | Whether a component stays in the building, or a stock returns after use. Reinforcement is permanent, formwork temporary. No default. Declared in product from 2026-09-15; moved here 2026-09-22 with its slot `permanence`, because resource's `Stock` carries it too (decision 18). |

Common's two shared vocabularies are classes with documents, not enums, by the rule in decision 17: an enum is for a value set code branches on, and no code branches on a verb or a category. `MaterialCategory` was an enum for one day, 2026-09-21. `ComponentPermanence` passes the rule: the HDDL export branches on its value.

### Type

None since 2026-09-21. `MaterialName`, a string type for the IFC material name, was declared here from 2026-09-11 for the join between product's `material` and process's `applies_to`. Product's `Material` class now carries the string as its `id`, `applies_to` ranges `MaterialCategory`, and nothing ranges the type (decision 16).

### Shared slots

`id` (`identifier: true`), `description`, `x_coord`, `y_coord`, `z_coord`, `value`, `minimum`, `maximum`, `unit` (shared by `Quantity`, `Position`, and `Interval`), the four dimension slots `length`, `width`, `height`, `weight`, each range `Quantity`, `inlined: true`, added 2026-09-12 for resource and product, and `permanence`, range `ComponentPermanence`, moved here from product 2026-09-22 for product's `BuildingComponent` and resource's `Stock` (decision 18). Defined here once; domain modules reuse them and never redeclare them. `id` is unique among instances of its class, not across the document set: every reference slot declares its range, so the class is always known and the id carries no namespace. There is no `label` slot in common. A class whose id is not a readable name, such as a robot type, brings `label` with it when its module is specified.

### Foreseen additions

Not in this module now. Listed so they land here, and nowhere else, when they arrive.

- **Rotation, or a Pose combining Position and Rotation.** The parameter-kinds research notes that `Detach` as a bare position drops orientation, and the product side has a rotation. Arrives with the first task that needs placement orientation, possibly as a fourth `ParameterKind`.
- **Provenance.** Dropped from `Quantity` here and deferred with Plan and Run. Arrives with execution records as a value type shared by everything that records where a fact came from.
- **On `CapabilityType`:** `aliases` if a published verb is renamed and old names need a grace period; `mappings` to external ontology terms when ontology alignment begins. Explored 2026-09-11 and declined for now; `id` and `description` are enough.

Other shared classes are added as the project identifies them, by amending this spec first.

### Fixed by the brief

Duration is a Quantity-typed slot on `PrimitiveTask`, not a parameter kind. CapabilityType lives here because process `requires` it and resource `offers` it; `MaterialCategory` because a product Material names it and process names it; both are vocabularies two modules read and neither module can see the other, which is why they are here and `ParameterKind` is not. `offers` is a flat set, so CapabilityType carries no level or qualifier. One coordinate frame, no frame slot; a unit slot is not a frame slot. No graph vocabulary or annotations. Every element has a description.

## Code Style

The module follows the conventions in `SPEC-toolchain.md` and the snippet in the brief. One class in full, as it will appear:

```yaml
classes:
  CapabilityType:
    description: >-
      Something a robot can do, named by a verb. Required by primitive tasks and
      offered by robots.
    slots:
      - id
      - description
    slot_usage:
      description:
        required: true
```

Conventions specific to this module:

- **Value objects state that they are inlined** in their description, so a reader of `docs/model/common/Position.md` knows it is never a document on its own. The `inlined: true` itself is set by the owning slot in the consuming module, because inlining is a property of the slot in LinkML.
- **Descriptions are simple and descriptive.** One or two plain sentences saying what the thing is. No rationale, no history, no claims about which other things use it. This rule applies to every module and to example documents.
- **Capability descriptions are migrated from the reference, with "element" replaced by "component"** and nothing else changed unless a sentence no longer makes sense. The vocabulary is a starting point, open to revision; capabilities are added when a method needs them.
- **Capability ids are bare verbs**, `locomote`, `grip`, `lift`, `align`, and every future capability follows: a capability is something a robot can *do*. The id is the name, so there is no label; descriptions open with the verb.
- **Material category values are single lowercase nouns**, `masonry`, `timber`, `concrete`, one per kind of material a method is written for; the mapping step's not-yet is `""` on the Material, not a category. A category is added to `material_categories.yaml` when a method needs one, never to describe a model.
- **No `tree_root`.** See Decisions Made Here.

## Testing Strategy

This module lights up the tests the toolchain left waiting and adds rows to one table. Since 2026-09-21 it also has `tests/test_references.py`, the resolution test that makes the two vocabularies type safe: every `requires` and `offers` value in the examples must be an id in `capability_types.yaml`, every `category` and `applies_to` value an id in `material_categories.yaml`, and every `made_of` an id in product's `materials.yaml`; `""` passes only where the owning spec says the key may be empty. A reference to an identified class renders as a plain string in JSON Schema, so without this test nothing checks the join at all, and the same rule is the generator's tier 2 obligation.

| Test | What it proves for common | Change |
|---|---|---|
| `test_lint.py` | `schema/common.yaml` lints clean | none, it collects the file |
| `test_examples.py` | `capability_types.yaml` validates against `CapabilityType`; `capability_type_missing_id.yaml` fails naming `id`; since 2026-09-21 `material_categories.yaml` validates against `MaterialCategory` and `material_category_missing_description.yaml` fails naming `description` | four rows in `EXAMPLES` |
| `test_references.py` | every `requires`, `offers`, `category`, `applies_to`, and `made_of` value in the examples resolves in its vocabulary or record file | one row per document and slot, added 2026-09-21 |
| `test_dist.py` | committed `dist/common.schema.json` and `docs/model/common/` equal a fresh build; the schema passes the 2020-12 meta-schema | none, it collects the files |
| `test_build.py` | unchanged; still runs on the fixture | none |

`Position`, `Quantity`, and `Interval` have no example document because they are never top-level. They are exercised by the first consumer module's examples. If that feels like a gap, the mitigation is a fixture-style probe, not a container class.

## Boundaries

**Always.** Every class, slot, enum, and permissible value has a description. Rebuild `dist/` and `docs/model/` in the same commit as the YAML. `uv run pytest` passes before committing. Conventional Commits. LF.

**Ask first.** Adding a class, type, slot, or enum value beyond the ones listed under The Model, including the foreseen additions before their trigger arrives. Making `unit` an enum. Changing the schema `id` or prefix. Moving anything into common from another module.

**Never.** `tree_root: true` on any class. Graph vocabulary or annotations. Hand edits under `dist/` or `docs/model/`. Redefining any slot this module declares, `id`, `description`, `value`, `unit`, or the coordinate slots, in another module; a module lists them and refines them with `slot_usage`. A container or payload class.

## Success Criteria

1. `uv run pytest` passes with `test_lint.py` and `test_dist.py` no longer skipped: 1 lint test, 1 meta-schema test, and 2 new example rows collected and passing; 4 example rows and the `test_references.py` rows since 2026-09-21.
2. `dist/common.schema.json` exists, declares draft 2020-12, passes the meta-schema check, and its `$defs` contain exactly `Position`, `Quantity`, `Interval`, `CapabilityType`, since 2026-09-22 `ComponentPermanence`, and since 2026-09-21 `MaterialCategory`, a class like `CapabilityType`, so nothing in any module's file points at either: a reference by id renders as a plain string. `MaterialName` never appeared while it existed: LinkML inlines types onto the slots that use them, so it rendered as a plain string, and it was retired on 2026-09-21. Its root has no `properties` of its own, confirming the no-`tree_root` decision. Both behaviours verified on a probe, 2026-09-11.
3. `dist/README.md` lists `common.schema.json` with the module description.
4. `docs/model/common/index.md` lists five classes, fourteen slots, one enum, `ComponentPermanence`, and no type, since 2026-09-22. Every page has a description.
5. `examples/common/capability_types.yaml` contains the four core capability types, `locomote`, `grip`, `lift`, `align`, with `id` and `description` only; every id is a bare verb and the word "element" appears in none of them. `examples/common/material_categories.yaml` contains `masonry`, `timber`, `concrete` with `id` and `description` only, since 2026-09-21.
6. Another team's check: given only `docs/model/common/`, a person adds an eleventh capability type to the example file and `uv run pytest` still passes. Recorded as done when it has happened once; not blocking.
7. The toolchain was not changed by this module's own work. One exception, recorded: using common surfaced a toolchain bug, stale pages surviving inside a module's docs folder when an element is removed, fixed in a separate `fix(build)` commit with its own test. `git log -- scripts tests/test_build.py tests/test_lint.py tests/test_dist.py` shows that commit and no other from this module.

## Decisions Made Here (for review)

1. **Position is an object, not an array.** The reference used a three-number array. An object flattens to `x`, `y`, `z` properties in the graph and is unambiguous in YAML.
2. **Quantity drops `provenance`.** Deferred to Plan and Run with the rest of provenance.
3. **`unit` is a free string, UCUM recommended.** Enforcing a unit vocabulary is a later decision that the graph would inherit; nothing in step 1 needs it.
4. **The four core capabilities migrate; the other six reference entries do not.** Revised 2026-09-11: the vocabulary is open for improvement, so the example holds only what the reference primitives require and the brief's allocation example names. Others return one at a time when a method needs them.
5. **`description` required on CapabilityType; no `label`, and no `label` slot in common at all.** Revised 2026-09-11: the id is the verb and a label would repeat it. A class whose id is not a readable name brings `label` with its own module. Display is English only; a second language would make `label` a language-keyed map, and nothing asks for that.
6. **Capability ids are bare verbs.** Decided 2026-09-11: the reference's noun ids (`locomotion`, `gripper`, `lifting`, `alignment`) become `locomote`, `grip`, `lift`, `align`, because a capability names something a robot can do. Bare verbs over gerunds for brevity and because `requires: [lift, align]` reads naturally.
7. **`id` is unique among instances of its class, with no namespace prefix.** Decided 2026-09-11. In the graph the node label is the namespace, and in documents every reference slot declares its range, so the class is always known. Namespaced ids such as `capability.lift` would state the class twice; opaque ids would make the hand-authored catalogue unreadable. The projection's one uniqueness constraint per label enforces exactly this promise.
8. **`MaterialName` as a shared string type.** Retired 2026-09-21, decision 16. From 2026-09-11 it joined product's `material` and process's `applies_to` by exact match; the join is now `MaterialCategory` and the string is the `id` of product's `Material`.
9. **Coordinate slots are `x_coord`, `y_coord`, `z_coord`.** Decided 2026-09-11: `linkml-lint`'s snake_case rule requires at least two characters and rejects hyphens, so single letters and `x-coord` both fail. A lint exemption for three names was considered and declined in favour of names that pass the rule as it stands.
10. **No `tree_root` anywhere, and no container classes.** LinkML recommends a `tree_root` container for serialisation, and that is right for a single self-contained schema. Here modules merge on import, and a probe on 2026-09-11 showed the consequence: with a container in common and another in product, product's generated schema took common's root and rejected a product document as having unexpected properties. So documents are top-level lists, validation always names the class with `-C`, and the `dist/` files are definition libraries with no root properties. Container classes without `tree_root` were considered and declined to avoid a wrapper class per module and an extra projection rule.
11. **The four dimension slots live here.** Decided 2026-09-12 in resource's Phase 1: slots are global to the merged schema and product does not import resource, so a slot both need is declared in the module both import. `weight` is also what the brief's Capacity check compares against load capacity.
12. **`Position` carries `unit`, required.** Decided 2026-09-14 in resource's Task 3 review. Before this, `Position` was three floats whose unit was a sentence in its description, "the project's units, read from the IFC," which the schema itself could not see: a `Position` was only meaningful inside the document that produced it. Resource's mount offsets, a sensor's or manipulator's installation point on the robot body, needed a unit-carrying point and got a second class, `MountPosition`, which sidestepped the brief's one-frame rule by name. Putting `unit` on `Position` makes a point self-describing wherever it is written, retires `MountPosition`, and leaves the brief untouched: it forbids a frame slot, and a unit is not a frame. Product's derived positions write the unit the IFC parse read them in, redundant with the IFC and harmless. The schema stays at eleven shared slots; `unit` was already declared for `Quantity`.
13. **`Position` is a triple with a unit, not only a point.** Decided 2026-09-14 in resource's Task 3 review. Resource's manipulator reach is three extents along the robot's axes with one unit, the same data as a point and nothing more; a second class for it would duplicate `Position` under another name. The description now reads "a point, or an extent along each axis", and the owning slot says which it holds.
14. **`ParameterKind` moved to process.** Decided 2026-09-17 in process's Phase 1 and applied 2026-09-18: its only reader is process, and its values, `component`, `location`, `robot`, name classes common cannot see. Common carries no enum: its two shared vocabularies are classes with documents (decision 17).
15. **`MaterialCategory` lives in common.** Decided 2026-09-21 in process's Phase 4, when `applies_to` moved from the parameter declaration to `Method`. Material strings arrive from the IFC parser per model, spelled as the authoring tool spelled them, so no method can be written against one; they are the `id` of a product `Material` record. The categories are the project's words, IFC's `IfcMaterial.Category`, which real files rarely fill, written at the granularity methods distinguish. Common carries the vocabulary because product and process both read it and cannot see each other, the test `ParameterKind` failed. Its form was decided twice that day: first a class with `id` and `description` beside product's `Material`, then folded to an enum for tier 1 checking on both sides and visible values in the JSON Schema, then returned to the class by decision 17.
16. **`MaterialName` retired.** Decided 2026-09-21 with `SPEC-product.md` decision 17. The material string became the `id` of product's `Material` record, shaped on `IfcMaterial`, and `applies_to` moved to `MaterialCategory`, so nothing ranged the type. A type ranged by nothing is a sentence with no reader. Common carries no type; `dist/common.schema.json` is unchanged, since a type never appeared there.
17. **Vocabularies are classes with documents; enums are for values code branches on.** Decided 2026-09-21, the evening of decision 15, reversing that day's enum. The question was how a company adopting the schema adds a capability its robot offers, or a category its methods need, and how the two readers of each vocabulary, `offers` and `requires`, `category` and `applies_to`, are kept from drifting silently. An enum answers the second at tier 1 and fails the first: every new word is a schema change, and the schema's longevity is the point of publishing it. The comparable systems put curated words that adopters extend in documents, never in the base schema: FHIR's CodeSystems and ValueSets with a terminology server checking codes at ingestion, IFC's `USERDEFINED` escape and external classification tables, IANA registries referenced by pattern, and LinkML's own dynamic enums. The deciding test, from the GraphQL enum discussion the author brought: an enum is for a flag the code depends on; a value the code only carries and matches is data. No code here branches on `grip` or `masonry`; the generator branches on `ParameterKind`. So `CapabilityType` and `MaterialCategory` are classes with `id` and `description`, each with a document under `examples/common/`, and a company adds a word by adding a record. The price is that a reference by id renders as a plain string in JSON Schema and nothing checks the join at tier 1; the design is type safe only through an explicit check, so `tests/test_references.py` resolves every `requires`, `offers`, `category`, `applies_to`, and `made_of` in the examples against its document on every run, and the generator carries the same rule at tier 2. `unassigned` goes with the enum: a reference slot holds `""` until the mapping step assigns a category, as every other product reference slot does.
18. **`ComponentPermanence` and `permanence` move here from product, unchanged.** Decided 2026-09-21 in Phase 1 of the `Stock` extension, `SPEC-stock.md` decisions 3 and 5, recorded 2026-09-22. Resource's `Stock` needs the same distinction a `BuildingComponent` carries: formwork is temporary and comes back after use, rebar is permanent and is consumed. Product and resource never import each other, so a slot and an enum both need are declared in the module both import, the rule the four dimension slots followed (decision 11). The wording is product's; `BuildingComponent` keeps `permanence` required through its own `slot_usage`, and product's JSON Schema does not change in content. The enum stays an enum under decision 17's rule: the HDDL export branches on the value, releasing a temporary stock after the method's last subtask and consuming a permanent one.

## Open Questions

- Does the schema viewer need a root `properties` block to render, or does it read `$defs` directly? The generated root has `$id`, `$schema`, `title`, `type`, `version`, `additionalProperties`, and `$defs`, and no `properties`. If the viewer needs a root, the fix is in the toolchain build, not in this module.
