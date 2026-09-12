# LinkML-Backed Product Process Graph Schema

*Idea brief, 2026-09-10. Output of an idea-refinement session; supersedes the reference schemas under `docs/reference-schemas/` as the statement of intent.*

## Problem Statement
How might we define a representation of robotic construction planning that humans can read and extend as a catalogue, that a loader can project onto the Product Process Graph without judgment calls, and that stands as a research contribution in its own right?

## Confirmed Intent
Confirmed 2026-09-10.

- **Outcome:** One LinkML model, four YAML files, that other teams can read and build against, that a Python component turns into a Neo4j Product Process Graph deterministically, and that is publishable as the representation.
- **User:** The author first, as the person writing the model and the graph. Then the other project teams who need a contract to code against without asking. Then the paper's reviewers.
- **Why now:** Other teams are blocked on the contract, and the paper is to be submitted by the end of 2026.
- **Success:** Another team validates their documents against the model without help; the conformance corpus proves the graph is deterministic; the paper is submitted with the model and its graph projection as the contribution.
- **Constraint:** Two, in order. The contract goes out before the generator exists, because that is what unblocks the other teams. Everything is publishable by December 2026, so the first increment cannot grow.
- **Out of scope:** See MVP Scope, Out.

## Recommended Direction
Author the domain model once, in LinkML YAML, and treat it as the single source of truth. Instance data, whether a hand-authored catalogue or components parsed from IFC, is validated directly against that model with `linkml.validator`. The Neo4j graph is a derived shape of the same model, produced by a Python LinkML-to-Neo4j component that owns all graph logic: it reads the schema to emit Neo4j constraints and reads validated data to write nodes and edges, on one shared rule table. The model itself stays neutral, with no graph vocabulary and no annotations, so SHACL, JSON Schema, and documentation can be generated from it for other consumers without contamination.

The component projects using LinkML's own metamodel and nothing else. Identified classes become node labels, `is_a` becomes stacked labels, classes marked `represents_relationship` become edges carrying their non-role slots as edge properties, reference slots become edges, primitive slots become properties, and identifier-less inlined objects are flattened to prefixed properties, keyed maps with the key as prefix. An identified object projects to a node and an edge whether it is written inline in the document or referenced by id: `inlined` shapes the document, never the graph. Node ids are authored by the data author and referenced, never minted by the component; edges carry no ids. Slot defaults declared with `ifabsent` are written by the component, because the validator and the generated JSON Schema ignore them; this is a metamodel rule, not a named-slot rule. One rule is keyed on a named slot rather than on the metamodel: a `RobotUnit` with `count` n yields n machine nodes with ids suffixed `_1` to `_n`, derived from the authored entry id and all linked to the same group nodes and capabilities. Recorded 2026-09-11 as the only such rule; a second one reopens the decision. The rule table is total over the constructs it accepts, and the component rejects any schema using a construct outside the table, with a reason. Two rejections are fixed now: a `represents_relationship` class that declares an identifier, and a multivalued class-ranged slot on such a class. That rejection is the guarantee: a schema it accepts projects deterministically, and data the validator accepts loads without judgment calls.

Wherever the reference schemas stored open-ended structure as data, the model instead uses a closed set of typed kinds, each a LinkML class. This applies to action parameters and, by the same reasoning, to preconditions.

The model is one schema split across four files joined by `imports`: `common.yaml` for shared types and kinds such as Position and Quantity, and for CapabilityType, since both the process side (`requires`) and the resource side (`offers`) point at it; `product.yaml` for BuildingComponent, Space, and Opening; `process.yaml` for PrimitiveTask, CompoundTask, Method, and the instantiated tasks; `resource.yaml` for RobotUnit and its four Construction Robot Schema group classes. Product and resource import only common. Process imports common, product, and resource: methods match component materials, primitives reference components, and the instantiated primitive carries `assigned_unit`, the one edge that records stage-two allocation, pointing at a machine node such as `sam100_2`. Nothing imports process. The assignment is stored once, on the task; "all tasks for this robot" is a query over the same edge, not a second slot. The split is for readability. Validator, generator, and documentation see a single model.

