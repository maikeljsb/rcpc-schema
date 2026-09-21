# Spec: process

*Module `process` of `CAPABILITY-MAP.md`. Drafted 2026-09-17, reviewed and revised 2026-09-18, and revised again the same day in the plan review, where decision 6 turned the plan side top-down and decision 18 gave the catalogue tasks the same base shape; amended 2026-09-21 after Task 2, when decision 19 moved `applies_to` onto `Method` as one `MaterialCategory` and prerequisite 7 gave common the category vocabulary and product the `Material` class; every decision below is accepted. Depends on `common`, `product`, and `resource`; imported by nothing. Direction fixed by the brief's Domain Structure, its relation kinds table, and its dated process decisions of 2026-09-17; HDDL lineage from `docs/research/pddl-for-process.md` (the deciding source, with the subtask experiment in its Appendix B); the multi-agent question closed by `docs/research/ma-pddl-for-process.md`; metamodel usage follows `docs/research/linkml-metamodel-conformance-and-inheritance.md`. Every mechanism claim below was probed on LinkML 1.11.1 on 2026-09-17 and 2026-09-18 against a draft of this module importing the three committed modules.*

## Objective

Give the planner its domain and its output shape in HDDL's own words: a catalogue of primitive tasks that require capabilities, compound tasks, and methods that decompose them into ordered subtasks matched to components by material category; and a plan side where a task network says what is asked for, and every planned task occurrence points at its catalogue task and binds each parameter to a component, a space, or a machine. Deliver it as `schema/process.yaml`, with one hand-written example catalogue file, one example plan file holding a task network decomposed down to its leaves and bound to ids from the product and resource examples, generated JSON Schema, and generated documentation.

**Users.** The person writing the catalogue, who adds a primitive, a compound task, or a method by copying an entry. The planner, which reads the catalogue as an HDDL domain, the product and resource documents plus the task network as the problem, and writes the instance records as its solution. Stage two, which rewrites the `robot` binding on a primitive task instance. The projection component, which turns every reference into an edge and flattens the keyed maps and the subtask list onto their owners. The behaviour tree mapping, which reads each primitive task instance as a leaf. Other project teams, who read `docs/model/process/`.

**Success in one sentence.** `schema/process.yaml` lints clean, the catalogue file and the plan file validate record by record and the eleven invalid documents fail naming their slot, the toolchain produces its JSON Schema and docs unchanged, and the path BuildingComponent to Method to PrimitiveTask to CapabilityType to RobotUnit is written out in the examples with every id resolving in a sibling file.

**What this module deliberately is not.** It has no precondition or effect language, no method preconditions, no component-state or resource-availability kinds, no Plan or Run class with versions or provenance, no HDDL export, no allocation algorithm, no behaviour tree. The catalogue is the domain and the instances are one solution; what produces or consumes them is outside.

## Tech Stack

Inherited from `SPEC-toolchain.md` unchanged. This module adds no dependency.

## Commands

```
uv run linkml-lint schema/process.yaml
uv run pytest tests/test_examples.py -k process
                                        # splits catalogue.yaml and plan.yaml by record_type into temporary
                                        # per-class files and runs linkml-validate -C <record_type> on each
uv run linkml-validate -s schema/process.yaml -C PrimitiveTask <a file holding PrimitiveTask records only>
                                        # the same check by hand, one class at a time
uv run python scripts/build.py          # produces dist/process.schema.json, dist/README.md, docs/model/process/
uv run pytest
```

`linkml-validate` checks one class per run and does not read `record_type` (checked in the installed 1.11.1), so a mixed file is validated by splitting it first. The test harness does the split; the generator will group by the same key when it reads the files.

## Project Structure

Files this module adds.

```
schema/
  process.yaml                                              the module
examples/
  process/
    catalogue.yaml                                          MoveTo, Attach, Detach, Place; ConstructComponent, Transport;
                                                            m_transport, m_prefab: every catalogue record, in one file
    plan.yaml                                               one network of two walls, the second after the first; the two
                                                            network tasks, one Transport compound, and the five leaves
    invalid/
      primitive_task_missing_duration.yaml                  no duration
      primitive_task_requires_empty.yaml                    requires: []
      primitive_task_id_not_a_name.yaml                     id with a hyphen
      primitive_task_parameter_unknown_kind.yaml            a parameter of kind position
      method_parameter_missing_kind.yaml                    a parameter written as an object without parameter_kind
      method_subtask_names_two_tasks.yaml                   a subtask with both primitive_task and compound_task
      method_subtasks_empty.yaml                            subtasks: []
      method_ordering_not_a_list.yaml                       ordering: "1<2"
      compound_task_record_type_mismatch.yaml               a CompoundTask record whose record_type says Method
      task_network_tasks_empty.yaml                         tasks: []
      compound_task_instance_missing_subtasks.yaml          no subtasks key
dist/
  process.schema.json                                       generated
  README.md                                                 regenerated, now lists process
docs/
  model/
    process/                                                generated, one page per element
tests/
  test_examples.py                                          thirteen rows added to EXAMPLES; one new row kind, see prerequisite 5
```

The catalogue examples are written by hand and are fictional in the sense that no site runs them; they use the four capability ids in `examples/common/capability_types.yaml` and the material category the product examples carry. The instance examples bind ids that exist in `examples/product/` and machine ids derived from `examples/resource/`.

## Prerequisite changes

Seven: five decided in Phase 1 on 2026-09-17 or in this spec's review on 2026-09-18, all landing with this module's first task and amended in their own document in the same review; the sixth decided during Task 1 on 2026-09-18; the seventh decided on 2026-09-21 after Task 2, landing before Task 4.

1. **`ParameterKind` leaves `schema/common.yaml`.** Its only reader is process, and its values name classes common cannot see. `SPEC-common.md` loses the Enum section and its success criteria 2 and 4 change: `$defs` are exactly `Position`, `Quantity`, `Interval`, `CapabilityType`; the index lists four classes, thirteen slots, no enum, one type. `dist/common.schema.json`, `dist/product.schema.json`, `dist/resource.schema.json` and the three docs folders regenerate without it, and the `$defs` lists in `SPEC-product.md` criterion 2 and `SPEC-resource.md` criterion 2 drop `ParameterKind`, in place.
2. **`mason_m1` offers `locomote`** in `examples/resource/robot_units.yaml`, one word added to its `offers`. The example method threads one robot through `MoveTo` and `Attach`, so the machine bound in the instance example must offer both `locomote` and `grip`; today no example robot does. A bricklaying robot that drives along its wall is plausible, and the change keeps the first conformance corpus consistent at tier 3 rather than only at tier 1.
3. **`SPEC-toolchain.md` success criterion 9 is narrowed** from "no `dist/*.schema.json` contains `"null"` as a type" to "no optional slot's type contains `"null"`". The `ordering` array slot renders, on LinkML 1.11.1, as `items: {type: ["null", "boolean", "object", "number", "string", "array"]}`, the generator's own lax array form (linkml issue 2188, quoted in `docs/research/pddl-for-process.md` Appendix A). That word is not the optional-slot null the criterion was written against and the toolchain's own test checks only the fixture, so nothing fails; the criterion's wording is corrected so the artifact and the spec agree.
4. **The brief's projection rule admits a second rule keyed on the model's own catalogue.** Recommended Direction today reads "One rule is keyed on a named slot rather than on the metamodel: a `RobotUnit` with `count` n yields n machine nodes … Recorded 2026-09-11 as the only such rule; a second one reopens the decision." Reopened and decided 2026-09-18: a binding's value is an edge to the node whose class is named by the declared kind of that parameter on the bound task or method (see decision 4). The sentence becomes "Two rules are keyed on the model's own data rather than on the metamodel alone: the `count` expansion, and the binding edge, whose target class is the parameter's declared kind. Both are deterministic and recorded; a third reopens the decision." The capability map's process row gains `TaskNetwork` and `ParameterBinding`. The same review amends two more brief sentences for decision 5: Domain Structure's "binds that method's variables once" and the default "A method's `robot` variable is bound once on the `CompoundTaskInstance` and its children inherit it" become "each instance binds its own task's parameters; the method's variables are bound on the children that use them".
5. **`tests/test_examples.py` gains one row kind: a class value of `by record_type`.** For such a row the harness reads the file, groups its records by `record_type`, writes each group to a temporary file, runs `linkml-validate -C <record_type>` on it, and fails naming the record if a `record_type` is missing or names no class in the schema. Everything else in the harness is unchanged, and rows naming a class directly keep working, which is how the invalid documents are checked. `SPEC-toolchain.md`'s line "Domain modules add rows; nothing else changes" is amended to name this row kind. Product's four files by class are unaffected; whether they merge into one self-describing file, which `SPEC-product.md` decision 16 left open, is recorded on the capability map as a follow-up, not done here.
6. **`SPEC-toolchain.md` gains rule 8: one JSON Schema definition for a keyed class written only as dict values.** The dict form of `parameters` and `bindings` rests on a key slot, and LinkML's generator renders every keyed class twice: the class itself, with the key required, and a copy suffixed `__identifier_optional` with the key dropped, which is what the dict's values are checked against because the key carries the name. For `Parameter` and `ParameterBinding` the first definition is referenced by nothing, since neither is ever written on its own. The author required the dict form as input and a single definition in the output, both hard, on 2026-09-18; the list form was declined as not what a person writes. The build script therefore replaces the unreferenced definition with the copy under the class's own name. It touches no check: `linkml-validate` builds its own JSON Schema from the YAML, and the pruned definition was satisfiable by no correct record. Committed on its own, before this module's first task, with its test on `tests/fixtures/keyed.yaml`.
7. **`MaterialCategory` in common, `Material` and `made_of` in product.** Decided 2026-09-21 with decision 19. `SPEC-common.md` decisions 15 and 17 add `MaterialCategory` as a class with `id` and `description` and its document `material_categories.yaml`, `masonry`, `timber`, `concrete`; decision 16 retires the `MaterialName` type once nothing ranges it. `SPEC-product.md` decision 17 adds the `Material` class shaped on `IfcMaterial`, one shared record per distinct material string with its `category`, `""` until a mapping step outside the schema fills it, and renames the component's slot to `made_of`; the product examples gain `materials.yaml` through the throwaway extractor's string-to-category table. Each lands in its own commit, common then product, before this module's Task 3 moves `applies_to`. The vocabulary was an enum between Task 3's first and its follow-up commits of the same day; `tests/test_references.py` guards the join since.

