# Spec: mvp

*Module `mvp` of `CAPABILITY-MAP.md`; Phase 1 decided 2026-09-23 from `docs/prompt.md`, spec for review. A demonstration for the progress report, not the paper's generator: the plainest pipeline that runs the chain IFC to product graph to generated process graph to plan to compared plans, on the model and catalogue this repository already holds. Depends on all four schema modules and changes none of them.*

## Objective

Show, live, that a process graph for a building is derived from its IFC model through the validated product data and the validated catalogue, and that plans and their comparison follow from it. The audience sees the chain end to end and can trace any process node back to the component, material, category and method that produced it, and from any process node to the element in the 3D model. The transformation from validated product and catalogue data into the process graph is the place where the model's adequacy is tested first.

**Success in one sentence.** The prompt's own: an IFC is uploaded, parsed with topologicpy, validated with the catalogue and mapped into Neo4j, materials are corrected, a process graph is generated from that and inspected, robots are configured, plans are generated and compared as Gantt charts and metrics, and the audience sees that nothing in the process graph was authored by hand.

**Not in this spec.** The projection rule document `PROJECTION.md`, schema rejection with reasons, the conformance corpus, `CHECKS.md`: the paper's generator, later. Stage-two allocation, behaviour trees, geometry beyond centroids and the browser's own rendering of the IFC, distance-dependent durations, energy metrics, authentication, deployment. Any change to `schema/`: a modelling limitation found here is written to `mvp/FINDINGS.md` and decided in its own cycle.

## Tech Stack

**Backend.** Python 3.12 under uv, a second uv project in `mvp/` so the schema project's dependencies and CI do not change. `linkml` for tier 1, `linkml_runtime.SchemaView` for the projection, `pyyaml`. `topologicpy` with `topologic_core` for the IFC parse. `neo4j` driver against a Neo4j 5 DBMS from Neo4j Desktop. `unified-planning` with `up-aries` for HTN planning. `fastapi` and `uvicorn`, which also serve the built frontend.

**Frontend.** React with Vite and Tailwind, built once into `mvp/ui/dist`. Components from two shadcn registries: Kokonut UI for the chrome, Bklit UI for the charts on the Compare page; both bring Motion, which is the one animation library. React Flow with ELK for the graph pane. xeokit and web-ifc loaded from a CDN for the 3D pane: the IFC is rendered in the browser and picked by GlobalId, so no server-side geometry exists. A Gantt component of our own on Visx, because Bklit has no timeline chart. Style after the INO reference (`styles.refero.design`, 57388b47): near-monochrome light theme, white and near-black with two greys, one typeface at one weight, hierarchy by uppercase and letter-spacing, 8px radii, pill buttons, generous whitespace; the graphs carry the colour.

The example corpus under `examples/` is the catalogue, the robots, the stocks and the vocabularies; the Duplex under `examples/ifc_models/` is the building.

## Commands

```
cd mvp && uv sync && (cd ui && npm install && npm run build)
uv run --project mvp pytest mvp/tests
uv run --project mvp python -m mvp.parse examples/ifc_models/20260907_1713.ifc     # parse and cache; pre-warm before the talk
uv run --project mvp uvicorn mvp.app:app --reload                                   # http://localhost:8000
```

Neo4j: a Neo4j Desktop DBMS started by hand, reached at `bolt://localhost:7687`; credentials in `mvp/.env`, never committed. `npm run dev` in `mvp/ui` for frontend work only; the demo runs on the built files.

## Project Structure

