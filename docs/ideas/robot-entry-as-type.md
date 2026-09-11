# Robot Entry as Type

*Idea one-pager, 2026-09-11. Output of an idea-refinement session on the resource module. Refines the resource side of `linkml-product-process-graph-schema.md`; its amendments were applied to that brief and to `CAPABILITY-MAP.md` on 2026-09-11.*

## Problem Statement
How might we let someone enter a robot from its Construction Robot Schema attributes alone, with no type to choose, and still give the planner something coarser than one machine to allocate against and the orchestrator one machine to point at?

## Recommended Direction
Five classes. `RobotUnit` is the entry: `id`, `count`, `status`, and four single-valued slots holding one object each of `PhysicalProperty`, `OperationalRequirement`, `Safety`, and `Activity`, the four groups of the Construction Robot Schema (CRS, Li et al. 2026). Each group class carries its own `id` and the CRS attributes of its group; `offers`, the capability types the robot provides, sits in `Activity` where the paper's `Task Type` is. An entry describes one robot product as the paper describes it; two identical machines are one entry with `count: 2`. Nobody decides what type their robot is, because the entry is the type. `RobotType` is retired.

The generator turns one entry into `count` machine nodes, `sam100_1` and `sam100_2`, each linked to the same four group nodes and the same capabilities. Ids are always suffixed, even at count 1. This is the one rule in the generator keyed on a named slot rather than on the metamodel, `RobotUnit.count`, recorded as such. It puts into the graph exactly what the planner export needs, one object per machine with its capability facts, so the export is a straight walk.

Planning allocates by capability. A primitive task `requires` a set of capability types; a machine's `Activity` `offers` a set; the match is containment. A robot with three capabilities is one object with three facts, never three objects. Orchestration allocates one machine node and writes its `status`. Everything else that differs between machines, position, battery, wear, is runtime state read from the robot and lives outside the model.

## What This Fixes in the Resource Schema
- **Five classes, four of them groups.** `RobotUnit` plus `PhysicalProperty`, `OperationalRequirement`, `Safety`, `Activity`. Each group class has `id`, authored, so that by the existing projection rule it becomes a node with an edge rather than flattening into the robot. A group left out of a document is simply absent: no node, no edge.
- **`offers` is required, multivalued, range `CapabilityType`, on `Activity`.** It replaces the CRS `Task Type` attribute and stays in the paper's group. An allocation query is two hops, machine to `Activity` to capability; the PDDL export walks the same two hops to write one `offers` fact per machine. Because `offers` is required, so is the `Activity` group.
- **`count` is required, integer, at least one, on `RobotUnit`.** It replaces authored machines. The generator reads it; nothing else does.
- **`status` on `RobotUnit`, enum `idle`, `deployed`, `charging`, `out_of_service`, default `idle`.** Written onto every machine node at load, updated by orchestration. The one runtime slot in the model, and the substrate for the brief's resource-availability relation kind.
- **CRS attributes live in their group class, all optional.** A thin spec sheet still validates. No `label`: the entry id is a readable product slug such as `sam100`; group ids follow it, `sam100_physical`.
- **Numbers with a dimension are `Quantity`.** Value and unit, as common defines it, flattened to `_value` and `_unit` properties inside the group node. The CRS pairs `Productivity` and `Productivity Units`, and likewise precision and accuracy, become one `Quantity` each.
- **Renamed attributes name their origin.** `id` on `RobotUnit` says it is the CRS `Name`; `Activity.offers` says it is `Task Type`. Attributes that keep the CRS name carry no attribution. The full lineage table is in the spec.
- **`Activity Type` and `Material` are dropped.** The process side owns them, as compound tasks and method applicability.
- **Different capabilities, different entry.** A SAM100 fitted with a gripper and one fitted with a drill are two entries if their `offers` differ.

### Required
Planning needs to know what a robot can do and how many there are; orchestration needs a machine to write to. That fixes the required set, and nothing else is required.

| Slot | Why |
|---|---|
| `RobotUnit.id` | The entry's name; every machine id is derived from it. |
| `RobotUnit.activity`, and `Activity.offers` with at least one | Without a capability the entry can never be matched to a task. |
| `RobotUnit.count`, at least one | Without a count the generator cannot create a machine node. |
| `id` on any group object that is present | The group projects to a node, and a node needs an identifier. |