## The Model

### Schema header

```yaml
id: https://rcpc.for5672/schema/process
name: process
version: 0.1.0
description: >-
  Tasks and how they decompose. PrimitiveTask, CompoundTask, and Method as the
  catalogue; TaskNetwork, CompoundTaskInstance, and PrimitiveTaskInstance as a
  plan: what is asked for, and each planned occurrence bound to components,
  spaces, and machines.
prefixes:
  rcpc: https://rcpc.for5672/schema/
  linkml: https://w3id.org/linkml/
default_prefix: rcpc
default_range: string
imports:
  - linkml:types
  - common
  - product
  - resource
```

### Two sides, two conventions

The **catalogue** (`PrimitiveTask`, `CompoundTask`, `Method`) is the HDDL domain, one file, hand-authored: its slots are required where a missing value would leave the task unusable, and optional otherwise. The **plan side** (`TaskNetwork`, `CompoundTaskInstance`, `PrimitiveTaskInstance`) is the HDDL problem's initial task network and the planner's solution, one file per plan, and follows the required-everywhere rule product adopted for pipeline output: every slot is a required key, and an unresolved or inapplicable value is `""` on a string or reference slot and `[]` on a list. A reference holding `""` renders as no edge.

Wherever the module orders things it uses one mechanism: a list, its entries counted from 1, and `ordering` as pairs of those numbers. A method's `subtasks`, a network's `tasks`, and a compound instance's `subtasks` are all read the same way.

### Classes

| Class | Slots | Notes |
|---|---|---|
| `Task` | `record_type`, `id`, `description`, `parameters` | HDDL's task: a name and typed parameters, the word the paper uses before it says which kind. Never written as a record: it is the base `PrimitiveTask` and `CompoundTask` are `is_a`, declaring their four shared slots once, with `id` matching `^[A-Za-z][A-Za-z0-9_]*$`, the one name pattern for the whole catalogue namespace. `record_type` locks to the subclass, probed. Required: everything; `parameters` may be `{}`. |
| `PrimitiveTask` | the four of `Task`, plus `requires`, `duration` | HDDL's action: a task with a requirement and a duration added. `id` is the action name and is what a behaviour tree registers. Every primitive declares a parameter of kind `robot`. `requires` is the one condition the model states. Required: everything. |
| `CompoundTask` | the four of `Task` | HDDL's abstract task: a task with nothing added, no body, no state change. Adds no slot; the class is the kind. |
| `Method` | `record_type`, `id`, `description`, `compound_task`, `applies_to`, `parameters`, `subtasks`, `ordering` | HDDL's decomposition method. `compound_task` is the task it decomposes, HDDL's `:task`; `applies_to` is the one material category of the components it is written for, constraining the component bound to that task's component parameter, absent when the method applies to any; `parameters` declares every variable its subtasks use, a superset of the task's parameters under the same names; `subtasks` is an ordered list of `Subtask`, at least one; `ordering` is a list of position pairs, `[]` when unordered. Same `id` pattern. Required: everything but `applies_to`. |
| `Parameter` | `parameter_name` (key), `parameter_kind` | HDDL's typed variable, `?c - component`: one declared parameter of a task or a method, its name and the kind of object it ranges over, nothing else. Written inline, keyed by name, in the one-line form `c: component`; the object form `c: {parameter_kind: component}` also validates and says the same. No identifier: flattens onto its owner with the key as prefix. Required: `parameter_kind`. |
| `Subtask` | `primitive_task`, `compound_task`, `arguments` | One entry of a method's `subtasks`: HDDL's `(t3 (move ?r ?from ?to))` with the list position standing for `t3`. Exactly one of the two task slots is set, checked by a class rule at tier 1. `arguments` lists, in the named task's parameter order, method parameter names or object ids. No key, no identifier: flattens onto the method with its position as prefix, and its task reference is one edge from the method to the task carrying the position. Required: `arguments`, which may be `[]`. |
| `TaskNetwork` | `record_type`, `id`, `tasks`, `ordering` | HDDL's `:htn` block: what the plan is asked to accomplish. `tasks` is the ordered list of the `CompoundTaskInstance`s no compound lists as a subtask, at least one, each position its label; `ordering` is the same list of position pairs a method carries, `[]` when the tasks may interleave. Every slot required. |
| `TaskInstance` | `record_type`, `id`, `bindings` | One planned occurrence of a task, HDDL's "task" when the kind does not matter. Never written as a record: it is the one range the two instance classes share, so that a compound's `subtasks` can list either kind. `CompoundTaskInstance` and `PrimitiveTaskInstance` are `is_a` it; each inherits the three slots, and `record_type` locks to the subclass, probed. |
| `CompoundTaskInstance` | `record_type`, `id`, `compound_task`, `decomposed_by`, `bindings`, `subtasks` | One planned occurrence of a compound task: the IPC decomposition line `<id> <task> <args> -> <method> <child ids>`. `decomposed_by` is `""` until the planner has chosen a method, then that method; `subtasks` is `[]` until then, and afterwards the ground tasks that replaced this one, one per line of the method's `subtasks`, in the same order, so entry `i` realises line `i` and takes its order from the method's `ordering`. `bindings` binds exactly its task's parameters, decomposed or not; the method's own variables are bound on the subtasks. Every slot required. |
| `PrimitiveTaskInstance` | `record_type`, `id`, `primitive_task`, `bindings` | One planned occurrence of a primitive task: the IPC plan line `<id> <action> <args>`. Always listed in some compound's `subtasks`, never in a network's `tasks`. `bindings` binds every parameter of its primitive task. Every slot required. |
| `ParameterBinding` | `parameter_name` (key), `bound_to` | One parameter bound to one object id. Written inline, keyed by name, always in the one-line form `r: mason_m1_1`, because `bound_to` is the class's one required non-key slot. What kind of object the id names is read from the parameter's declaration on the bound task or method, at tier 2 and by the projection. No identifier. Named `ParameterBinding` in the Task 4 review, 2026-09-21, from `Binding`: the entry binds one parameter, and the name should say so beside `Parameter`. |