```
mvp/pyproject.toml         its own dependencies; no change to the root pyproject
mvp/mvp/parse.py           topologicpy entity parse; components, storeys, spaces, connectors, materials written as product.yaml records and nothing of topologicpy's own dictionaries kept; materials read from the IfcRelAssociatesMaterial entities, not from the dictionary's material string, which is unusable on the Duplex; centroids from topologies of the selected storeys only; cache under mvp/cache/<sha256 of file>/
mvp/mvp/validate.py        tier 1: split by record_type and validate with linkml against schema/*.yaml; tier 2: one id index over all documents, every reference resolves, position and machine names by the two minting rules, "" on bound_to only under a robot parameter of a process graph document
mvp/mvp/project.py         the brief's rule table over SchemaView: label per identified class, stacked labels for is_a, edge per reference slot named by the slot, prefixed properties for identifier-less inlined objects, count expansion, binding edges by declared kind, location bindings to the component carrying the slot; batched UNWIND/MERGE with one uniqueness constraint per label
mvp/mvp/generate.py        product graph plus catalogue to process graph: one CompoundTaskInstance per component whose Material's category a ConstructComponent method applies_to, decomposed through the catalogue, positions bound from the component, r empty; one TaskNetwork per storey
mvp/mvp/hddl.py            catalogue to domain, product and inventory and network to problem, per storey
mvp/mvp/plan.py            solve with Aries through unified-planning; write r onto a copy of the process graph; run record
mvp/mvp/metrics.py         makespan, busy and idle time per machine, utilisation, time-weighted and peak parallelism, primitives per machine, stock occupancy
mvp/mvp/forms.py           one form description per class from SchemaView: per slot its name, description, required, minimum cardinality, kind, range, enum values, and the resolving document for a reference; what every editor renders from
mvp/mvp/app.py             FastAPI routes for the four pages, including validate-on-change for the catalogue editor; serves mvp/ui/dist
mvp/ui/                    Vite app: src/pages/{Integrated,Process,Resource,Compare}.jsx, src/components/ (shadcn registry components, Gantt, GraphPane, ModelPane, Inspector, MethodEditor)
mvp/models/<sha256>/       the parsed product documents of one IFC, edited from the Integrated Page, and its process_graph.yaml; the source the pipeline validates and projects
mvp/catalogue/             catalogue.yaml, capability_types.yaml, material_categories.yaml, seeded from examples/, edited on the Process page
mvp/inventory/             robot_units.yaml and stocks.yaml, seeded from examples/resource/, edited on the Resource page
mvp/runs/<run id>/         plan.yaml, the process graph with r bound, and run.json: the inventory as it was, start and duration per primitive, take and release per stock unit, metrics
mvp/FINDINGS.md            where information was lost, duplicated, inferred ad hoc, or represented awkwardly at a boundary, one line each, sorted into the prompt's three cases; the product-and-catalogue to process-graph transition is the first boundary to look at
mvp/tests/                 pytest, no Neo4j needed except one marked integration test
```

## The Demonstration

**Building.** The Duplex, storeys `T/FDN` and `Level 1` by default, selectable. The concrete foundation walls and slabs on grade go through `m_insitu`, the brick-on-block and CMU walls through `m_prefab`. Components whose Material has no category, or a category no method names, are shown as warnings and produce no process; that is the honest coverage of the catalogue and is shown, not hidden.

**Pages, four.** Product, process and resource are split as the schema splits them; the Integrated Page is where the chain runs.

