# Parameter Kinds: Mapping the Reference `actions.json` onto a Closed Set

*Research note, 2026-09-10. Answers the second checklist item in `docs/ideas/linkml-product-process-graph-schema.md` ("A closed set of parameter kinds covers every primitive in the reference `actions.json`. Test: enumerate, map every existing parameter, list what doesn't fit."). Inputs are repo files only.*

## Inputs

| File | Role in this note |
|---|---|
| `docs/ideas/linkml-product-process-graph-schema.md` | The brief. Sections used: Recommended Direction (l. 8–13), Domain Structure: HDDL (l. 22–35), Preconditions as Relation Kinds (l. 38–48), Open Questions first bullet (l. 100). |
| `docs/reference-schemas/actions.json` | The three primitive actions and one compound whose parameters are mapped. |
| `docs/reference-schemas/action.schema.json` | How a parameter is currently declared: `#/$defs/parameter/properties/value` is "a JSON Schema, not the name of one", stored as data per slot. |
| `docs/reference-schemas/common.schema.json` | The shared value types the `$ref`s resolve to (`position`, `vec3`, `rotation`, `element_id`, `quantities`, identifiers, `provenance`, `envelope_head`). |
| `docs/reference-schemas/capability.schema.json`, `capabilities.json` | Target of `requires_capabilities`; the capability descriptions are the only in-repo evidence for future parameter kinds. |
| `docs/reference-schemas/process.schema.json` | Where the reference puts duration and the robot binding (on the task instance, not the action), and how a task instance carries parameter values. |
| `docs/reference-schemas/product.schema.json`, `resource.schema.json` | Other consumers of the `common` defs; the `offers` side of capability matching. |

## 1. Parameter-by-parameter mapping

Every parameter of every primitive in `actions.json`. JSON pointers are into `docs/reference-schemas/actions.json`.

| Action | Parameter | Current declared value type (`$ref`) | Pointer | Proposed kind | Notes |
|---|---|---|---|---|---|
| `MoveTo` | `target` | `common.schema.json#/$defs/position` | `/actions/0/parameters/target` | **Position** | An independent binding: "Where to go." Nothing on the product side determines it. Fits without qualification. |
| `Attach` | `object` | `common.schema.json#/$defs/element_id` | `/actions/1/parameters/object` | **ElementReference** | "The element taken into custody." This is the brief's "Acts on element" pattern (brief l. 46): a reference slot with range `Element`, projecting to an edge. Fits. |
| `Attach` | `target` | `common.schema.json#/$defs/position` | `/actions/1/parameters/target` | **Position** | Description says "resolved from the referenced product element". That claim does not hold: the product side holds only the as-designed `geometry.location` (`product.schema.json#/$defs/geometry/properties/location`), and Attach happens where the element currently is (staging, delivery), which no product field records. So `target` is a genuinely independent binding, not a derived one. Fits as Position; see section 2 for the description fix. |
| `Detach` | `object` | `common.schema.json#/$defs/element_id` | `/actions/2/parameters/object` | **ElementReference** | Same as `Attach.object`. Fits. |
| `Detach` | `target` | `common.schema.json#/$defs/position` | `/actions/2/parameters/target` | **Position** | Here the "resolved from the referenced product element" claim does hold: the release point is the element's designed `geometry.location`. The binding is derivable, but keeping it explicit costs nothing and keeps the two halves of the grasp/release pair symmetric. Fits as Position; but note the placement-orientation gap in section 2. |

Coverage: 5 parameters, 2 distinct value types, 2 kinds. Every parameter fits one of the brief's candidate kinds. The compound `TransportComponent` (`/compounds/0`) declares no parameters at all (`action.schema.json#/$defs/compound_action` description: "no `parameters` and no `requires_capabilities`"); the brief's `Transport(element)` adds one, of kind ElementReference (see section 6).

Kinds from the brief's candidate list that **no parameter in the data uses**: quantity with unit, enumeration, duration, resource reference. Each is dispositioned in sections 3 and 4.

## 2. What does not fit, or fits with a caveat

Nothing is unmappable. Four observations qualify the "fits":