`status` is not required: it defaults to `idle` and orchestration owns it from there. The other three groups are optional, and every attribute inside any group is optional, so an entry with `id`, `count`, and an `Activity` holding only `id` and `offers` is valid.

### One robot, as a document
```yaml
- id: sam100
  count: 2
  status: idle
  activity:
    id: sam100_activity
    offers: [locomote, grip, align]
  physical_property:
    id: sam100_physical
    manufacturer: Construction Robotics
    length: {value: 3.0, unit: m}
    load_capacity: {value: 15, unit: kg}
  safety:
    id: sam100_safety
    safety_barrier: true
```

### The same robot, in the graph
```
(:RobotUnit {id: sam100_1, count: 2, status: idle})
(:RobotUnit {id: sam100_2, count: 2, status: idle})
  each -[:ACTIVITY]-> (:Activity {id: sam100_activity}) -[:OFFERS]-> (:CapabilityType {id: locomote}), (grip), (align)
  each -[:PHYSICAL_PROPERTY]-> (:PhysicalProperty {id: sam100_physical, manufacturer: ..., length_value: 3.0, length_unit: m, ...})
  each -[:SAFETY]-> (:Safety {id: sam100_safety, safety_barrier: true})
```

## Validation Done
Three throwaway PDDL 2.1 problems with durative actions, one shared domain, solved by the Aries temporal planner through `unified-planning`. Each robot is one object; its `Activity.offers` are init facts on that object; each durative action requires its capability over its whole duration and holds a `free` lock on the robot from start to end. Durations are placeholders for the `duration` slot on `PrimitiveTask`; the `at-target`, `gripped`, `aligned` chain stands in for the method's subtask ordering. Plans were satisficing, so makespans show feasibility, not optimality.

### Domain
```lisp
(define (domain robots-temporal)
  (:requirements :strips :typing :durative-actions)
  (:types robot capability component)
  (:constants locomote grip align - capability)
  (:predicates
    (offers ?r - robot ?c - capability)
    (free ?r - robot)
    (at-target ?x - component)
    (gripped ?x - component)
    (aligned ?x - component))
  (:durative-action do-locomote
    :parameters (?r - robot ?x - component)
    :duration (= ?duration 4)
    :condition (and (over all (offers ?r locomote)) (at start (free ?r)))
    :effect (and (at start (not (free ?r))) (at end (free ?r)) (at end (at-target ?x))))
  (:durative-action do-grip
    :parameters (?r - robot ?x - component)
    :duration (= ?duration 2)
    :condition (and (over all (offers ?r grip)) (at start (free ?r)) (at start (at-target ?x)))
    :effect (and (at start (not (free ?r))) (at end (free ?r)) (at end (gripped ?x))))
  (:durative-action do-align
    :parameters (?r - robot ?x - component)
    :duration (= ?duration 3)
    :condition (and (over all (offers ?r align)) (at start (free ?r)) (at start (gripped ?x)))
    :effect (and (at start (not (free ?r))) (at end (free ?r)) (at end (aligned ?x)))))
```

### Problem 1: one entry per robot
```lisp
(define (problem entry) (:domain robots-temporal)
  (:objects sam100 anymal - robot b1 b2 - component)
  (:init (offers sam100 locomote) (offers sam100 grip) (offers sam100 align) (offers anymal locomote)
         (free sam100) (free anymal))
  (:goal (and (aligned b1) (aligned b2))))
```
```
 0.0 -  4.0  do-locomote(sam100, b1)
 0.0 -  4.0  do-locomote(anymal, b2)
 4.1 -  6.1  do-grip(sam100, b2)
 6.2 -  8.2  do-grip(sam100, b1)
 8.3 - 11.3  do-align(sam100, b1)
11.4 - 14.4  do-align(sam100, b2)
makespan 14.4
```
`sam100` holds three `offers` facts and does every grip and align, one at a time. It overlaps only with `anymal`, a different machine.