1. **Integrated Page.** Three buttons in sequence, each unlocking the next, with status and errors by tier beside them.
   - *Upload IFC*: parse or load from cache, write the product documents, validate, project. Site setup on the same page: one depot xyz written into every `supply_location` that still carries the unresolved sentinel.
   - *Generate Processes and Resources*: validate the catalogue and vocabularies under `mvp/catalogue/` and the inventory; project them; then generate the building's process graph from the projected product graph and catalogue, validate it, project it. The graph pane gains its process layer.
   - *Plan*: export the HDDL domain and problem per storey, solve with Aries, bind `r`, validate and project the plan, save the run. Nothing new is drawn here beyond the run's status; the result is on the Compare page.

   Three panes. The *3D pane* renders the uploaded IFC in the browser, picking by GlobalId. The *graph pane* shows the product graph, filtered by storey, and after generation the process layer above it: networks, compound instances, primitive instances, their catalogue tasks. The *inspector* shows the selected record's slots. For a component it offers two controls: its Material, a dropdown over the existing Material records plus "new", which asks for the material id and category and writes a new Material record; and that Material's category, a dropdown over `material_categories.yaml`. Shift-click selects several elements and sets `made_of` on all of them in one write. Every change rewrites the model's product documents, revalidates and reprojects; nothing is kept in browser state. A method is never assigned to an element; it follows from the material through the catalogue.

   *Warnings*: the list of components no method applies to, with the reason: no material, material without category, category no method names. Clicking one selects the element in both panes.

   *Bidirectional selection*: an element clicked in 3D highlights its component node and the process subtree bound to it; a process node clicked highlights its component in 3D and the path that justifies it in the graph pane: component, material, category, method, subtask edge with position, primitive task, required capabilities, offering robot entries. Every element of that path is a node or edge the projection wrote; both directions are a lookup on the GlobalId every instance binds as `c`.

2. **Process page.** The catalogue editor, over `mvp/catalogue/`: primitive tasks, compound tasks and methods, HDDL's three kinds and no other. Three create buttons, one per kind, and a list of what exists. Every reference is offered as a dropdown over a validated document, and every dropdown ends with "new": capabilities from `capability_types.yaml` for `requires`, categories from `material_categories.yaml` for `applies_to`, stocks from the inventory for `uses`, tasks for `compound_task` and for subtask lines, kinds from the enum. A new capability or category is created in place with its id and description and written to the vocabulary copy; a new stock is created on the Resource page. A new construction method is therefore made entirely in the browser: its primitives with their capabilities and durations, its compound task, its method.

   A method has three renderings of the one record, two of them editors, kept in sync:
   - *List*: the form and the subtask list. Picking a task for a line lays out one argument slot per parameter that task declares, labelled with name and kind; each slot takes a method variable of that kind, or a new name, which is then added to the method's parameters with that kind. Ordering is drawn as ends-before arrows between rows, or a total order with one click.
   - *Graph*: a node editor on React Flow. The method's compound task sits at the top; each subtask line is a node carrying its position badge, its task and its argument slots; an ordering pair is an edge dragged from one node to another; a node is added by dropping a task from the palette, existing or new, and removed with its edges. The graph and the list write the same record, and the HDDL rule that a method declares every variable its subtasks use is enforced by construction in both: a variable exists because a slot named it.
   - *HDDL*: the `:method` block the exporter will emit, read-only, produced by `hddl.py`, so what is read is what Aries gets.

   On every change the record is validated at tier 1 against `schema/process.yaml` and the tier 2 rows of `SPEC-process.md` run over the catalogue: arity, kinds, name uniqueness, no cycle in the ordering, every reference resolving. Errors sit beside the field or on the node. Beside each method stands the count of components in the loaded model whose Material's category it applies to, and beside each category whether any method covers it, both read from the projected graph. Effects, preconditions beyond `requires`, and formula fields do not exist, because the schema has none.
3. **Resource page.** The inventory editor, over `mvp/inventory/`: robot entries and stocks, with create buttons for both. A robot's form shows what `schema/resource.yaml` requires, `id`, `count`, and the Activity group with its `id` and `offers`, and folds the three other CRS groups and the rest of Activity under "Detailed properties"; a stock's form shows `id`, `count`, `permanence`. A group's `id` is prefilled as the robot's id with the group suffix, the convention of the examples. `offers` is a dropdown over the capability vocabulary ending in "new". Saving rewrites `mvp/inventory/` and reprojects. A planning strategy in this MVP is a resource configuration, nothing else.
4. **Compare page.** The planner's output. Select runs; one Gantt per run, lanes per machine and per stock unit, aligned on one time axis; Bklit charts for the metrics across runs. Planner outputs exposed: solve status, and per primitive instance its start, duration and robot binding, plus each stock unit's take and release times. Nothing else of the planner is shown.