Eight classes carry an identifier: `Task` with its two subclasses, `Method`, the network, and `TaskInstance` with its two subclasses. Six are written as records and project to nodes; `Task` and `TaskInstance` are the labels their subclasses stack, by the brief's `is_a` rule, so "every catalogue task" and "every planned occurrence" are each one label. `Parameter`, `Subtask`, and `ParameterBinding` have no identifier and flatten into the record that holds them. `compound_task`, `primitive_task`, `requires`, `tasks`, `decomposed_by`, and the instance's `subtasks` are reference slots and project to edges. `bound_to` projects to an edge by the second catalogue-keyed rule (prerequisite 4). `Quantity` flattens as in every module.

The six record classes carry `record_type`, product's type designator, reused as `id` is; LinkML locks its value to the class being validated, probed for all six, including the four that inherit it from `Task` or `TaskInstance`. Here it is load-bearing: a catalogue file and a plan file each hold records of three classes, and `record_type` is what routes a record to its class for validation and, later, in the generator. `Parameter`, `Subtask`, and `ParameterBinding` do not carry it, for the same reason `Position` does not: they are never a record on their own and never validated against directly.

### Enum

| Enum | Values | Notes |
|---|---|---|
| `ParameterKind` | `component`, `location`, `robot` | The kinds of object a parameter ranges over: a `BuildingComponent` or its subclass, a `Space`, a machine of a `RobotUnit` entry. Moved here from common with these values, replacing `position`, `component_reference`, `quantity`. No default. |

### Slots declared in this module

| Slot | Range | Notes |
|---|---|---|
| `parameters` | `Parameter`, multivalued, `inlined: true` | The declared parameters, keyed by name. Dict form: a keyed range class whose one required non-key slot is `parameter_kind`, so LinkML accepts the value alone, `r: robot`, beside the full object form. Probed. |
| `parameter_name` | string, `key: true` | The parameter's name, a plain word such as `c`, `r`, `from`. Shared by `Parameter` and `ParameterBinding`. Lifted out as the map key, so no pattern can reach it at tier 1; the HDDL export prefixes `?`. |
| `parameter_kind` | `ParameterKind` | Required on `Parameter`. |
| `applies_to` | `MaterialCategory` | The material category of the components a method decomposes its task for, one value such as `masonry`; a component matches when the Material it is `made_of` has that `category`. On `Method` only. Optional: absent when the method applies to any component; `""` is never written here. Single-valued: the vocabulary is cut so that every method has one category, decision 19. A plain string in JSON Schema, a reference by id like `requires`; resolved against `material_categories.yaml` by `tests/test_references.py`. |
| `requires` | `CapabilityType`, multivalued, `required: true`, `minimum_cardinality: 1` | What a robot must offer to perform the primitive. Renders `minItems: 1`; `[]` fails naming `requires`. Probed. |
| `duration` | `Quantity`, `inlined: true` | How long one performance takes, recommended in seconds. Required on `PrimitiveTask`. One value per primitive; a duration depending on the parameters, HDDL 2.1's `(= ?duration (road-length ?l1 ?l2))`, is a recorded limit. |
| `compound_task` | `CompoundTask` | The compound task a method decomposes, a subtask names, or an instance realises. Required on `Method` and `CompoundTaskInstance`; one of two on `Subtask`. |
| `primitive_task` | `PrimitiveTask` | The primitive task a subtask names or an instance realises. Required on `PrimitiveTaskInstance`; one of two on `Subtask`. |
| `subtasks` | multivalued; range set per class in `slot_usage` | The subtasks in list order, HDDL's word for both the lifted and the ground case. On `Method`: range `Subtask`, `inlined: true`, `inlined_as_list: true`, `required: true`, `minimum_cardinality: 1`; `[]` fails naming `subtasks`. On `CompoundTaskInstance`: range `TaskInstance`, by id, `required: true`; `[]` is an undecomposed task, and a missing key fails naming `subtasks`. Both probed. One slot with two ranges, because HDDL has one word; gen-doc's page for the slot then states range `string` while each class page states the right one, accepted in decision 6. |
| `tasks` | `CompoundTaskInstance`, multivalued, `minimum_cardinality: 1` | The network's tasks in list order, by id; each position is its label. Required on `TaskNetwork`; `[]` fails naming `tasks`. Probed. |
| `ordering` | integer, `array: {exact_number_dimensions: 2, dimensions: [{alias: pair}, {exact_cardinality: 2}]}` | Pairs of positions in the owner's `subtasks` or `tasks` list, `[[1, 2], [2, 3]]`; in each pair the first ends before the second starts. Required on `Method` and `TaskNetwork`, `[]` when unordered. The validator checks only that it is a list (Appendix A of the PDDL note); pair shape and position existence are tier 2. |
| `arguments` | string, multivalued | The values a subtask passes, in the named task's parameter order: method parameter names or object ids. Required on `Subtask`. |
| `decomposed_by` | `Method`, pattern `^$|^[A-Za-z][A-Za-z0-9_]*$` | The method chosen for a compound instance. Required; `""` until chosen. |
| `bindings` | `ParameterBinding`, multivalued, `inlined: true` | The instance's parameters bound to object ids, keyed by parameter name: `{r: mason_m1_1, to: 0BTBFw6f90Nfh9rP1dlXrr}`. Required on `TaskInstance`, so on both instance classes. Dict form with the one-line value; an object or a list in its place is rejected, probed. |
| `bound_to` | string | The id of the object the parameter is bound to: a `BuildingComponent`, a `Space`, or a machine such as `mason_m1_1`, as the parameter's declared kind says. Required on `ParameterBinding`. No pattern, because the three kinds have three id shapes. |

Reused: `id`, `description` from common; `record_type` from product; `Quantity`, `CapabilityType`, `MaterialCategory` as ranges. Not used, because product owns them with product's meaning and they are global: `name`, `kind`, `source`, `status`.

### Class rule

One, tier 1, probed to fire in the list form `subtasks` is written in. A rule with no precondition renders a bare `then` and never fires (Appendix A of the PDDL note), so it carries a precondition on a slot that is always present inside the entry.

| Class | Precondition | Postcondition | Catches |
|---|---|---|---|
| `Subtask` | `arguments` present | exactly one of `primitive_task`, `compound_task` present | both set: "is valid under each of"; none set: "is not valid under any of the given schemas"; both messages name `/subtasks/<n>` |

### Lineage: HDDL construct to slot

Every row is a decision. "Borrowed" means the construct is carried under HDDL's meaning, "Adapted" that it is narrowed or moved. Constructs the module carries nothing for are not listed; the brief's Not Doing and Out sections and `docs/research/pddl-for-process.md` Part 2 record them. Sources are `docs/research/pddl-for-process.md` Part 1 by section.

**Domain: tasks and methods**