1. **`Attach.target` is mis-described, not mis-typed.** `actions.json` `/actions/1/parameters/target/description` says the position is "resolved from the referenced product element". The product schema has one location per element, the designed one (`product.schema.json#/$defs/geometry`, `required: ["location"]`). For a prefab element picked up from a staging area that is the wrong point. Either the description changes to "supplied by the plan" or the product side grows a current/staging position. The kind (Position) is right either way; the provenance claim is wrong for Attach and right for Detach.

2. **A position alone under-specifies placement.** `Detach.target` is a `position` (three numbers, `common.schema.json#/$defs/position` refers to `#/$defs/vec3`). Placing a wall needs an orientation; the product side already carries one (`product.schema.json#/$defs/geometry/properties/rotation` refers to `common.schema.json#/$defs/rotation`). The data does not force a new kind, so this note does not add one. If it becomes necessary, the right move is a **Pose** kind (Position plus Rotation) rather than a separate Rotation kind, since no action needs orientation without location. Recorded as a gap, not a kind.

3. **Duration is a slot, not a parameter kind.** No action in `actions.json` takes a duration as a parameter. The reference puts duration on the task instance: `process.schema.json#/$defs/plan_task/properties/planned_duration_seconds` (required on primitive, forbidden on compound) and `#/$defs/run_task/properties/actual_duration_seconds`. The brief likewise puts it on `PrimitiveTask` as its own slot (brief l. 19, l. 27, l. 83), following HDDL 2.1 durative actions. So "duration" belongs in the model as a **value type** (a `Duration` class, or a `Quantity` constrained to a time unit) used by the `duration` slot, but it is **not a parameter kind** unless a primitive such as `Cure(element, duration)` appears. The `surface_treatment` capability ("humidity maintenance", `capabilities.json` `/capability_types/8`) is the one hint that such a primitive may come. Recommendation: define `Duration` once, use it for the slot now, admit it to the parameter-kind enum only when a primitive needs it. Adding a permissible value to a LinkML enum is an additive change.

4. **Resource reference is excluded by design, not merely unused.** `action.schema.json#/$defs/parameter/properties/value` carries a `not` guard against `common.schema.json#/$defs/robot_id` and says why: "no parameter may take a concrete robot as its value, because an action states the capability it requires and the robot is matched at dispatch." The brief agrees (l. 53: "The planner never sees individual robots"; l. 83: "a slot on the instantiated primitive for its assigned unit"). The robot binding is therefore the `assigned_unit` slot on the instantiated primitive (reference counterpart: `process.schema.json#/$defs/run_task/properties/robot_id`), and **ResourceReference is not a parameter kind**. Admitting it would reopen the door the reference deliberately closed. A CapabilityType reference is likewise not a parameter; it is the `requires` relation (section 7).

Also not forced by the data: **Enumeration**. The reference schemas contain enums (`product.schema.json#/$defs/method_id` with `prefab | insitu | masonry | 3dcp`; `process.schema.json#/$defs/run_mode`, `plan_origin`, `outcome`; `unresolved_reason`), but none is an action parameter. The `resource.schema.json#/$defs/crs` description explicitly keeps CRS enums open ("no value set is closed; closing one is a major"). Recommendation: do not add an Enumeration kind until a primitive needs one (a `Fasten(element, mode: {bolt, weld})` would). LinkML enums are native, and the kind can be added as one enum value plus one binding class with no change to the projection rule table.

## 3. (a) The minimal closed set

Two tiers, stated separately so the evidence is not overstated.

**Forced by the data (covers all five parameters):**

| Kind | LinkML class | Slots | Projection (per brief l. 11) |
|---|---|---|---|
| **Position** | `Position` | `x: float`, `y: float`, `z: float`, all required. Coordinate frame is the baseline's, implicit, as `common.schema.json#/$defs/position` says. | Identifier-less inlined object, flattened to prefixed properties (`target_x`, `target_y`, `target_z`) on the owning node. |
| **ElementReference** | none new; a slot with `range: Element` | The `Element` class carries `element_id` as `identifier: true` (from `common.schema.json#/$defs/element_id`, an IFC GlobalId). | Reference slot, becomes an edge from the instantiated primitive to the Element node. This is the "Acts on element" relation kind (brief l. 46). |