## Design Inspirations
The model borrows structure from three sources. "Inspired by" means adapted: for each, a borrowed/adapted/dropped table records the lineage under one house naming style.

- **Product side: IFC.** Borrow the occurrence/type split (`IfcWall` versus `IfcWallType`), which mirrors the catalogue/instance split across the whole model, the GlobalId as the join key for components that come from IFC, and the property-set idea for planning-relevant attributes. Do not copy geometry or the full element hierarchy: IFC remains owner of element detail; the graph holds the join key and what planning needs. IFC's own process classes are a cross-check, not a source. Method applicability matches the material string IFC already carries on the component; no taxonomy is built.
- **Process side: HDDL and HDDL 2.1.** Borrow the three concepts below and the subtask network with ordering. Method applicability is a constraint on the component parameter, as HDDL constrains method parameters, not a state-based method precondition, which the HDDL authors call "somewhat problematic" because it is usually search advice. In the model it is a list of accepted material strings. Capability requirement is an ordinary primitive-task precondition. From HDDL 2.1 (Pellier et al., 2023) borrow a duration on each primitive task and ordering over start and end events, which subsumes simple precedence and leaves room for overlap. Leave out its "at e φ" constraints. Producing runnable HDDL from the graph is outside the model, but the mapping should be a straight walk.
- **Resource side: the Construction Robot Schema** from "A Planning Schema of On-Site Construction Robot Operation." Borrow its physical, operational, safety, and activity attribute groups as four classes, `PhysicalProperty`, `OperationalRequirement`, `Safety`, `Activity`, each held by `RobotUnit`. Adapt units to the model's quantity kind, split type from unit, and relocate attributes the process side already owns, such as capabilities, so nothing is declared twice.

## Domain Structure: HDDL
The process side follows HDDL (Höller et al., AAAI 2020) and uses its words. Three catalogue concepts, no more.

| Class | HDDL | Carries | Example |
|---|---|---|---|
| `PrimitiveTask` | Primitive task, also "action" | Name, typed parameters, capability requirements as its precondition, duration. Effects deferred, see Preconditions as Relation Kinds. | `MoveTo`, `Attach`, `Detach` |
| `CompoundTask` | Compound task, also "abstract task" | Name and typed parameters only. No body, no state change. | `ConstructComponent(component)`, `Transport(component)` |
| `Method` | Decomposition method | The compound task it refines, the material strings it applies to, an ordered or partially ordered subtask network of primitive or compound tasks | `prefab` refines `ConstructComponent` for components whose material is in its list |

A ConstructionMethod is simply a `Method` whose task is `ConstructComponent`. Several methods may refine the same compound task; choosing among them is the planner's job. The reference `TransportComponent` splits into a `CompoundTask` `Transport` and one `Method` refining it into `MoveTo, Attach, MoveTo, Detach`; a second transport method can be added later without touching anything else.

On the instance side, each node is an instantiated primitive or an instantiated compound, pointing at its catalogue definition, with the compound also pointing at the method chosen to refine it. Siblings are ordered by `after` constraints over start and end events. There is no separate Task-as-plan-unit and no catalogue-side compound action.

The graph path this yields, and the picture the paper should open with: BuildingComponent, matched by material, `REFINED_BY` a Method, which `DECOMPOSES_INTO` PrimitiveTasks, each of which `REQUIRES` CapabilityTypes that a RobotUnit's Activity `OFFERS`. Product, process, and resource in one query.

## Preconditions as Relation Kinds
Preconditions and effects are not a formula language. They are a closed set of kinds, each projecting to a graph pattern a query can match. The graph gives a planner typed facts; the planner reasons.