| HDDL construct | Slot or class | Borrowed / Adapted | Note |
|---|---|---|---|
| `(:types ...)` (1.2) | `ParameterKind` | Adapted | Three object kinds, each an identified class in product or resource. No hierarchy, no `either`. Numbers are not types (PDDL 2.1 §3), so `position` and `quantity` left the enum. |
| `(:predicates ...)`, `(:functions ...)` (1.3) | nothing here | Adapted | Every reference and enum slot in product and resource is a predicate, every `Quantity` or `Position` slot a function. Process declares none. |
| "Each task (primitive or compound) is given by its name, followed by a parameter sequence" (§2, p. 2) | `Task`, the base of both | Borrowed | The name and typed parameters every task has; "two kinds of tasks in HTN planning: primitive and compound ones" (§2, p. 2) are the two subclasses. |
| `(:action name :parameters ...)` (1.4) | `PrimitiveTask` with `id`, `parameters` | Borrowed | Name unique among tasks, typed parameters. |
| `:precondition`, `:condition` (1.4) | `requires` | Adapted | The one condition kept, `(over all (offers ?r <capability>))` in the export, a durative action's condition. No formula language; the other kinds are Later in the brief's table. |
| `:duration` (HDDL 2.1, 1.4) | `duration` | Adapted | One `Quantity` per primitive; no parameter-dependent expression. Integer time is the export's rounding. |
| `(:task name :parameters ...)` (1.5) | `CompoundTask` with `id`, `parameters` | Borrowed | Declared explicitly so a misspelt primitive is not read as abstract and arity is stated, HDDL §3. |
| `(:method name` (1.6) | `Method.id` | Borrowed | |
| `:task (c ?x ...)` (1.6) | `compound_task` | Adapted | The task by id; its parameters are matched to method parameters by name, not by an argument list. Tier 2 checks the method declares each under the same name and kind. |
| `:parameters` of a method (1.6) | `Method.parameters` | Borrowed | Every variable the subtasks use, a superset of the task's, HDDL §4 p. 7. |
| a method restricted to a kind of object: a subtype on its own parameter declaration (§4 p. 7, 1.6) or a method precondition over a fact of the object (1.6) | `Method.applies_to` | Adapted | One `MaterialCategory` on the method. The schema stores the category; the export chooses the HDDL form, and Appendix B.1 of the PDDL note writes `:precondition (material ?e masonry)` over category constants and solves it. The declaration `?c - component` stays a typed variable and nothing else. |
| `<subtask-def>` `(id (task term*))` (1.7) | `Subtask` with `primitive_task` or `compound_task` and `arguments` | Adapted | The entry's list position is the id. Two reference slots because one slot cannot range two classes and stay a reference. |
| `:ordered-subtasks`, `:subtasks` alone (1.8) | `ordering` as all pairs, or `[]` | Adapted | Three surface forms become one; the export always writes the labelled form with `(< t1 t2)`. |
| `:ordering (and (t1 < t2) ...)` (1.7, 1.8) | `ordering` | Borrowed | Pairs of whole-task positions. HDDL 2.1's event-level ordering (Def. 6) not taken. |

**Problem and solution**

| HDDL construct | Slot or class | Borrowed / Adapted | Note |
|---|---|---|---|
| `(:objects ...)`, `(:init ...)` (1.9) | product and resource documents | Adapted | Components, spaces, storeys, materials, machines are the objects; `located_in`, `made_of` with each Material's `category`, `offers`, `status`, and the quantities are the initial state. |
| `(:htn :tasks (and ...) :ordering (...))` (1.9) | `TaskNetwork` with `tasks`, `ordering` | Borrowed | The same `<tasknetwork-def>` a method body uses: a labelled list and pairs over the labels. Its tasks are the `CompoundTaskInstance`s no compound lists among its `subtasks`. |
| a ground initial task `(deliver package-0 city-loc-0)` (1.9) | a `CompoundTaskInstance` with `bindings` and `decomposed_by: ""` | Borrowed | Always ground; HDDL's lifted `:htn :parameters` not taken. |
| ground primitive line `<id> <action> <args>` (1.10) | `PrimitiveTaskInstance` with `primitive_task`, `bindings` | Borrowed | |
| decomposition line `<id> <task> <args> -> <method> <child ids>` (1.10) | `CompoundTaskInstance` with `compound_task`, `bindings`, `decomposed_by`, `subtasks` | Borrowed | The line's fields, one slot each. The compound carries its task's arguments only; the method's own variables appear on the subtasks. `subtasks` ranges `TaskInstance`, the class the two instance classes share, because a reference slot ranges one class and the line lists both kinds. |
| ordering among a compound's subtasks (Def. 5) | none written | Borrowed | Inherited from the method: entry `i` of the instance's `subtasks` is line `i` of the method's, and the method's `ordering` orders both. Nothing to drift. |
| an agent construct (MA-PDDL) | `robot` kind and the `robot` binding | Adapted | A typed parameter, threaded through a method's subtasks as Transport threads `?v`; no `:agent`, no privacy, no joint actions. |

### Required

| Slot | Why |
|---|---|
| `record_type` on the six record classes | A record says what it is; a document validated against the wrong class fails on `record_type` specifically. |
| `id` on the six record classes, the catalogue three matching the name pattern | Nodes need identifiers; catalogue names travel unchanged into HDDL and a behaviour tree. |
| `description` on the catalogue three | A task nobody can read is not a catalogue entry. Same rule as `CapabilityType`. |
| `parameters` on the catalogue three | A task's arity is its declaration, and `{}` says "none" explicitly rather than by absence. |
| `requires` with at least one | A primitive nothing offers can never be allocated. Mirrors `offers`. |
| `duration` | A primitive without a duration cannot be scheduled and has no HDDL 2.1 form. |
| `Method.compound_task`, `subtasks` with at least one, `ordering` | A method decomposes one task into something; `[]` on `ordering` says unordered, absence would say nothing. |
| `TaskNetwork.tasks` with at least one, `ordering` | A network with no tasks asks for nothing; `[]` on `ordering` says the tasks may interleave. |
| `Parameter.parameter_kind` | A parameter without a kind is untyped, which HDDL forbids everywhere but the type list. |
| `Subtask.arguments`, and exactly one task | An entry is a task and its parameter sequence; `[]` is a nullary task. |
| every slot of both instance classes | Planner output has the same shape on every record; `""` and `[]` mark the undecomposed case so a check reads a value, never tests for a key. |
| `CompoundTaskInstance.subtasks` | A decomposed task says what replaced it, in its method's order; `[]` says "not yet decomposed" explicitly rather than by absence. |
| `ParameterBinding.bound_to` | A binding without a value is not a binding; and being the one required non-key slot is what makes the one-line form valid. |

### The catalogue, as one document

`catalogue.yaml` holds all eight records in one list, in any order; `record_type` says what each is. Two primitives, one compound task, and the two methods:

```yaml
- record_type: PrimitiveTask
  id: MoveTo
  description: Drive the robot to a space.
  parameters: {r: robot, to: location}
  requires: [locomote]
  duration: {value: 120, unit: s}
- record_type: PrimitiveTask
  id: Place
  description: Lift the held component and set it down aligned at its target.
  parameters: {r: robot, c: component, at: location}
  requires: [lift, align]
  duration: {value: 180, unit: s}
```

```yaml
- record_type: CompoundTask
  id: Transport
  description: Bring a component from where it lies to where it belongs.
  parameters: {c: component}
- record_type: Method
  id: m_transport
  description: Fetch the component and carry it to its target space with one robot.
  compound_task: Transport
  parameters: {c: component, r: robot, from: location, to: location}
  subtasks:
    - {primitive_task: MoveTo, arguments: [r, from]}
    - {primitive_task: Attach, arguments: [r, c, from]}
    - {primitive_task: MoveTo, arguments: [r, to]}
    - {primitive_task: Detach, arguments: [r, c, to]}
  ordering: [[1, 2], [2, 3], [3, 4]]
- record_type: Method
  id: m_prefab
  description: Build a prefabricated component by transporting it and placing it.
  compound_task: ConstructComponent
  applies_to: masonry
  parameters: {c: component, r: robot, at: location}
  subtasks:
    - {compound_task: Transport, arguments: [c]}
    - {primitive_task: Place, arguments: [r, c, at]}
  ordering: [[1, 2]]
```

`Attach(r, c, at)` and `Detach(r, c, at)` both require `[grip]`; `ConstructComponent` has `parameters: {c: component}` like `Transport`. `masonry` is the `category` of the brick-on-block Material the product examples' walls are `made_of`; `m_transport` has no `applies_to` and applies to any component. `m_prefab` has a compound subtask so the tree has three levels; `m_transport`'s two `MoveTo` entries are two positions and two edges.

### One plan, as one document

`plan.yaml` holds the network, its compounds, and its leaves in one list, read top down as a method is read. The network, the three compounds, and the first of five leaves:

```yaml
- record_type: TaskNetwork
  id: level_1_walls
  tasks: [construct_138157, construct_138062]
  ordering: [[1, 2]]
- record_type: CompoundTaskInstance
  id: construct_138157
  compound_task: ConstructComponent
  decomposed_by: m_prefab
  bindings: {c: 2O2Fr$t4X7Zf8NOew3FNqI}
  subtasks: [construct_138157_1, construct_138157_2]
- record_type: CompoundTaskInstance
  id: construct_138157_1
  compound_task: Transport
  decomposed_by: m_transport
  bindings: {c: 2O2Fr$t4X7Zf8NOew3FNqI}
  subtasks: [construct_138157_1_1, construct_138157_1_2, construct_138157_1_3, construct_138157_1_4]
- record_type: CompoundTaskInstance
  id: construct_138062
  compound_task: ConstructComponent
  decomposed_by: ""
  bindings: {c: 2O2Fr$t4X7Zf8NOew3FNtn}
  subtasks: []
- record_type: PrimitiveTaskInstance
  id: construct_138157_1_1
  primitive_task: MoveTo
  bindings: {r: mason_m1_1, to: 3It7HtQdTQBQsvQlFr2iGK}
```