### Problem 2: count 2, one object per machine
```lisp
(define (problem count2) (:domain robots-temporal)
  (:objects sam100_1 sam100_2 anymal - robot b1 b2 - component)
  (:init (offers sam100_1 locomote) (offers sam100_1 grip) (offers sam100_1 align)
         (offers sam100_2 locomote) (offers sam100_2 grip) (offers sam100_2 align)
         (offers anymal locomote) (free sam100_1) (free sam100_2) (free anymal))
  (:goal (and (aligned b1) (aligned b2))))
```
```
 0.0 -  4.0  do-locomote(sam100_1, b1)
 0.0 -  4.0  do-locomote(sam100_2, b2)
 4.1 -  6.1  do-grip(sam100_1, b1)
 4.1 -  6.1  do-grip(sam100_2, b2)
 6.2 -  9.2  do-align(sam100_1, b1)
 6.2 -  9.2  do-align(sam100_2, b2)
makespan 9.2
```
Both bricks proceed in parallel. This problem is exactly the graph shape the generator now produces from `count: 2`.

### Problem 3: a third robot that grips but cannot align
```lisp
(define (problem three) (:domain robots-temporal)
  (:objects sam100 anymal gripbot - robot b1 b2 - component)
  (:init (offers sam100 locomote) (offers sam100 grip) (offers sam100 align)
         (offers anymal locomote)
         (offers gripbot locomote) (offers gripbot grip)
         (free sam100) (free anymal) (free gripbot))
  (:goal (and (aligned b1) (aligned b2))))
```
```
 0.0 -  4.0  do-locomote(sam100, b1)
 0.0 -  4.0  do-locomote(anymal, b2)
 4.1 -  6.1  do-grip(gripbot, b1)
 6.2 -  8.2  do-grip(gripbot, b2)
 8.3 - 11.3  do-align(sam100, b1)
11.4 - 14.4  do-align(sam100, b2)
makespan 14.4
```
`gripbot` grips both bricks and is never asked to align. `sam100`, the only robot offering align, aligns both. No robot appears in an action its `offers` does not cover.

### Findings
A multi-capability robot is one object and is never used twice at once. `count` is what unlocks parallelism, and one object per machine is the shape the planner wants, so the generator produces it. The planner picks by capability and by nothing else. Splitting a robot into one object per capability was not run: it would treat one machine as three, which is the failure the direction avoids.

## Key Assumptions to Validate
- [ ] **`status` is the only per-machine fact the model needs.** Position, battery, and wear stay outside. Test: when process specifies stage two, confirm it reads only `status` from a machine node and the group nodes for `offers` and quantities. If it needs more, add a slot, not a class.
- [ ] **One named-slot rule in the generator is acceptable.** `RobotUnit.count` is the first departure from projecting by metamodel alone. Test: when the generator is specified, it stays the only one; a second such rule reopens this decision.
- [ ] **A spec sheet maps onto the CRS slots.** The paper warns manufacturers publish little. Test: author the example entries and note which slots stay empty.
- [ ] **One `free` lock per robot is enough for the export.** A robot that can locomote while gripping would need a per-capability lock. Test: process decides when it specifies durations and ordering; resource carries nothing for it.

## MVP Scope
**In.** `schema/resource.yaml` with the five classes and the `status` enum, importing common. Fictional example entries under `examples/resource/`, plus one invalid document. Rows in `tests/test_examples.py`. Generated `dist/resource.schema.json` and `docs/model/resource/`. The lineage table, CRS attribute to slot and group, in `SPEC-resource.md`.

**Out.** `RobotType`. `position` or any runtime state beyond `status`. Closed enums for the five CRS enum attributes, since the paper publishes no value sets. Anything the process side owns: the assigned-machine slot, durations, locks, the PDDL export. The generator itself.

## Not Doing (and Why)
- **`RobotType` as a class.** Identical machines share one entry; machines are generated from `count`. A type over entries would have nothing left to say.
- **Type as a capability class, "every robot that can grip is Type B".** A robot with two capabilities would be two objects and could be planned twice at once. The entry is the type instead.
- **Deriving types by grouping entries with equal `Activity.offers`.** Not needed once the entry is the type; a group would have no name to write in a plan.
- **CRS attributes as flat slots on the robot.** One node with about fifty properties is hard to read and to query. Four group nodes match the paper and let a query touch one group.
- **Generator-minted group ids.** Would need a second named rule to tell a group object from a `Quantity`. Four authored ids per robot is cheaper.
- **`position` on the resource side.** Not in the paper; changes every second; read from the robot, not from a catalogue.
- **`label` on `RobotUnit`.** The id is a readable product slug already.

## Open Questions
None. Status values fixed 2026-09-11 as `idle`, `deployed`, `charging`, `out_of_service`.