| Kind | Pattern | Enables | Slice |
|---|---|---|---|
| Applies to product | Method lists accepted material strings; a BuildingComponent matches if its material is among them | Method selection, the Product-to-Process link | First |
| Requires capability | PrimitiveTask requires CapabilityType; the RobotUnit's Activity offers it | Type-level task allocation | First |
| Ordered after | Task after Task over start and end events, a DAG | Sequencing | First |
| Acts on component | PrimitiveTask targets BuildingComponent via the component-reference parameter | Product-process join | First, as a parameter kind |
| Component state | Task requires or produces a component state such as placed, fixed, inspected. This is where effects enter the model. | Real preconditions and effects on the product | Later |
| Resource availability | The machine node's `status` is `idle` during the task's duration | Scheduling | Later |
| Capacity | A Quantity parameter of the task compared against an attribute of the machine's `PhysicalProperty`, such as component weight against load capacity | Rejecting robots that cannot do the task, before stage two | Later |
| Contained in | BuildingComponent is contained in a Space | Locating work, resolving a Position to a Space | First in the contract; instances derived later |
| Connects | Opening connects two Spaces, carrying clear width and height | Reachability, door-fit checks, path finding | First in the contract; instances derived later |
| Derived from | A derived BuildingComponent points at the IFC-sourced BuildingComponent it was generated from | Product lineage, wall-to-bricks | First |

## Two-Stage Allocation and Execution
Allocation happens twice, at different granularity, with different data, and the model must serve both without confusing them.

**Planning allocates to an entry.** HDDL-level planning uses only the `requires` / `offers` pattern: this primitive needs lift and align, and every machine of entry SAM100 offers both, so any of them can do it. The planner sees one object per machine, `sam100_1` to `sam100_n`, generated from `count`, and the machines of one entry are interchangeable, so "one of the five" is what a plan says. There is no `RobotType`: the entry is the type. Amended 2026-09-11, see `robot-entry-as-type.md`.

**Orchestration allocates to a machine.** At execution time a separate step, using multi-robot task allocation algorithms rather than HDDL, refines the plan to a specific machine: "of the five SAM100s, `sam100_2` is most suitable," judged on the group attributes, current position, battery, and `status`. This is where the Construction Robot Schema's quantitative attributes earn their place. Every attribute lives in one of the four group classes, shared by the machines of one entry; `status` lives on the machine node and is written by orchestration; position and battery are runtime state outside the model.

**Execution is a behaviour tree.** The allocated, instantiated task network is mapped to BT.CPP XML: a compound becomes a control node, Sequence for totally ordered subtasks, Parallel where the ordering allows, and a primitive becomes an action leaf whose name and filled parameters the tree can dispatch to the assigned unit. The mapping is a downstream consumer, out of MVP scope, but it imposes three requirements on the model now: every primitive must be addressable as a BT leaf, ordering must be expressible as control-node nesting, and the instantiated primitive needs a place to record its assigned `RobotUnit`.

Neither stage-two allocation nor the BT mapping is native to HDDL. Both are their own algorithms and their own specs. They are in this brief because they fix what the resource model has to carry and where the entry/machine boundary falls.

## Product Side
The Product contract is part of the first slice. What comes later is only the tooling that fills it.

**BuildingComponent.** Every component carries two orthogonal distinctions as required slots:

- `permanence`: `permanent` or `temporary`. Reinforcement is permanent; formwork is temporary.
- `source`: `ifc`, parsed directly from the model, or `derived`, added by an external algorithm, with the producer named. Bricks are the standard example: usually absent from the IFC model, yet needed as components.

Because a derived component has no IFC GlobalId, the BuildingComponent's identifier is its own, not the GlobalId. `ifc_global_id` is an optional slot, required when `source` is `ifc`. `BuildingComponent` is subclassed by kind only, never by source or permanence; see Decisions Taken by Default. A derived component carries `derived_from`, an edge to the IFC-sourced component it was generated from, so the wall-to-bricks relationship is in the graph. Formwork is often both temporary and derived; the two slots are independent.

**Spatial topology.** The Product side carries a light topological graph: `Space` nodes, `Opening` nodes with clear width and height, `connects` edges from an Opening to the two Spaces it joins, and `contained_in` edges from a BuildingComponent to its Space. These classes and slots are in the contract from the first slice. Their instances are derived, not authored: Topologicpy computes them from the IFC geometry, and since Topologicpy reads IFC itself, one parse of the model can emit both the BuildingComponents and the topology as instance documents in one coordinate frame. That derivation is a later slice. IFC's spatial structure (`IfcSpace`, `IfcOpeningElement`, `IfcDoor`, spatial containment) is the source; the Building Topology Ontology is a cheap `exact_mappings` target later, nothing more.