**Forms from the schema, one rule for both editors.** Every form on the Process and Resource pages is rendered from the form description `forms.py` emits for its class, never written by hand: required slots on top and always visible, everything else collapsed under "Detailed properties"; inlined objects, a `Quantity`, a `Position`, a CRS group, as sub-forms by the same rule; enums as dropdowns; references as dropdowns over the resolving document ending in "new"; a required list with a minimum of one, `requires`, `subtasks`, needs an entry, a required list the spec allows empty, `ordering`, `parameters`, may be empty. A record cannot be finalised until it passes tier 1 against its module's schema and the tier 2 rows over the documents it references: the save button is disabled and the errors stand beside the fields, or on the graph nodes, until they are gone. Nothing is written before that, so an unfinished robot or method never reaches the inventory or the catalogue. A slot added to a schema appears in its form without frontend work.

**Process graph generation, the rule.** For each `BuildingComponent` of the selected storeys, read its `Material` and that Material's `category`. Find every `Method` whose `compound_task` is `ConstructComponent` and whose `applies_to` equals the category, or is absent. One matching method: write a `CompoundTaskInstance` with `decomposed_by` set to it and instantiate its subtask lines recursively, compound lines through their own methods the same way, `c` bound from the parent, `from` to `<c>_supply`, `to` and `at` to `<c>_target`, `r` to `""`. Several matching methods: `decomposed_by: ""`, `subtasks: []`, the planner chooses. None: no instance, the component is a warning. One `TaskNetwork` per storey, `ordering: []`. Everything read comes from the projected graph; no material, method or task name appears in the code. The result is the middle of the three states `SPEC-process.md` decision 22 names: decomposed, positions bound, robots empty.

**Planning representation.** Domain from the catalogue: types `component`, `location`, `robot`, one per `Stock`; constants for the material categories; `applies_to` as a method precondition over a `material` fact, the form of `docs/research/pddl-for-process.md` B.1; each primitive a durative action with `duration` from the catalogue, its `requires` as `over all` conditions on `offers` facts of the robot, and a `free` lock on the robot taken at start and returned at end, the form of `docs/ideas/robot-entry-as-type.md`; `uses` as take and release steps around the method's span, the form of Appendix C.3. Problem per storey: objects are the components, the machines from `count`, the stock units from `count`, and the position names; init has each component's material category, each machine's capabilities and `free`, each stock unit `free`, each component at its supply position or its current one when set; `:htn` is the storey's `TaskNetwork`. Storeys are solved in elevation order and concatenated. The plan's robot bindings are written onto a copy of the process graph, which is validated with the tier 3 check that no `r` is empty, and projected.

**Experiments, each an inventory state.**

| Run | Configuration | Shows |
|---|---|---|
| E0 | `scout_v1` only | unsolvable: `requires` against `offers` |
| E1 | 2 `mason_m1`, 1 `concreter_k1`, 8 `formwork_panels`, 10 `rebar` | baseline, masonry in parallel |
| E2 | 1 `mason_m1`, rest as E1 | `count` drives parallelism |
| E3 | 1 `formwork_panels`, rest as E1 | `uses` serialises the concrete work |

**Metrics.** From the run record alone: makespan; per machine busy time, idle time, utilisation as busy over makespan; time-weighted mean and peak number of concurrent primitives; primitives per machine; stock units in use over time. Energy is displayed as not representable: the resource module carries no power draw.