The network asks for two walls, the second after the first. The first is decomposed by `m_prefab`, whose two lines are Transport then Place, so its `subtasks` has two entries: the Transport compound and the Place leaf. The Transport compound is decomposed by `m_transport`, four lines, so it lists four leaves; the first and third are both `MoveTo`, told apart by their place in the list, and ordered by the method's `ordering` applied to that list. The second wall is still an undecomposed task, as a planner's input looks before it runs. One plan is one file: what the planner hands over and what stage two rewrites the robot bindings in. The component is the Level 1 wall `Basic Wall:Exterior - Brick on Block:138157`; `0BTB…` is the foyer A101 and `3It7…` the derived exterior Space of Level 1, all from `examples/product/`. `mason_m1_1` is the first machine of the `mason_m1` entry; it appears only on the leaves, because a compound binds its task's one parameter `c` and the method's variables `r`, `from`, `to` are bound where they are used. Instance ids are the listing compound's id with the entry's number appended, a convention of the example, not of the schema.

### Fixed by the brief

Three catalogue concepts under HDDL's names and no Task-as-plan-unit. Parameter kinds `component`, `location`, `robot`; `ParameterKind` in process. `applies_to` on the method, one `MaterialCategory`, equality (2026-09-21). `requires` as the one precondition; no effects, no method preconditions, no formula language. `duration` on `PrimitiveTask`. Subtasks as list entries, not nodes; ordering as position pairs on the method, whole tasks only. Ground classes `PrimitiveTaskInstance` and `CompoundTaskInstance`; ground ordering only among the network's tasks; a compound's subtasks inherit order from the method. The `robot` binding on the primitive instance is the allocation edge, bound by the planner, rewritten by stage two within the entry; no `assigned_unit`. Amended 2026-09-18: the compound binds its task's parameters, not the method's variables; see decision 5. `record_type` on process classes. The example instance proves the path component to method to primitive to capability to robot. MA-PDDL not adopted.

## Code Style

The module follows `SPEC-toolchain.md` and `SPEC-common.md`. The method class and the subtask entry with its rule, as they will appear:

```yaml
classes:
  Method:
    description: >-
      One way to decompose a compound task into an ordered network of subtasks.
    slots:
      - record_type
      - id
      - description
      - compound_task
      - applies_to
      - parameters
      - subtasks
      - ordering
    slot_usage:
      id:
        pattern: "^[A-Za-z][A-Za-z0-9_]*$"
        description: The method name.
      description:
        required: true
      compound_task:
        required: true
      parameters:
        required: true
      ordering:
        required: true

  Subtask:
    description: >-
      One entry of a method's subtask list: the task it names and the
      arguments it passes, in that task's parameter order. Its position in the
      list, counted from 1, is what ordering refers to.
    slots:
      - primitive_task
      - compound_task
      - arguments
    slot_usage:
      arguments:
        required: true
    rules:
      - description: A subtask names exactly one task, primitive or compound.
        preconditions:
          slot_conditions:
            arguments:
              required: true
        postconditions:
          exactly_one_of:
            - slot_conditions:
                primitive_task:
                  required: true
            - slot_conditions:
                compound_task:
                  required: true

slots:
  ordering:
    range: integer
    array:
      exact_number_dimensions: 2
      dimensions:
        - alias: pair
        - exact_cardinality: 2
    description: >-
      Pairs of positions in the owner's subtask or task list; in each pair the
      first ends before the second starts. Empty when unordered.
```

Conventions specific to this module:

- **Names follow the linter's `standard_naming` rule**: CamelCase classes and enum, snake_case slots and permissible values. Catalogue ids are CamelCase for tasks (`MoveTo`) and `m_` snake_case for methods (`m_prefab`), as HDDL files write them; the pattern admits both.
- **HDDL's words where HDDL has one.** `Task`, `PrimitiveTask`, `CompoundTask`, `Method`, `Subtask`, `TaskNetwork`, `TaskInstance`, `parameters`, `subtasks`, `tasks`, `ordering`, `duration` are HDDL's; `subtasks` is used on the method and on the compound instance because HDDL uses one word for the lifted and the ground network. `compound_task` stands for `:task` because a slot named `task` would carry two ranges across three classes; `arguments` stands for the parameter sequence because `parameters` already names the declaration map; `requires`, `applies_to`, `bindings`, `bound_to`, `decomposed_by` are the module's own plain words.
- **One line for a declaration, one for a binding.** A `Parameter` is written `r: robot`; the object form `r: {parameter_kind: robot}` validates but says nothing more and is not written. A `ParameterBinding` is always the one-line `r: mason_m1_1`.
- **One ordering mechanism.** Wherever tasks are ordered, on a method, on a network, or under a decomposed compound, it is a list with positions from 1 and `ordering` as pairs of positions. A compound instance carries no `ordering` of its own; its list is in its method's order and the method's pairs apply. Nothing else orders anything.
- **Catalogue descriptions say what the task does**, one sentence in the imperative, as a capability description opens with its verb. Nothing about which robots or methods use it.
- **Every rule has a `description`** in the indicative, for the reader of the YAML. gen-doc's Rules table prints neither the description nor an `exactly_one_of` postcondition, only `slot_conditions` (seen on product's rule and on `Subtask` on 2026-09-18), so the YAML is where a rule is read.
- **`inlined: true` stated on every object-valued slot**, `parameters`, `subtasks`, `bindings`, `duration`; a reference slot states `range` alone.
- **No `record_type` on `Parameter`, `Subtask`, `ParameterBinding`**, which are never documents; on everything that is.

## Testing Strategy

No new test files. Thirteen rows in `EXAMPLES`: the two mixed files under the `by record_type` row kind of prerequisite 5, the eleven invalid documents, each one record, under their class directly. Where the validator's message names a path rather than a slot, the row's expected string is the path's first segment, which is the slot on the record.

| Document | Class | Expected | Proves |
|---|---|---|---|
| `examples/process/catalogue.yaml` | by `record_type` | validates | Four primitives, one `requires` of two, every primitive with a `robot` parameter; two compound tasks; a method with a total order of four and a repeated primitive and no `applies_to`, and one with a compound subtask and `applies_to: masonry`; all three classes in one file |
| `examples/process/plan.yaml` | by `record_type` | validates | One network with two tasks and one ordering pair; a decomposed network task listing two subtasks, a decomposed compound listing four, an undecomposed network task listing none; five leaves with one-line bindings of every kind; all three classes in one file, `record_type` locking through `is_a` |
| `invalid/primitive_task_missing_duration.yaml` | `PrimitiveTask` | fails on `duration` | A plain required slot |
| `invalid/primitive_task_requires_empty.yaml` | `PrimitiveTask` | fails on `requires` | `minimum_cardinality` reaches the validator as `minItems` |
| `invalid/primitive_task_id_not_a_name.yaml` | `PrimitiveTask` | fails on `id` | The name pattern |
| `invalid/primitive_task_parameter_unknown_kind.yaml` | `PrimitiveTask` | fails on `parameters` | The enum reaches the one-line form; message names `/parameters/r` |
| `invalid/method_parameter_missing_kind.yaml` | `Method` | fails on `parameter_kind` | A parameter written as an object still needs its kind |
| `invalid/method_subtask_names_two_tasks.yaml` | `Method` | fails on `subtasks` | The exactly-one rule fires in list form |
| `invalid/method_subtasks_empty.yaml` | `Method` | fails on `subtasks` | At least one subtask |
| `invalid/method_ordering_not_a_list.yaml` | `Method` | fails on `ordering` | The array slot rejects a scalar, all the validator checks of it |
| `invalid/compound_task_record_type_mismatch.yaml` | `CompoundTask` | fails on `record_type` | The designator locks per class |
| `invalid/task_network_tasks_empty.yaml` | `TaskNetwork` | fails on `tasks` | A network asks for at least one task |
| `invalid/compound_task_instance_missing_subtasks.yaml` | `CompoundTaskInstance` | fails on `subtasks` | Required-everywhere reaches the list: an undecomposed task writes `[]`, never omits the key |