The two questions the topology answers are queries, not model logic, and belong to stage two: "does this robot fit through that door" compares a machine's `PhysicalProperty` dimensions with an `Opening`'s clearance; "how to move from A to B" is a shortest path over Space adjacency.

`Position` must be a coordinate in the same site frame the IFC parse produces, so a position can be resolved to its Space at parse time.

## Error Tiers
The guarantee "follow the schema and you get a graph, don't and you get an error" holds only if each kind of error has one named owner. There are three, ordered by how much context is needed to detect them.

| Tier | Question | Context needed | Owner | Example |
|---|---|---|---|---|
| 1. Shape | Is this document well formed against the model? | The document and the schema | `linkml.validator` | `requires` is a string, not a list |
| 2. Key | Does every key point at something that exists, and does the value fit its declared kind? | All documents, parsed together | The generator, at parse time, before any write | A method refines `Weld`; no such compound task exists. A filled parameter is a position where the kind says component reference |
| 3. Domain rule | Is the assembled structure legal? | The whole graph | Post-load checks: Cypher queries that must return zero rows, in the same transaction so a violation rolls back | Ordering forms a cycle. A method has an empty network without declaring it |

Tier 2 is a parse check. `linkml.validator` checks that a key has the right shape, never that its target exists; bundling documents into one run does not change that (verified against the validator source, see `docs/research/linkml-neo4j-and-metamodel.md`). So the generator parses all documents, indexes every identifier, and flags a key with no target as an error and a definition nothing points at as a warning. It needs that index anyway to create edges. Tier 3 rules are not expressible in LinkML and are documented and tested as part of the artifact rather than folded into the schema and lost.

## Key Assumptions to Validate
- [ ] **LinkML's metamodel alone disambiguates the projection.** Test: write the rule table over `identifier`, `inlined`, `represents_relationship`, `relational_role`, `is_a`, `multivalued`, `range`, then walk every class through it. Any class needing a case outside the table is a finding.
- [x] **A closed set of parameter kinds covers every primitive in the reference `actions.json`.** Verified 2026-09-10, see `docs/research/parameter-kinds-mapping.md`: Position and ComponentReference cover all five parameters; Quantity is added because the capability descriptions already name tolerances, torques, and rates. Duration is a slot type on `PrimitiveTask`, not a parameter kind. Enumeration and resource reference are deferred.
- [ ] **Material-list applicability plus capability matching are enough for method selection and type-level allocation.** Test: migrate the reference catalogue, write both queries, and check each returns what you'd choose by hand. Where it doesn't, name the missing kind rather than adding logic to the query.
- [x] **The type/unit split in the resource model is clean.** Answered 2026-09-11, see `robot-entry-as-type.md`: there is no type. Every Construction Robot Schema attribute has one home in one of four group classes held by `RobotUnit`, and `status` is the only per-machine fact in the model.
- [ ] **The three inspirations share one house style without losing lineage.** Test: write the borrowed/adapted/dropped table for each before writing classes.
- [ ] **`linkml.validator` catches the shape tier without a hand-maintained JSON Schema.** Its default plugin generates one internally, which is fine. Test: validate the migrated catalogue directly.
- [ ] **Topologicpy can read the project's actual IFC files and derive Space adjacency and Opening clearances from them.** Test: run it on one real model and check the BuildingComponents, Spaces, Openings, and connections it produces against the drawings. Not needed for the first slice, but it decides whether one parser produces both BuildingComponents and topology, or two tools do, and whether the topology is derived or has to be authored.
- [ ] **Each error tier has exactly one owner that catches its tier.** Test: one deliberately broken document per tier, each failing where the table says and nowhere else.
- [x] **No existing LinkML-to-Neo4j backend already does this well.** Verified 2026-09-10, see `docs/research/linkml-neo4j-and-metamodel.md`: no official generator exists; linkml-store's adapter and KGX project from data-row conventions, not from the schema. Write our own on `SchemaView`; borrow KGX's batching and constraint pattern. `represents_relationship` and `relational_role` exist but are marked "testing" and no shipped generator consumes `relational_role`, so this would be its first consumer.