**Reused.** The record-type split of `tests/test_examples.py` for tier 1; the resolution logic of `tests/test_references.py`, with its machine and position minting rules, for tier 2; the lineage rules of `examples/ifc_models/extract_product_examples.py` for the product records, re-read from topologicpy's entities instead of ifcopenshell; the method exporter and solver call of `docs/research/pddl-for-process.md` Appendix B and the stock take-and-release shape of Appendix C; the per-machine `free` lock of `docs/ideas/robot-entry-as-type.md`; the ELK layout code of the sibling `rcpc-schema-viewer`; the browser-side xeokit and web-ifc loading and GlobalId picking of the author's prototype in `FOR5672/frontend`, as a mechanism, not its structure or APIs; the 3D-to-graph selection idea of the sibling `IFCGraphViewer`. Not reused: `IFC2Graph`, which writes every STEP entity as a node for versioning, the round trip the brief lists under Not Doing; `FOR5672/planning-service`, by the author's instruction.

**Simplified, by decision.** One duration per primitive from the catalogue, whatever the component's size. Precedence between components is storey order and nothing else, with storeys solved in sequence. Robots have no start position. One depot xyz is written into every unresolved `supply_location`. Geometry is centroids only. Components whose Material has no category, or has one no method names, produce no process.

**Exercised.** Common: `CapabilityType` and `MaterialCategory` as documents a user adds words to. Product: `BuildingComponent` with `ifc_type`, `made_of`, the three positions and `contained_in`; `Material`; `Storey`; `Space` and `Connector` only as product graph nodes. Process: `Method` with `applies_to`, `parameters`, `subtasks`, `ordering`, `uses`; `PrimitiveTask` with `parameters`, `requires`, `duration`; `CompoundTask`; `TaskNetwork`; both instance classes with `bindings` and `decomposed_by`, in the three states of decision 22. Resource: `RobotUnit` with `count` and `Activity.offers`, the other CRS groups as editable records only; `Stock` with `count` and `permanence`. Not exercised: `Connector` clearances, `located_in`, `connects`, `status`, `current_location`, `derived_from`, `part_of`, `supply_location` beyond the depot value.

## Code Style

Backend: plain functions over dicts loaded from YAML, the style of `scripts/build.py` and `tests/test_references.py`. No classes for data, no framework beyond FastAPI. The generation loop is the reference shape:

```python
def construct_instances(components, materials, methods):
    """One compound instance per component a ConstructComponent method applies to."""
    for c in components:
        category = materials.get(c["made_of"], {}).get("category", "")
        fitting = [m for m in methods
                   if m["compound_task"] == "ConstructComponent"
                   and m.get("applies_to", category) == category]
        if len(fitting) == 1:
            yield instance(c, fitting[0])
```

Every id the pipeline mints follows a rule already in the specs: machine `<entry>_<n>`, position `<id>_target|_supply|_current`, instance ids as the example plan writes them. Cypher is generated, never hand-written per class.

Frontend: function components, one file per page and per pane, registry components copied in as the shadcn CLI leaves them, Tailwind tokens for the INO palette and type scale in one place, selection state in one store keyed by GlobalId. The backend hands the graph pane `{nodes, edges}` with the node's label and slots; the browser lays out and draws, nothing more.

## Testing Strategy

Backend pytest in `mvp/tests/`, run on its own, no database except one marked test: `validate` on the example corpus passes and fails on one planted dangling reference per document kind, and on `r: ""` in a plan but not in a process graph; `project` turns the example corpus into rows whose labels, edge names and counts are asserted, and never emits a label or edge name that is not a class or slot of the schema; `generate` on the example product documents yields one construct per masonry or concrete component and none for the rest, with `decomposed_by` and the bound positions asserted and every `r` empty; `hddl` reproduces the two-wall sequencing of Appendix C on one formwork set and the parallel plan on two; `metrics` on a hand-written run record; `forms` for every editable class lists exactly the slots `SchemaView` induces, with `required` matching the schema. The integration test applies the projection to the local Neo4j and reads node counts back. Frontend: `npm run build` passing is the check; no browser tests in this MVP. No test touches `tests/` of the schema project.

## Boundaries

**Always.** Validate at tier 1 and tier 2 before any write to Neo4j. Read methods, applicability, capabilities and durations from the projected catalogue, never from code. Every edit in the browser writes a document, revalidates and reprojects; the graph shown is always the projected one. Record every boundary finding in `mvp/FINDINGS.md` under the prompt's three cases. Keep Neo4j the only graph store. Rebuild nothing under `dist/` or `docs/model/`. Conventional Commits.