All eleven error messages were probed on 2026-09-17 and 2026-09-18 with the schema shape above and contain the expected string; the two mixed files were probed as their per-class groups. `test_lint.py` and `test_dist.py` collect the new files with no change. The prerequisite changes are covered by the existing common, product, and resource rows, the drift test, and the new row kind's own use on the two mixed files. A record in either file whose `record_type` is missing or unknown fails the row naming that record, in the harness, before the validator runs.

What the validator does not check, and who does: everything that joins two records. This module produces more such checks than the other three together, because a decomposition is nothing but joins. They are listed below in one place, so `CHECKS.md` and the generator's parse step can take them without rereading the spec. Until then, success criterion 5 checks the example corpus by a one-off script, recorded once.

### Deferred to the generator's tier 2

Each is a parse-time check over all documents, an error, before any write.

| Check | Reads |
|---|---|
| Every `compound_task`, `primitive_task`, `decomposed_by`, `tasks`, `subtasks` (on an instance), and `requires` value names a record of its range; `""` excepted where allowed | the catalogue and plan files |
| No id is both a `PrimitiveTask` and a `CompoundTask` | both catalogue files |
| A method declares, under the same name and kind, every parameter of the task it decomposes | `Method.parameters`, `CompoundTask.parameters` |
| A subtask's `arguments` count equals the named task's parameter count, and each argument is either a method parameter of the kind the task declares at that position or an id of a record of that kind | `Subtask`, `Method.parameters`, the task's `parameters`, product and resource ids |
| Every `ordering` entry is a pair of two distinct integers in `1..len(subtasks)` on a method, `1..len(tasks)` on a network | `Method`, `TaskNetwork` |
| Every instance is listed exactly once, in one network's `tasks` or one compound's `subtasks`; `tasks` lists compounds only, so a primitive is never a task of the network | `TaskNetwork.tasks`, `CompoundTaskInstance.subtasks` |
| An instance's `bindings` keys are exactly the parameters of its `primitive_task` or `compound_task` | both instance classes, the catalogue |
| Each `bound_to` names a record of the class the parameter's declared kind says: a `BuildingComponent` for `component`, a `Space` for `location`, a machine id `<entry>_<n>` with `1 <= n <= count` of an existing entry for `robot` | `ParameterBinding`, the declaration on the bound task, product and resource ids |
| A decomposed compound's `subtasks` is as long as its method's, and entry `i` names an instance of the task line `i` names; an undecomposed compound's is `[]` | `CompoundTaskInstance.subtasks`, `decomposed_by`, `Method.subtasks` |
| Through the compound's method, each line's argument names a method variable or an object id. Where it names a variable that is also a parameter of the compound's task, the subtask's binding equals the compound's; where two lines name the same method variable, the two subtasks' bindings are equal; where it names an object id, the subtask's binding is that id. The `robot` variable is exempt from the equality within one entry, so stage two may rewrite one leaf | both instance classes, `Subtask.arguments`, `Method.parameters` |

### Deferred to CHECKS.md, tier 3

Whole-graph queries, each returning zero rows, except work lists.

| Check | Why not tier 2 |
|---|---|
| `ordering` induces a strict partial order: no cycle within a method or within a network | Cycle detection over the whole set |
| Every primitive's `requires` is offered by at least one entry's `Activity` | Otherwise no plan can use it; a work list, not an error |
| The machine bound to a primitive instance offers everything the primitive requires | Type-level allocation, the brief's second checked assumption |
| The component bound to a decomposed compound's component parameter is made of a Material whose `category` its method's `applies_to` names, when the method has one | Method selection, the first checked assumption |
| Work list: every Material whose `category` is `""` or one no method's `applies_to` names | The brief's example of a tier 3 rule |

## What the projection must add

The brief's rule table already covers reference slots, keyed maps with the key as prefix, unkeyed inlined lists with the position as prefix, and the `count` expansion. This module forces three additions, recorded here for `PROJECTION.md`:

1. **A two-dimensional array of primitives** flattens to two index-aligned integer list properties on the owning node, `ordering_before` and `ordering_after`, because a Neo4j property holds flat lists only. The spec chooses parallel lists over a list of strings so that a query compares integers.
2. **A reference inside an ordered list** yields one edge from the owner to the referenced node carrying the entry's position. For an inlined entry with a reference slot, the edge also carries the entry's other primitive slots: `Method -[position, arguments]-> PrimitiveTask | CompoundTask`, two parallel edges when the same task occurs twice. For a multivalued reference slot, `TaskNetwork.tasks` and `CompoundTaskInstance.subtasks`, the edge carries the position alone. This is the existing reference-slot rule applied inside an ordered list; without the position the owner's `ordering` pairs would point at nothing.
3. **A binding is an edge whose target class is the parameter's declared kind.** For each `bindings` entry the component looks up the parameter on the instance's `primitive_task` or `compound_task`, reads `parameter_kind`, and writes one edge carrying the key to the `BuildingComponent`, `Space`, or `RobotUnit` machine node the id names. The machine node is the one the `count` rule created; no document holds its id. This is the second rule keyed on the model's own data (prerequisite 4); a missing declaration is a tier 2 error before any write, so the rule never guesses.

## Boundaries

**Always.** Every class, slot, enum, permissible value, and rule has a description. `inlined: true` on every object-valued slot. The name pattern on `id` in the three catalogue classes. Example instances bind ids that exist in the sibling example files. Rebuild `dist/` and `docs/model/` in the same commit as the YAML. `uv run pytest` passes before committing. Conventional Commits. LF.

**Ask first.** Adding a class or slot beyond the tables above. A fourth `ParameterKind` value. A slot for effects, preconditions, or component state. A planned or actual duration on an instance. A `Plan` or `Run` class beside `TaskNetwork`. A second class rule on any class. A third `is_a` in the module. A pattern on `parameter_name`, `bound_to`, or instance ids. Making `applies_to` required, a list, or a slot of anything but `Method`. A primitive as a task of the network. Moving anything into common beyond prerequisite 7. Touching `schema/product.yaml` or `schema/resource.yaml` beyond prerequisites 2 and 7. Adding a test file.

**Never.** A formula language or a string that is one. Method preconditions or effects. `Subtask` or `ParameterBinding` as identified classes. `assigned_unit` or any mirror slot on `RobotUnit`. An `ordering` on a compound instance. A `Task` or `TaskInstance` written as a record. A third rule keyed on the model's data in the projection. `abstract`, `mixins`, or `union_of`. `any_of` ranges. Graph vocabulary or annotations. Hand edits under `dist/` or `docs/model/`. Redefining a slot common or product declares. Real robot products in the examples.

## Success Criteria