## MVP Scope
Sequenced by the constraint. **Step 1, the contract:** the four YAML files, the documentation LinkML generates from them, the JSON Schema for the viewer, and the migrated reference catalogue as example instance documents, shipped to the other teams. The examples double as the first conformance corpus in step 2. **Step 2, the proof:** the generator, the tier 2 and tier 3 checks, and the conformance corpus. Same scope; the contract lands before the code because the dependency needs it.

**In.** The LinkML model for the catalogue: `PrimitiveTask` with typed parameter kinds, a duration, and `requires` to `CapabilityType`; `CompoundTask`; `Method` with `applies_to` material strings and an ordered subtask network; `CapabilityType`; `RobotUnit` with `count`, `status`, and the four Construction Robot Schema group classes, `offers` on Activity. The borrowed/adapted/dropped table per inspiration. The Python component with its rule table, emitting constraints from the schema and writes from data, refusing unprojectable schemas with a reason, performing tier 2 checks before writing. Tier 3 checks as a documented query set. A conformance corpus: example documents paired with the exact graph each must produce, plus one broken document per tier; the migrated reference catalogue is the first corpus. The Product contract: `BuildingComponent` with its own identifier, `permanence`, `source`, optional `ifc_global_id`, `derived_from`, and `contained_in`; `Space`; `Opening` with clearances and `connects`. On the instance side, one component with its instantiated compound and primitives, to prove the full path BuildingComponent to Method to PrimitiveTask to CapabilityType to RobotUnit as a single query, plus a slot on the instantiated primitive for its assigned machine node, so stage two has somewhere to write. Generated JSON Schema as a secondary output for the viewer.

**Out.** Plan, Run, ExecutionRecord, the IFC parser, and the Topologicpy derivation of Spaces and Openings. The classes are in; the tools that populate them are not. HDDL export. Stage-two allocation algorithms. BT.CPP generation. SHACL generation and RDF loading. Formal ontology alignment. Component-state and resource-availability kinds, and with them effects. Any graph vocabulary in the LinkML files.

## Not Doing (and Why)
- **Hand-authored JSON Schema with a prose mapping.** It's what the reference schemas are, and the guarantee lives in the loader author's head.
- **Graph annotations in the LinkML model.** The metamodel already carries the needed distinctions; annotations would leak Neo4j into a model that also serves SHACL and documentation.
- **Guessing in the generator.** Unprojectable constructs are rejected with a reason. A permissive generator produces a graph nobody can explain. The `count` rule is deterministic and recorded, not a guess.
- **A Task class as plan unit, or a catalogue-side compound action.** HDDL's three concepts cover it. `TransportComponent` becomes a compound task plus a method.
- **State-based method preconditions.** HDDL's authors flag them as search advice. Applicability is a list of accepted material strings on the method.
- **A precondition language.** Preconditions are a closed set of relation kinds that project to patterns. Formulae belong to the planner.
- **Runtime state in the model.** Position, battery, and wear are read from the robot at run time and stay outside the model. `status` is the one exception, written by orchestration onto the machine node. Amended 2026-09-11.
- **Copying any inspiration wholesale.** Borrow structure, record the adaptation.
- **Ontology alignment up front.** `exact_mappings` can be added later at near-zero cost.
- **Subclassing `BuildingComponent` by source or permanence.** Provenance and lifetime are slots. Subclasses are for kinds, added on demand.
- **Full IFC-to-graph round trip in the first slice.** It multiplies entity count before the rule table is proven.

## Open Questions
None at the time of writing. New ones go here as the spec raises them.