**Ask first.** Any change under `schema/`, `examples/`, `tests/`, `scripts/` or `.github/`. A dependency beyond the Tech Stack list. A fifth page or a pane beyond the three. A metric that needs an assumption not in the resource model. A second building. A field on any form that is not a slot of the class it edits.

**Never.** A hardcoded material-to-method or component-type-to-method rule, or a method assigned to an element. A second graph representation kept beside Neo4j. Server-side geometry conversion. Editing a generated process instance by hand; the process graph is regenerated, never patched. Writing catalogue or vocabulary edits back to `examples/`. Committing `mvp/.env`, `mvp/cache/`, `mvp/models/`, `mvp/runs/`, `mvp/catalogue/`, `mvp/ui/node_modules/`, `mvp/ui/dist/`, or the IFC. Modifying the example corpus to make a plan come out better.

## Order of Work

Pipeline before chrome, so the novelty is safe if the frontend runs late: parse with cache, validate, project, catalogue load, and the Aries scaling test on the `Level 1` network first; then generation and the HDDL export and solve as backend routes with tests; then the Integrated Page with the three buttons, the graph pane and the inspector; then the 3D pane and bidirectional selection; then Compare with the Gantt and Bklit charts; then the Resource page; then the Process page, its list editor before its graph editor; then the INO styling pass. The catalogue editor is the largest piece of the chrome and the last before styling, so that the chain demonstrates without it if it runs late.

## Success Criteria

1. From a fresh clone, `uv sync` and `npm run build` in `mvp/`, a running Neo4j Desktop DBMS, and the commands above, the four pages work on the Duplex with the parse served from cache.
2. Uploading the Duplex yields product documents that validate against `schema/product.yaml` by record type and pass tier 2; a planted error in each tier is shown at its tier and stops the write.
3. Generate Processes and Resources validates and projects the catalogue, the vocabularies and the inventory, then yields a process graph for `T/FDN` and `Level 1` with one construct per component whose Material's category `m_prefab` or `m_insitu` names, decomposed to the leaves, `r` empty, positions bound; every other component is a warning with its reason. Changing one wall's Material or a Material's category in the inspector and regenerating changes the graph accordingly, with no code change.
4. Clicking a wall in the 3D pane highlights its component node and its process subtree; clicking any primitive instance highlights its element in 3D and the full path to the component, its Material, the category, the method with the subtask position, the primitive task, its capabilities and the offering entries.
5. E1 to E3, each an inventory state set on the Resource page, solve; E0 reports unsolvable. E2's makespan exceeds E1's and E3's concrete tasks do not overlap, both visible on the Compare page. Changing an entry's `offers` changes which primitives it may perform, visible in the next run. Solve time per storey is measured on the first day and recorded here.
6. `uv run --project mvp pytest mvp/tests` passes and `npm run build` succeeds; the root `uv run pytest` is unchanged at 79.
7. `mvp/FINDINGS.md` lists every boundary finding met, each sorted into one of the prompt's three cases, with the location decision of 2026-09-23 and the three states of decision 22 as its first entries.
8. Every form on the Process and Resource pages is rendered from `forms.py`; its required slots match the class's `required` slots in the schema, checked by a test over every editable class; saving is disabled until tier 1 and tier 2 pass, shown with a robot missing `offers` and a method with a subtask of the wrong arity. A robot entered with only its required fields validates, projects and takes part in the next plan.
9. On the Process page a method for a category no method covers today, `timber`, is created in the browser, in the graph editor and in the list editor alike, with a new primitive task and a new capability; the catalogue copy validates; the next Generate yields instances for the timber components with no code change, and the HDDL rendering of the new method is what the planner receives.

## Open Questions

None at the time of writing.