1. `uv run pytest` passes with thirteen new rows collected and passing, and no test file other than `test_examples.py` changed; its change is the row kind of prerequisite 5 and nothing else.
2. `dist/process.schema.json` declares draft 2020-12, passes the meta-schema check, and its `$defs` contain exactly this module's `Task`, `PrimitiveTask`, `CompoundTask`, `Method`, `Parameter`, `Subtask`, `TaskNetwork`, `TaskInstance`, `PrimitiveTaskInstance`, `CompoundTaskInstance`, `ParameterBinding`, `ParameterKind`, and every class and enum of common, product, and resource (imports merge), 30 entries, 32 with `MaterialCategory` and `Material` from 2026-09-21; no entry carries the `__identifier_optional` suffix (prerequisite 6), and `Parameter` and `ParameterBinding` each require their non-key slot only, because their name is the dict key. `record_type` is an `enum` of one value in each of the eight identified classes, the subclass name in each subclass; both catalogue task classes list `description`, `id` with the name pattern, `parameters`, `record_type` among their properties and their `required`, and both instance classes list `bindings`, `id`, `record_type`; `Method.subtasks` has `items` a `$ref` to `Subtask` and `CompoundTaskInstance.subtasks` has `items` of type string; `requires`, `Method.subtasks`, and `tasks` carry `minItems: 1`; `parameters` and `bindings` are objects whose `additionalProperties` is an `anyOf` of the entry object and its one-line value; `Method.applies_to` is a plain string, a reference to `MaterialCategory` by id as `requires` is to `CapabilityType`; `Subtask` carries a bare `if`/`then`; the string `"null"` occurs exactly twice, inside `ordering.items.type` on `Method` and on `TaskNetwork`. All probed 2026-09-18.
3. `dist/README.md` lists `process.schema.json` with the module description.
4. `docs/model/process/index.md` lists exactly eleven classes, the two catalogue task classes indented under `Task` and the two instance classes under `TaskInstance`, fifteen slots, and `ParameterKind`, every entry with a description; `Subtask.md` shows a Rules table. No two names among the classes, slots, enums, types, and schemas `SchemaView` reports for the module with imports coincide case-insensitively (checked on the names, not the folder, because this checkout's filesystem folds case; probed 2026-09-18, none). The folder also holds unlinked pages for the imported modules' elements, as in product and resource.
5. Checked by `tests/test_references.py` on every run since 2026-09-21, and before that once by a one-off script: every `requires` id is in `examples/common/capability_types.yaml`, every `applies_to` in `material_categories.yaml`; every `compound_task`, `primitive_task`, and `decomposed_by` value in `plan.yaml` resolves in `catalogue.yaml`, and every `tasks` and instance `subtasks` value within `plan.yaml`; every `bound_to` under a `component` or `location` parameter resolves in `examples/product/` and every one under a `robot` parameter is `mason_m1_1` or `mason_m1_2`; the example tree passes every tier 2 row above by hand, including the binding agreement between a compound and its subtasks; `m_prefab`'s `applies_to` equals the `category` of the Material the bound wall is `made_of`; `mason_m1` offers everything `MoveTo`, `Attach`, `Detach`, and `Place` require.
6. Every slot declared in `schema/process.yaml` appears in the slot table above and in the lineage table or the module's-own-words list under Code Style. Checked by reading, recorded once.
7. `schema/common.yaml` changed only by the removal of `ParameterKind` and, in prerequisite 7, the addition of `MaterialCategory` and the removal of `MaterialName`; `examples/resource/robot_units.yaml` changed only by one word in `mason_m1`'s `offers`; `scripts/build.py` and `tests/test_build.py` changed only by rule 8 (prerequisite 6), in its own commit; `schema/product.yaml` and its examples changed only by `Material` and `made_of` (prerequisite 7), in its own commit; `schema/resource.yaml`, `tests/test_lint.py`, and `tests/test_dist.py` did not change. `git log -- schema/resource.yaml tests/test_lint.py tests/test_dist.py` shows no commit from this module, `git log -- schema/product.yaml` shows the one prerequisite 7 commit, and `git log -- scripts tests/test_build.py` shows the one prerequisite 6 commit.

## Decisions Made Here

Everything the brief fixed is under Fixed by the brief. The following were decided while writing this spec on 2026-09-17 and revised in its review on 2026-09-18, where the author accepted every item; those that changed in review say so.

1. **`compound_task`, not `task`, on `Method`.** Accepted. The brief writes "its `task`". A slot named `task` would need range `CompoundTask` on `Method` and `CompoundTaskInstance`, `PrimitiveTask` on `PrimitiveTaskInstance`, and both on `Subtask`; a global slot with per-class ranges is legal LinkML but its one docs page would state one range and mislead. Two slots, `compound_task` and `primitive_task`, each with one range, serve all five uses and read unambiguously in every record. HDDL's `:task` is what the exporter writes.
2. **A subtask names its task through two reference slots and a rule, not one string.** Accepted. A string slot leaves the check to tier 2 and gives the projection no reference to turn into the Method-to-task edge the brief's opening picture needs. An `any_of` range renders as a plain string and would be a construct outside the rule table. Two reference slots with an exactly-one rule, precondition on `arguments`, reach tier 1 in list form, probed both ways.
3. **`arguments` for a subtask's parameter sequence.** Accepted. The PDDL note's `rep_b.yaml` reused `parameters` for it; here `parameters` is the keyed declaration map on three classes, and one global slot cannot be a map on one class and a list of strings on another without the same docs problem as decision 1. The clash is between the declaration map and the subtask's list, not between methods and tasks, so prefixed declaration slots would not remove it. HDDL's own phrase is "parameter sequence".
4. **A binding is one line, `r: mason_m1_1`, and the projection reads the kind from the catalogue.** Reviewed 2026-09-18, replacing the first draft's three typed slots with `""` in the two unused ones. The draft restated the kind in every binding so that the projection could make the edge from the metamodel alone, under the brief's sentence "the component projects using LinkML's own metamodel and nothing else" and its one allowed exception, `count`. Review found that sentence too strict for this case: the kind of `r` is a declared fact in the validated catalogue, the same documents the component already indexes for tier 2, and reading it is a deterministic lookup, not a guess and not an annotation, which is what the sentence was written against. So the brief admits a second data-keyed rule (prerequisite 4), `ParameterBinding` has one value slot, and the one-line form is what the planner writes. What is lost: the graph shape of `bindings` can no longer be read off the schema alone, and a two-id or kindless binding is caught at tier 2 rather than tier 1.
5. **Each instance binds exactly its own task's parameters: the compound its compound task's, the primitive its primitive task's.** Decided in review 2026-09-18 as the shape truest to HDDL, replacing the draft in which the compound bound all of its method's variables. The IPC solution format, the attested HDDL output, writes a decomposition as `<id> <task> <args> -> <method> <child ids>`: the compound carries its task's arguments only, and the method's own variables (`r`, `from`, `to` in `m_transport`) exist only in the subtasks' arguments. So `bindings` keys are always the task's parameters, the same before and after decomposition, nothing is bound twice, and stage two's rewrite of a leaf's `robot` conflicts with nothing on the compound. Agreement between records is a tier 2 check through the method's `arguments`: a variable shared by two lines binds equal on both subtasks, a variable that is the compound task's parameter binds equal to the compound's, the `robot` variable equal within its entry. The brief's two sentences saying the compound "binds that method's variables once" and that the method's `robot` variable "is bound once on the CompoundTaskInstance and its children inherit it" are amended to this; its "no copy is written" stays true and now covers bindings as well as ordering.
6. **The tree is written top-down: a decomposed compound lists its `subtasks`, and `TaskInstance` is the range they share.** Decided 2026-09-18 in the plan review, replacing the accepted draft in which every instance carried `parent` and `position`, a network task `parent: ""` and `position: 0`. That draft was the module's one departure from HDDL's own shape, taken because a reference slot ranges one class and a compound's subtasks are of two; its cost showed in the plan review, where the author could not read `position: 0` beside an `ordering` counted from 1. HDDL's decomposition, and the IPC line that writes it, list the subtasks on the compound in the method's order, and the plain LinkML way to give that list one range is a class both instance classes `is_a`: `TaskInstance`, HDDL's "task" when the kind is not stated. So `CompoundTaskInstance.subtasks` ranges `TaskInstance`, entry `i` realises line `i` of the method and inherits its order from the method's `ordering`, and the module orders everything by one mechanism. Probed the same day: `record_type` locks per subclass through `is_a`; the inherited slots appear in each subclass's JSON Schema; a missing `subtasks` key fails naming it; a `subtasks` key on a primitive fails as an additional property. One slot named `subtasks` serves both the method and the instance because HDDL has one word; the cost is gen-doc's slot page, which states range `string` while each class page states the right range, accepted. The brief's inheritance policy, previously `is_a` in product only, admits process's two bases, this one and decision 18's.
7. **The initial task network is a record, `TaskNetwork`, shaped like a method body.** Decided in review 2026-09-18, replacing the first draft's `after` slot on each network task. HDDL's `:htn` block reuses the method body's grammar, a labelled task list and ordering pairs, and the IPC solution format opens with a `root <ids>` line; both point at one record listing the network's tasks. `TaskNetwork` carries `tasks`, the ordered ids of the compounds no compound lists, and `ordering`, the same pair list a method carries, so the module has one ordering mechanism, and after decision 6 the network reads exactly as a decomposed compound does: a list and the order over it. Tier 2 checks that every instance is listed exactly once. A step number per task was considered and set aside because it cannot write every partial order HDDL can.
8. **`record_type` only on the six record classes**, declared on their bases where they have one, not on `Parameter`, `Subtask`, `ParameterBinding`. Accepted. The brief says "every process class". The three are inlined value-like objects never validated on their own, like `Position`; a designator inside every one-line entry would end the one-line form.
9. **Catalogue optional where sensible, plan side required-everywhere** with `""` and `0` sentinels. Accepted. The catalogue is hand-authored, so `applies_to` is optional and means "any component" when absent; the plan side is planner output, so every slot is a required key, product's convention.
10. **A primitive instance is never a task of the network.** Accepted as the simplest shape. `tasks` ranges `CompoundTaskInstance` only; since a reference's class is not checked at tier 1, the check is the tier 2 row on listing. HDDL's initial network may hold a primitive directly; here a standalone action needs a compound and a one-subtask method around it, as Transport wraps `noop` in `get-to` and `m-i-am-there`, though there for the sake of alternatives. The gain is one class of network task and a control node above every leaf in the behaviour tree. `tasks` could range `TaskInstance` as `subtasks` does and admit primitives at the top; declined for the behaviour tree's sake, revisit if a real plan needs it.
11. **A pattern on `decomposed_by`.** Accepted. `decomposed_by` names what HDDL Definition 5 (Höller et al. 2020, §2 p. 3 of the arXiv version) defines, the decomposition of a task by a method, which the IPC solution line writes as `-> <method>`; the slot name is ours, not a quotation. It takes the catalogue name pattern or empty. The first draft also had GlobalId-or-empty and machine-id patterns on the three typed binding slots; with one `bound_to` slot for three id shapes there is nothing a single pattern can say, so the kind check is tier 2 alone.
12. **`duration` recommended in seconds.** Accepted. The brief fixes no unit; HDDL 2.1 wants integers, and seconds are the finest unit a construction schedule needs.
13. **One name pattern for all catalogue ids, allowing underscores.** Accepted. It is HDDL's `<name>` token without the hyphen. The PDDL note fixed `^[A-Za-z][A-Za-z0-9]*$` for primitives from the reference's behaviour tree rule; the underscore is added so method ids can be `m_prefab`, and applied to all three so the shared task namespace has one rule. Instance ids carry no pattern; the ids in the example, the listing compound's id plus the entry's number, are a convention, and LinkML's `equals_expression` and `string_serialization` could document it but are read only by the runtime's inference utility, never by the validator or the JSON Schema generator (checked in the installed 1.11.1), so enforcing it would be tier 2 or the planner's own rule.
14. **Four example primitives, two compound tasks, two methods, one network.** Accepted. The reference's `MoveTo`, `Attach`, `Detach` plus `Place`, so that one `requires` has two entries and one method has a compound subtask. `Transport` and `ConstructComponent` are the brief's own. The network holds two walls so `ordering` has a pair and one task stays undecomposed.
15. **Invalid documents, one per mechanism, eleven.** Accepted. Required slot, `minItems` on three slots, the name pattern, the enum through the one-line form, the full form's required kind, the one class rule, the array slot, the designator, and the required list on the instance side. Each is one record and is validated under its class directly, not through the split.
16. **One catalogue file and one plan file, split by `record_type` for validation.** Decided in review 2026-09-18. The first draft had one file per class, three for the catalogue and three for the plan, because `linkml-validate` checks one class per run and the model has no `tree_root` container (common decision 10). Review found the split an artifact of the validator, not of the model: an author writes one catalogue, and a plan is one thing a planner hands over. Since every record carries `record_type`, the harness groups a file's records by it into temporary per-class files and validates each with `-C`; nothing in the schema changes, and the generator will do the same grouping natively. A container class without `tree_root` was considered and set aside: it would need a projection rule for a wrapper that is neither a node nor flattened onto an owner. `record_type` thereby becomes load-bearing rather than a guard, and a missing or unknown one is a harness error naming the record. Product's four files are left as they are, with the merge recorded as a follow-up on the map.
17. **The `"null"` inside the array slot's rendering is accepted**, and the toolchain criterion reworded, rather than post-processing it away in `build.py`. Accepted. It is the generator's lax array form, not an optional-slot null, and a build-script change for one slot would be a toolchain change this module should not make.
18. **`Task` is the base of `PrimitiveTask` and `CompoundTask`, so that the catalogue side has the shape the plan side has.** Decided 2026-09-18 in the plan review, after decision 6. Nothing forces it: no catalogue slot lists both kinds in one place, so the two classes validated on their own. It is there because the author wants both sides to read alike, `Task` over the two catalogue kinds as `TaskInstance` over the two instance kinds, both never written as records. What it also gives: the four shared slots and the name pattern declared once, and one label over every catalogue task. `CompoundTask` adds no slot, which is HDDL's own statement about it, and it is kept as a class rather than folded into `Task`, because `is_a` says "is a kind of" and a primitive task is not a kind of compound task, and because the plan side cannot fold the same way without every leaf inheriting `subtasks`. The two task-reference slots, `primitive_task` and `compound_task`, and the `Subtask` rule stay as decisions 1 and 2 have them: a base would allow one `task` slot ranging `Task`, considered and declined, because the author wants the kind readable on the line that names the task. Probed the same day: `record_type` locks per subclass, both subclasses carry the four inherited slots and the pattern in their JSON Schema, an extra slot on a `CompoundTask` record fails as an additional property, the docs index nests both under `Task`, and no name collides.
19. **`applies_to` is a slot of `Method`, single-valued, ranging `MaterialCategory`; `Parameter` is name and kind only.** Decided 2026-09-21 after Task 2, reversing the spec's first shape, in which `applies_to` was a list of material strings on the method's component parameter declaration. The author objected that the declaration mixed HDDL's typed variable with the method's scope, and the trace confirmed three structural defects: the statement "this method builds masonry walls" was written as a property of the variable `c`; the shared `Parameter` class let a task parameter or a `location` parameter carry `applies_to`, which needed a tier 2 check to forbid; and the projection flattened the list onto the Method node under the author's variable name, `c_applies_to`, so the brief's opening query could not be written once for all methods. On `Method` the slot cannot be misplaced and the property has one name. What the value is: the raw IFC strings, "Basic Wall:Exterior - Brick on Block", cannot be what a catalogue is written against, so a mapping step outside the schema turns them into a closed vocabulary, `MaterialCategory` in common (prerequisite 7), and `applies_to` names one of those. Single-valued because the vocabulary exists only to select methods and is cut at the granularity they distinguish, so every method has exactly one category by construction; a method that wants two is a sign the vocabulary is cut wrong, and the list's original reason, several spellings of one material, is what the mapping step removes. The HDDL reading, from `docs/research/pddl-for-process.md` Appendix B.1 rerun on 2026-09-21: a method is restricted either by a subtype on its own parameter, `?e - masonry-element`, or by a precondition over a fact of the element, `(material ?e masonry)`; both solve in Aries and both exclude, not prefer, and neither puts anything but a type on the declaration. The schema stores the category and leaves the form to the export. Considered and declined: a keyed constraint entry per parameter, HDDL's variable constraint made literal, which covers a compound task with two component parameters that no task has; and the string type `MaterialName` as the join, replaced by `MaterialCategory` in common for the vocabulary (`SPEC-common.md` decisions 15 and 17) and the `Material` class in product for the shared record that carries the string as its id and its category (`SPEC-product.md` decision 17). The vocabulary was an enum for one day, taken for tier 1 checking on both sides and visible values in the JSON Schema, and returned to a class with a document the same evening: a company adopting the schema adds a category in a document, never in the schema, and the join `category` to `applies_to` is made type safe by `tests/test_references.py` and the generator's tier 2 rule instead.

## Open Questions

None. Every decision above was accepted in review on 2026-09-18, and decisions 6 and 18 in the plan review the same day. One question raised in review is closed without a change: the instance classes keep common's `id` as their identifier, although on them it holds a planner-minted string rather than a catalogue name, because the rule table reads `identifier: true` rather than the slot's name and every other module identifies its classes the same way; the meaning per class is in `slot_usage`, as product and resource already do.