**Reserved by the brief, with in-repo evidence that it is coming, recommended for the first closed set:**

| Kind | LinkML class | Slots | Evidence | Projection |
|---|---|---|---|---|
| **Quantity** (quantity with unit) | `Quantity` | `value: float` required, `unit: string` required (or a `UnitEnum` if the unit vocabulary is to be closed), `provenance: string` optional. Mirrors one entry of `common.schema.json#/$defs/quantities/additionalProperties` exactly. | No action parameter uses it yet, but the capability vocabulary already names the parameters that will: "stated tolerance" (`alignment`), "stated torque" (`fastening`), "controlled rate" (`extrusion`), "stated thickness" (`mortar_application`), "stated precision" (`calibration`), all in `capabilities.json` `/capability_types`. Also needed for element quantities on the product side (`product.schema.json` l. 108, 294) and the `offers` qualifier question (brief l. 101). | Identifier-less inlined object, flattened (`tolerance_value`, `tolerance_unit`). |

Proposed closed set for the MVP: **Position, ElementReference, Quantity**. Held in reserve, defined as value types but not admitted as parameter kinds until a primitive needs them: **Duration** (slot on `PrimitiveTask`), **Enumeration**, **Pose**. Rejected: **ResourceReference**, **CapabilityReference**.

### How declaration and binding are modelled

The reference stores a JSON Schema per parameter (`action.schema.json#/$defs/parameter/properties/value`, "There is no separate type vocabulary"). The brief replaces this with a closed set of typed kinds (l. 13). In HDDL terms the kinds are exactly the `(:types ...)` declaration, and a parameter is a typed variable `?e - element`. The LinkML shape that follows:

```yaml
enums:
  ParameterKind:
    permissible_values:
      position: {}
      element_reference: {}
      quantity: {}

classes:
  ParameterDeclaration:          # catalogue side, on PrimitiveTask and CompoundTask
    slots: [name, kind]          # name: string (pattern ^[a-z][a-z0-9_]*$ from action.schema.json#/$defs/parameter_name)
                                 # kind: ParameterKind, required
  PrimitiveTask:
    slots: [id, description, parameters, requires, duration]
    slot_usage:
      parameters: {range: ParameterDeclaration, multivalued: true, inlined_as_list: true}
      requires:   {range: CapabilityType, multivalued: true, required: true}
      duration:   {range: Duration}

  ParameterBinding:              # instance side, abstract; one subclass per kind
    abstract: true
    slots: [parameter]           # the declared name it fills
  PositionBinding:
    is_a: ParameterBinding
    slots: [value]               # range Position, inlined
  ElementReferenceBinding:
    is_a: ParameterBinding
    slots: [element]             # range Element, not inlined -> edge
  QuantityBinding:
    is_a: ParameterBinding
    slots: [value]               # range Quantity, inlined
```

The one-to-one correspondence between `ParameterKind` values and `ParameterBinding` subclasses is what makes the brief's tier-2 example checkable (brief l. 67: "A filled parameter is a position where the kind says element reference"). It is a tier-2 check because it crosses two documents (catalogue declaration, instance binding), which `linkml.validator` does not join.

**Dependency on an open question.** `parameters` (catalogue) and the binding list (instance) are both *multivalued, identifier-less, inlined* value objects. That is exactly the brief's fourth open question (l. 103: "rejected, or promoted to nodes? The rule table must say"). This mapping is the first concrete case that forces an answer. Two workable options: give `ParameterDeclaration.name` (and `ParameterBinding.parameter`) `key: true` so the list is `inlined_as_dict`, and let the rule table flatten keyed inline dicts to `param_<key>_<slot>` properties; or promote both to nodes. The first keeps the catalogue a single node per task; the second makes the parameter a queryable node, which the "Acts on element" edge needs anyway for ElementReference (an edge has to leave from something). Recommendation: keyed inline for Position and Quantity bindings; the ElementReference binding's edge is emitted from the instantiated primitive node itself, with the parameter name as an edge property (`ACTS_ON {parameter: "object"}`).

## 4. (b) Summary of what does not fit