## Decisions Taken by Default
Accepted as working defaults on 2026-09-10; revisit if they bite.
- `RobotUnit` and the assigned-unit slot are in the first slice so stage two has a target. The target is a machine node generated from `count`. Amended 2026-09-11.
- Ordering is over start and end events from the start, rather than a plain `after` DAG upgraded later.
- The product class is `BuildingComponent`, the project's term, not `Element`. Decided 2026-09-10.
- The generator emits Cypher plus parameter JSON; a thin `apply` command loads them through the driver. Unit tests compare generated Cypher against the conformance corpus with no database running; one integration test applies it and checks the graph. Decided 2026-09-10.
- One coordinate frame, the IFC project frame, for every Position in the model. No frame slot. Transforming a robot's own frame into it is orchestration's job, outside the model. Decided 2026-09-10.
- The rule table lives in `PROJECTION.md` and the tier 3 query set in `CHECKS.md`, both beside the generator; the BT mapping requirements are a section in the model documentation generated from class descriptions. The repo is the published artifact. Decided 2026-09-10.
- `offers` is a flat set of capability types. Type-level allocation is set containment. The known gap, an entry that offers `lift` but whose load capacity is below the component weight, is recorded as the Capacity relation kind, Later. Decided 2026-09-10.
- Parameter declarations, parameter bindings, and subtask argument bindings are maps keyed by parameter name, using LinkML's `key` slot on the small class. The generator flattens a keyed inlined map to properties prefixed by the key (`target_kind`, `target_x`), and a reference-valued entry becomes an edge carrying the key. Unkeyed multivalued inlined objects are refused. No child nodes. Subtask occurrences carry a real identifier and become nodes by the standard rule, because ordering constraints point at them. Decided 2026-09-10.
- Method applicability is `applies_to`, a list of exact material strings as they appear in IFC, matched by membership. A list because real models spell one material several ways. No material taxonomy, no subtype semantics, no kind constraint; if two kinds share a material and need different methods, add a slot then. Decided 2026-09-10.
- `permanence` and `source` are required on every `BuildingComponent`, with no default. An unknown lifetime or provenance is a hole in the plan, and a default would silently mislabel temporary works. Confirmed 2026-09-10.
- Stage-two allocation is one edge, `assigned_unit` on the instantiated primitive, pointing at a machine node such as `sam100_2`. No mirror slot on `RobotUnit`; the reverse direction is a query. Decided 2026-09-10, target amended 2026-09-11.
- `RobotType` is retired. The resource module is five classes: `RobotUnit` with `id`, `count`, and `status`, holding one object each of `PhysicalProperty`, `OperationalRequirement`, `Safety`, and `Activity`, each with its own authored `id` so it projects to a node. `offers` sits on `Activity`, where the paper's Task Type is, so `Activity` is the one required group. `status` is an enum, `idle`, `deployed`, `charging`, `out_of_service`, default `idle`. Decided 2026-09-11, see `robot-entry-as-type.md`.
- The rule table was amended 2026-09-12 from `docs/research/linkml-metamodel-conformance-and-inheritance.md`: identified objects project as nodes whether inlined or referenced; node ids are authored and edges have none; `ifabsent` defaults are the component's job; an edge class with an identifier or with a multivalued class-ranged slot is rejected. The same note fixes the inheritance policy: no `abstract`, `mixins`, `union_of`, or `designates_type` in any module; `is_a` only in product, for kinds that need extra slots.
- `BuildingComponent` is subclassed by kind only, such as Wall or Brick, and only when a kind needs slots the others lack. Never by `source` or `permanence`: those are slots, because provenance and lifetime are facts about a component, not kinds of component, and a source-based class would change when the IFC model improves. GlobalId required for IFC-sourced components is a tier 2 check. Decided 2026-09-10.

## References
- Höller, Behnke, Bercher, Biundo, Fiorino, Pellier, Alford. HDDL: An Extension to PDDL for Expressing Hierarchical Planning Problems. AAAI 2020. DOI 10.1609/aaai.v34i06.6542.
- Pellier, Albore, Fiorino, Bailon-Ruiz. HDDL 2.1: Towards Defining a Formalism and a Semantics for Temporal HTN Planning. arXiv:2306.07353, 2023.
- Li et al. A Planning Schema of On-Site Construction Robot Operation. 2026. Source of the Construction Robot Schema.