| Item | Verdict | Why |
|---|---|---|
| Any of the 5 parameters | Fits | All are Position or ElementReference. |
| Duration as a parameter kind | Not forced; wrong place | Reference and brief both put it on the task, not in the parameter list. Define the `Duration` value type, use it for the slot. |
| Enumeration as a parameter kind | Not forced | No action parameter is an enum; the reference's enums are on other classes. Add when a primitive needs it. |
| Resource reference as a parameter kind | Excluded by design | `action.schema.json#/$defs/parameter/properties/value` `not` guard; brief l. 53, l. 83. It is the `assigned_unit` slot. |
| `Attach.target` description | Description wrong, type right | Not derivable from the product side; see section 2 item 1. |
| Placement orientation | Gap, not a misfit | Position only; product side has rotation. Candidate `Pose` kind later. |
| `TransportComponent` parameter flow | Not expressible in the reference at all | The reference decomposition is a list of action ids with no bindings (`action.schema.json#/$defs/compound_action/properties/decomposition`). Which `target` each `MoveTo` gets is stated only in prose. See section 6. |

## 5. (c) Disposition of `common.schema.json#/$defs`

| `$def` | Pointer | Becomes | Reason |
|---|---|---|---|
| `position` | `#/$defs/position` | **Parameter kind** `Position` (class: x, y, z) | Used by 3 of 5 parameters and by `product.schema.json#/$defs/geometry` (`location`, `bounding_box.min/max`). "Where an element sits, and where a robot is asked to arrive: the same kind of fact, so the same definition" (its own description); the class keeps that. |
| `element_id` | `#/$defs/element_id` | **Plain LinkML type** (`string`), used as the `identifier` slot of `Element`; the **kind** is the reference slot `ElementReference` with `range: Element` | The kind is the reference, not the id string. Keeping `element_id` as a type preserves the IFC GlobalId join key (brief l. 18). |
| `quantities` (one entry) | `#/$defs/quantities/additionalProperties` | **Parameter kind** `Quantity` (class: value, unit, provenance) | The entry shape is a ready-made quantity-with-unit. Also the value type for element and task quantities. |
| `quantities` (the map) | `#/$defs/quantities` | **Dropped as a shape**; replaced by `quantities: Quantity` multivalued with a `name` key slot | An open-keyed map (`propertyNames` pattern, `additionalProperties`) is exactly the "open-ended structure as data" the brief rejects (l. 13). LinkML has no arbitrary-key dict without a key slot; the same projection decision as section 3 applies. |
| `vec3` | `#/$defs/vec3` | **Dropped** | Shape-only by its own description (`position`/`rotation` "carry the meaning"). LinkML has no fixed-length array the rule table would accept; `Position` and `Rotation` carry three named float slots instead. |
| `rotation` | `#/$defs/rotation` | **Plain LinkML class** `Rotation` (rx, ry, rz, radians), product side only; **not a parameter kind** | No action uses it. Consumed by `product.schema.json#/$defs/geometry/properties/rotation`. Would join `Position` in a `Pose` kind if placement orientation is ever needed (section 2 item 2). |
| `robot_id` | `#/$defs/robot_id` | **Plain LinkML type**, the `identifier` of `RobotUnit`; **not a kind** | Excluded as a parameter value by `action.schema.json`. Its process-side use (`process.schema.json#/$defs/run_task/properties/robot_id`) becomes the `assigned_unit` slot on the instantiated primitive (brief l. 83). |
| `schema_version` | `#/$defs/schema_version` | **Dropped from the domain model** | Document-level versioning; LinkML's schema `version` metaslot and the generated artifact carry it. Not a domain fact. |
| `baseline_version`, `plan_version`, `run_id`, `task_id` | `#/$defs/baseline_version` etc. | **Plain LinkML types** (string with pattern / uuid), for identifier slots of `Plan`, `Run`, `Task`; **out of MVP** | Brief l. 85: "Plan, Run, ExecutionRecord ... Out." `task_id` maps to the identifier of the instantiated task node when that slice arrives. Not kinds. |
| `provenance` | `#/$defs/provenance` | **Deferred class**, not a kind | It records what produced a derived artifact; derived artifacts (plan versions, runs, BTs) are out of MVP. Later a `Provenance` class inlined on those nodes. |
| `envelope_head` | `#/$defs/envelope_head` | **Dropped** | A payload envelope for the served API. A LinkML container/tree-root class plays that role; nothing domain-level survives. |

Also relevant, from the sibling vocabulary: `capability.schema.json#/$defs/capability_type_id` becomes the `identifier` of `CapabilityType`; `#/$defs/capabilities` (array, `minItems: 1`) becomes a multivalued reference slot with `required: true` (see section 7).

## 6. (d) `TransportComponent` and the repeated `MoveTo`

The reference: `actions.json` `/compounds/0/decomposition` is `["MoveTo", "Attach", "MoveTo", "Detach"]`; `action.schema.json#/$defs/compound_action/properties/decomposition` admits repetition on purpose ("Repetition is meaningful, so `uniqueItems` is absent: `TransportComponent` names `MoveTo` twice"). But the list carries only action identifiers. Which `target` the first `MoveTo` receives (the element's pickup point) versus the second (its design location) lives only in the prose description ("reach the element, take custody, carry it to where it belongs, release it"). The reference cannot express parameter flow; a loader has to guess. That is the judgment call the brief wants gone (l. 9).

HDDL solves this natively, and the brief says to use HDDL's words (l. 23). A method's subtask network is a set of **labelled task occurrences**, and ordering is over labels, not task names:

```lisp
(:method m-transport
  :parameters (?e - element ?from - position ?to - position)
  :task (Transport ?e)
  :ordered-subtasks (and
    (t1 (MoveTo ?from))
    (t2 (Attach ?e ?from))
    (t3 (MoveTo ?to))
    (t4 (Detach ?e ?to))))
```

Two occurrences of `MoveTo` are two subtasks, `t1` and `t3`, each with its own argument binding. The primitive is referenced twice; nothing is duplicated in the catalogue. In LinkML:

```yaml
classes:
  Method:
    slots: [id, refines, parameters, applies_to, subtasks, ordering]
    slot_usage:
      refines:    {range: CompoundTask, required: true}
      parameters: {range: ParameterDeclaration, multivalued: true}   # ?e, ?from, ?to
      applies_to: {range: ElementType, multivalued: true}             # the type constraint on ?e (brief l. 19, l. 43)
      subtasks:   {range: Subtask, multivalued: true, required: true}
      ordering:   {range: OrderingConstraint, multivalued: true}

  Subtask:                       # one labelled occurrence in one method's network
    slots: [id, label, task, bindings]
    slot_usage:
      id:       {identifier: true}          # e.g. m-transport.t3; unique across the catalogue
      task:     {range: Task, required: true}   # Task is the abstract parent of PrimitiveTask and CompoundTask
      bindings: {range: ArgumentBinding, multivalued: true}

  ArgumentBinding:               # "this subtask's parameter <parameter> is the method's variable <variable>"
    slots: [parameter, variable] # parameter: name on the referenced task; variable: name on the method
                                 # parameter has key: true -> inlined_as_dict

  OrderingConstraint:            # HDDL 2.1 style, over start/end events (brief l. 19, l. 110)
    slots: [before, before_event, after, after_event]
    slot_usage:
      before: {range: Subtask}
      after:  {range: Subtask}
      before_event: {range: TaskEvent}   # enum {start, end}
      after_event:  {range: TaskEvent}
```

Why `Subtask` must be an identified node and not an edge property. The obvious alternative is `Method -DECOMPOSES_INTO {label: "t1"}-> MoveTo` with a second parallel edge labelled `t3`; Neo4j permits parallel edges, so the two occurrences are distinguishable. But ordering must then refer to occurrences, and a property-graph edge cannot point at another edge. The subtask occurrence therefore has to be a node so that `AFTER` can join `t3` to `t2`. Under the brief's rule table (l. 11) this is the plain case: `Subtask` is an identified class, so a node; `task` is a reference slot, so an edge `OF_TASK` to the catalogue `PrimitiveTask`; `Method.subtasks` is a reference slot, so an edge `HAS_SUBTASK`. The path the brief wants to open the paper with (l. 35, `Method DECOMPOSES_INTO PrimitiveTask`) is then one hop longer, or `DECOMPOSES_INTO` is defined as the derived two-hop pattern in the query set. Both `MoveTo` occurrences resolve to the single `MoveTo` node, so "which primitives does this method need capabilities for" is still one traversal.

Bindings are the same identifier-less-inlined-multivalued case as section 3 and depend on the same open-question decision. With `parameter` as a key slot and keyed-dict flattening, subtask `t3` projects to a node with properties `label: "t3", binds_target: "to"`. Tier-2 checks that fall out: every `variable` names a method parameter; every `parameter` names a parameter of the referenced task; the kinds agree (`?to` is declared `position`, `MoveTo.target` is declared `position`).

Instance side (brief l. 33). An instantiated `Transport(e = wall-17)` points at its `CompoundTask` and at the chosen `Method`; the four instantiated primitives each point at their catalogue `PrimitiveTask` and carry filled bindings, so the two `MoveTo` instances are distinct nodes with distinct `target` values. Nothing is ambiguous there, and the reference already treats it so: `process.schema.json#/$defs/decomposition/properties/children` has `uniqueItems: true` because it lists instance `task_id`s, not action names. The BT mapping (brief l. 57) is likewise untroubled: BT.CPP allows the same registered node name (`action.schema.json#/$defs/action_id`, which "travels unchanged to the wire") to appear as several leaves with different port values.

## 7. `requires_capabilities` maps to `requires`

| Reference | Pointer | Brief |
|---|---|---|
| Action declares the capability types it needs | `action.schema.json#/$defs/primitive_action/properties/requires_capabilities`, which refers to `capability.schema.json#/$defs/capabilities` (array of `capability_type_id`, `minItems: 1`, `uniqueItems: true`) | `PrimitiveTask.requires`, multivalued reference slot, `range: CapabilityType`, `required: true`. Projects to one `REQUIRES` edge per capability (brief l. 35, l. 44). HDDL-wise it is "an ordinary primitive-task precondition" (l. 19), realised as a relation kind rather than a formula (l. 39). |
| Task instance repeats the action's list, "Derived, not authored" | `process.schema.json#/$defs/task_shape/oneOf/0/properties/requires_capabilities` | **Dropped.** The instantiated primitive points at its catalogue definition (brief l. 33); the requirement is one hop away and never copied. |
| Robot resource states what it offers | `resource.schema.json#/$defs/crs/properties/activity/properties/task_type`, which refers to `capability.schema.json#/$defs/capabilities` ("Interpreted as the capabilities this robot offers") | `RobotType.offers`, multivalued reference to `CapabilityType`, projecting to `OFFERS`. Moves from the CRS activity group to the process side, as brief l. 20 requires ("relocate attributes the process side already owns, such as capabilities, so nothing is declared twice"). Flat set first (brief l. 101). |
| Membership check | "enforced by validate.py, not this schema" (`capability.schema.json#/$defs/capabilities` description) | Tier 2, owned by the generator at load (brief l. 67): every `requires` target must resolve to a `CapabilityType`. |

The two-vocabulary matching (`requires` intersected with `offers` non-empty, per primitive) is the type-level allocation query the brief's third checklist item tests (l. 75). Nothing in the reference's `requires_capabilities` carries a qualifier (payload, reach), which is consistent with "flat first".

## 8. Findings for the brief's checklist

- The assumption "a closed set of parameter kinds covers every primitive in the reference" **holds**, but the reference exercises only two kinds (Position, ElementReference). The evidence for Quantity is the capability vocabulary's descriptions, not any action. Duration, Enumeration, and Resource reference are not forced; the last is excluded by design.
- The mapping surfaces one concrete instance of open question 4 (identifier-less inlined multivalued objects): parameter declarations, parameter bindings, and argument bindings all have this shape. The rule table needs a decision before the catalogue can be written.
- The reference's compound cannot express parameter flow; HDDL's labelled subtasks with argument bindings are the missing construct, and `Subtask` must be a node for ordering to be expressible.
- Two description-level corrections to carry into the migrated catalogue: `Attach.target` is not derivable from the product element; `Detach.target` as a bare position omits orientation.
