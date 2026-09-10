# LinkML-to-Neo4j backends and metamodel semantics

*Research note, 2026-09-10. Answers two questions raised by `docs/ideas/linkml-product-process-graph-schema.md` (sections "Recommended Direction", "Error Tiers", "Key Assumptions to Validate"). Primary sources only: linkml.io docs and the linkml, linkml-model, linkml-store, kgx GitHub repositories, cloned at the commits listed under "Sources consulted". Line numbers refer to those commits.*

## Verdicts

**Q1. Does a LinkML-to-Neo4j / labeled-property-graph generator exist?** No official one. The LinkML generator list has no Neo4j, Cypher, or property-graph target, and the LinkML FAQ states outright "we don't yet have any bindings for Neo4J or other graph databases". Two adjacent tools exist: the **linkml-store Neo4j adapter** (generic store adapter; labels and edges come from *data-row conventions* — a `category` attribute and `subject`/`predicate`/`object` attributes — not from the schema's classes, `is_a`, `represents_relationship`, or `relational_role`) and **KGX** (Biolink-only; fixed node/edge record format; writes labels from a `category` list and relationships from a `predicate` string). Neither reads an arbitrary LinkML schema to derive labels, stacked labels, edge classes, or flattened inlined objects, and neither emits schema-derived constraints. The only generator that consumes `represents_relationship` at all is the TypeDB generator. **Verdict: write our own**, building on `linkml_runtime.SchemaView` for schema introspection and borrowing two proven patterns: linkml-store's `EdgeProjection` role triple (the runtime analogue of `relational_role`) and KGX's `UNWIND`/`MERGE` batch Cypher with a per-label `id` uniqueness constraint.

**Q2. Do the metamodel features exist with the assumed semantics, and does `linkml.validator` check referential integrity?** All features exist. Caveats: `represents_relationship` and `relational_role` carry `status: testing`; `relational_role` is used by *no* generator or runtime code (grep of the whole monorepo); `relational_role_enum` has five values (SUBJECT, OBJECT, PREDICATE, NODE, OTHER_ROLE), not three; the metaslot for type designation is `designates_type` (alias "type designator"), there is no `type_designator` metaslot; `union_of` is documented as "only applies in the OWL generation". **`linkml.validator` does not check referential integrity — not within one document and not across documents.** The `Validator` iterates instances one at a time through plugins; the default `JsonschemaValidationPlugin` validates each instance against a JSON Schema generated on the fly, in which a non-inlined class-range slot is typed as its target's identifier type (a string), so a dangling reference is indistinguishable from a valid one. No plugin in `linkml.validator.plugins` resolves references. This **corrects the brief**: the clause "unless the whole catalogue is bundled into one validation run" in the Error Tiers section is wrong; bundling does not help. Tier 2 must live entirely in the generator, as the brief already places it. Separately, linkml-store does implement an opt-in cross-collection `_validate_referential_integrity`, which confirms the gap in core and is a useful reference implementation.

---

## Q1 evidence

### 1.1 The official generator list has no graph-database target

The generators index at https://linkml.io/linkml/generators/index.html lists 35 generators: JSON Schema, ProtoBuf, GraphQL, OpenAPI, JSON-LD Contexts, JSON-LD, RDF, SPARQL, ShEx, SHACL, OWL, YARRRML, Documentation, ER Diagrams, PlantUML, Project Generator, Python, Pydantic, Java, Go, Typescript, Rust, SQL DDL, SQL Alchemy, SQL Validation, BigQuery DDL, TypeDB/TypeQL, LinkML, Prefix, SSSOM, TerminusDB, Excel, CSV, Yaml, Pandera. None mentions Neo4j, Cypher, or property graphs. (Confirmed by fetch of that page.)

The source tree `packages/linkml/src/linkml/generators/` at the current head matches this list (files `bigquerygen.py` ... `yarrrmlgen.py`, plus `dbmlgen.py`, `dotgen.py`, `golrgen.py`, `mermaidclassdiagramgen.py`, `summarygen.py`, `markdowndatadictgen.py`). A recursive grep for `neo4j|cypher` over `packages/linkml/src/linkml` and over `packages/linkml_runtime/src/linkml_runtime` returns nothing. (Confirmed at commit c10d16a3, https://github.com/linkml/linkml/tree/main/packages/linkml/src/linkml/generators.)

The FAQ is explicit. https://linkml.io/linkml/faq/tools.html, section "Can I use LinkML in conjunction with Neo4J or graph databases?" (source `docs/faq/tools.md` lines 286-294): "You definitely can, although we don't yet have any bindings for Neo4J or other graph databases. ... If you are using PGs, we recommend following the design patterns in" the property-graph how-to.

### 1.2 The official how-to: modelling a property graph in LinkML (no tooling)

https://linkml.io/linkml/howtos/model-property-graphs.html (source `docs/howtos/model-property-graphs.md`). It is a modelling guide, not a generator. Two projections are described and each is given as a table:

*Simple projection* (edge = slot): Node = "instance of a Class"; Edge = "Attribute-Value Assignment"; Predicate (Edge Label) = "Attribute"; Node Property = "Attribute-Value Assignment"; Edge Property = "*not represented*".

*Standard PG pattern* (Node and Edge classes): Node = "instance of a (Node) Class"; Edge = "instance of an (Edge) Class"; Predicate (Edge Label) = "(Edge) Class"; Node Property = "Attribute-Value Assignment on Node instance"; Edge Property = "Attribute-Value Assignment on Edge instance".

The how-to's `Edge` class uses `class_uri: rdf:Statement` and slots `subject`/`predicate`/`object` with `slot_uri: rdf:subject|predicate|object` and `designates_type: true` on `predicate`. It does **not** use `represents_relationship` or `relational_role`. It closes: "We are currently exploring options for allow features such as auto-asserting PG style models when mapping to RDF-star", and links "Property Graphs with LinkML store" as the only tooling.

Relevance: this is the pattern the brief's rule table generalises (edge classes carrying non-role slots as edge properties). The how-to confirms the pattern is sanctioned but gives no mechanism.

### 1.3 Candidate A: linkml-store Neo4j adapter

**What it is.** linkml-store (https://github.com/linkml/linkml-store, latest release v0.3.2, 2026-04-28; head e4023ed3) is "an abstraction layer over multiple different backends (including DuckDB, MongoDB, Neo4j, and local filesystems), allowing for common query, index, and storage operations" (README lines 3-6). The README warns "LinkML-Store is still undergoing changes and refactoring, APIs and command line options are subject to change!". FAQ (`docs/faq.rst` 191-196): "Yes, linkml-store supports Neo4J as a backend."

**Source files.** `src/linkml_store/api/stores/neo4j/neo4j_collection.py`, `neo4j_database.py`, `src/linkml_store/graphs/graph_map.py`, `src/linkml_store/utils/neo4j_utils.py`. Optional dependency group `neo4j = ["neo4j", "py2neo", "networkx"]` (`pyproject.toml` line 46).

**Projection rules (from source).**

- A collection is either a node collection or an edge collection, decided by `metadata.graph_projection` being a `NodeProjection` or an `EdgeProjection` (`neo4j_collection.py` 41-55, 90-102). `graph_map.py` 6-24 defines the only knobs: `identifier_attribute="id"`, `category_labels_attribute="category"`, `subject_attribute="subject"`, `predicate_attribute="predicate"`, `object_attribute="object"`.
- **Node labels come from the data row, not the schema.** `_node_pattern()` reads `obj.get(category_labels_attribute or "category", [])` and joins the values with `:` (`neo4j_collection.py` 77-84). Node insert is `CREATE ({node_pattern} {id: $id, <all other keys>})` (125-132). If a row lacks `category`, the node is created with no label. The schema's class name and `is_a` chain are not consulted.
- **Edges are data rows in an edge collection.** Insert requires `predicate`, `subject`, `object` keys (136-141), then `MATCH (s {id: $subject}), (o {id: $object}) CREATE (s)-[r:{pred} {<remaining keys>}]->(o)` (160-163). The relationship type is the *value* of the `predicate` attribute, not the class name. Remaining keys become edge properties.
- **Dangling endpoints.** Before creating an edge it runs `MATCH (n {id: $id}) RETURN count(n)` per endpoint; if 0, with `DeletePolicy.STUB` it creates a bare `(n {id})` node, otherwise it raises `ValueError("Node with identifier ... not found in the database.")` (143-156). Default policy is `CASCADE` (line 27), which in the insert path falls into the raise branch. A code comment reads "TODO: decide on how this should be handled in validation if some fields are required".
- One Cypher statement per object, `session.run(query, **obj)` (118-121); no batching, no `MERGE`, no constraint creation anywhere in the adapter.
- `init_collections()` uses `CALL db.labels()` and "We'll use node labels as a proxy for collections" (`neo4j_database.py` 85-98).
- Queries return `labels[0]` as the `category` of a node (`neo4j_collection.py` 181-187), so multi-label nodes lose information on read.

**Official how-to** (https://linkml.io/linkml-store/how-to/Use-Neo4j.html, source `docs/how-to/Use-Neo4j.ipynb`): "It's necessary to provide some kind of mechanism to indicate which collections are edge collections. This can be inferred from the schema, but here will will make it explicit." (md cell 12); "you can't mix nodes and edges in one collection" (cell 10); "it's possible to map **any** LinkML schema to a property graph. You don't need classes like 'Node' and 'Edge'" (cell 9) — a claim the code does not implement: only the `category`/`subject`/`predicate`/`object` convention is projected; "at this time we don't expose a graph-oriented API, we instead expose everything as node or edge collections" (cell 41); "By default, inserting an edge that points to a non-existent node will create a dangling node in Neo4j" (cell 30). The example schema `docs/how-to/input/movies_kg/schema.yaml` uses `Node`/`Edge` base classes, `designates_type: true` on `category` and `predicate`, and `class_uri: rdfs:Statement` on `Edge`; it does not use `represents_relationship` or `relational_role`.

**Referential integrity in linkml-store (outside the Neo4j adapter).** `Database.iter_validate_database(ensure_referential_integrity=...)` calls `_validate_referential_integrity()` (`src/linkml_store/api/database.py` 651-746): for every collection, for every slot whose range is a class stored in some collection, for every scalar value, it calls `ref_coll.get_one(v)` and yields `ValidationResult(type="ReferentialIntegrity", severity=ERROR, message=f"Referential integrity error: {slot.range} not found")` when no collection holds the target. Off by default (`config.py` 153-156, `ensure_referential_integrity: bool = Field(default=False)`). This is linkml-store code, not `linkml.validator`.

**What it does not handle (confirmed from source):** schema-derived labels; `is_a` label stacking; `represents_relationship`/`relational_role` (grep: no hits in `src/`); inlined/nested objects (a nested dict value would be passed as a Cypher parameter map property; Neo4j does not accept map-typed properties — *inferred*, not executed); constraint emission; batching. Every projection decision it does make is driven by attribute names fixed in `graph_map.py`.

### 1.4 Candidate B: KGX (Knowledge Graph Exchange)

**What it is.** https://github.com/biolink/kgx (latest release v2.7.0, 2026-05-28; head 0dee1bf2). README lines 13-32: "a Python library and set of command line utilities for exchanging Knowledge Graphs (KGs) that conform to or are aligned to the Biolink Model. ... The core datamodel is a Property Graph (PG), represented internally in Python using a networkx MultiDiGraph model." Sources/sinks include "Neo4j endpoints (read/write)"; "This release of KGX supports graph source and sink transactions with Neo4j 4.4" (README 166). Depends on `linkml>=1.9.1,<2.0.0`, `linkml-runtime>=1.9.1,<2.0.0`, `linkml-map` (`pyproject.toml` 33-35) — it uses linkml-runtime's metamodel classes to read the Biolink schema (`kgx/utils/kgx_utils.py` 11, `kgx/sink/rdf_sink.py` 5), not to interpret an arbitrary user schema.

**Input contract** (`docs/kgx_format.md`): node records require `id` and `category` ("Multivalued list with values from the Biolink NamedThing hierarchy", line 53); edge records require `subject`, `predicate`, `object` (81-84). "There is no separate 'KGX schema'—we validate directly against the Biolink Model schema" (line 17).

**Projection rules (from `kgx/sink/neo_sink.py`).**

- Node labels = the node's `category` list, each backticked, joined with `:` (`sanitize_category` 168-185, `write_node` 67-68, `_write_node_cache` 85-90). Every node also gets the label `biolink:NamedThing` (`DEFAULT_NODE_CATEGORY`, `kgx/source/source.py` line 10) so a single uniqueness constraint applies:
  ```
  UNWIND $nodes AS node
  MERGE (n:`biolink:NamedThing` {id: node.id})
  ON CREATE SET n += node, n:{category}
  ON MATCH SET n += node, n:{category}
  ```
  (`generate_unwind_node_query` 188-215). All record keys become node properties (`n += node`).
- Edges: relationship type = the `predicate` value; all record keys become relationship properties:
  ```
  UNWIND $edges AS edge
  MATCH (s:`biolink:NamedThing` {id: edge.subject}), (o:`biolink:NamedThing` {id: edge.object})
  MERGE (s)-[r:`{edge_predicate}`]->(o)
  SET r += edge
  ```
  (`generate_unwind_edge_query` 217-241). Because it is `MATCH ... MERGE`, an edge whose endpoint node does not exist is silently dropped by Cypher (no row matches) — *inferred from the Cypher semantics; KGX does not log this in the sink*.
- Constraints: `CREATE CONSTRAINT IF NOT EXISTS ON (n:{category}) ASSERT n.id IS UNIQUE` per category plus `biolink:NamedThing` (`create_constraints` 243-288). Note this is Neo4j 3.x/4.x constraint syntax; Neo4j 5 uses `FOR ... REQUIRE`.
- Batched writes with a cache of `CACHE_SIZE = 100000` records (lines 33, 50-53).

**KGX validation** (`kgx/validator.py`, `kgx/error_detection.py`): checks required properties, property value types, that categories are valid Biolink classes and predicates valid Biolink predicates, CURIE well-formedness. `ErrorType.MISSING_NODE` is raised only when an edge record lacks a `subject` or `object` *key* (`kgx/source/source.py` 337-359), not when the referenced node is absent from the graph. Networkx `graph_sink.write_edge` calls `add_edge(subject, object, ...)`, which in networkx auto-creates missing endpoint nodes (`kgx/sink/graph_sink.py` 45-61) — *networkx behaviour, inferred*.

**What it does not handle:** any schema other than Biolink; deriving labels from class names or `is_a` (labels are whatever the data's `category` list says — KGX has a `get_biolink_ancestors` helper in `kgx/utils/kgx_utils.py` 461-477, but whether the Transformer applies it before the sink was **not verified**); edge classes (`represents_relationship`) — edges are flat records with a predicate string; inlined objects; referential integrity.

### 1.5 The only generator that reads `represents_relationship`

`packages/linkml/src/linkml/generators/typedbgen.py` line 8: "``represents_relationship: true`` class → TypeDB ``relation`` type (with ``relates`` roles)"; lines 421-464 and 541-546 branch on `class_def.represents_relationship`. It does not read `relational_role` (grep over the whole monorepo for `relational_role` outside the generated metamodel returns nothing). TypeDB is a different data model (entity/relation/attribute) from Neo4j's LPG, but this file is the closest existing example of "relationship class → non-node construct" and is worth reading as a pattern for role assignment.

### 1.6 Verdict for Q1: write our own, borrow three things

Reasons to reject adopting either candidate against the brief's rule table:

| Rule-table requirement | linkml-store Neo4j | KGX NeoSink |
|---|---|---|
| Identified class → node label from **schema** | No: label from data `category` value | No: label from data `category` list, Biolink only |
| `is_a` → stacked labels | No | No (unless data pre-expanded) |
| `represents_relationship` class → edge, non-role slots → edge properties | No: edge = row with `predicate` string | No: same |
| `relational_role` SUBJECT/OBJECT → endpoints | No: fixed attribute names `subject`/`object` | No: fixed `subject`/`object` |
| Reference slot → edge | No: only edge-collection rows become edges; reference slots on node rows are stored as properties | No |
| Identifier-less inlined object → flattened prefixed properties | No | No |
| Emit constraints from schema | No | Per-category `id` uniqueness only |
| Reject unprojectable schema with reason | No | n/a |
| Tier-2 reference check before write | Partial: per-edge existence query at insert; opt-in DB-wide check | No |

Borrow: (1) the `EdgeProjection` role triple as the runtime shape that `relational_role` SUBJECT/OBJECT(/PREDICATE) resolves into; (2) KGX's `UNWIND $rows ... MERGE` batching and its per-label `id IS UNIQUE` constraint (updated to Neo4j 5 syntax); (3) linkml-store's `_validate_referential_integrity` loop as the reference shape for the Tier-2 pass. Reuse `linkml_runtime.utils.schemaview.SchemaView` (`is_inlined`, `get_identifier_slot`, `class_ancestors`, `class_induced_slots`, `get_type_designator_slot`) so the rule table is evaluated over induced, not asserted, slots.

---

## Q2 evidence

### 2.1 Metamodel features

Source: `linkml_model/model/schema/meta.yaml` and `mappings.yaml` in https://github.com/linkml/linkml-model (v1.11.0, head 35c91fb0). Docs: https://linkml.io/linkml-model/latest/docs/<slot>/.

| Feature | Exists | Definition (verbatim) | Caveats |
|---|---|---|---|
| `identifier` | Yes, `meta.yaml` 1895-1926, domain `slot_definition`, range boolean, `inherited: true` | "True means that the slot is the identifier slot of its class. Such a slot uniquely identifies instances of the class throughout an entire document, meaning there cannot be two (or more) instances of the class (or instances of any of its descendants) with the same value for the identifier slot anywhere in the document." Comments: "A domain can have at most one identifier slot OR a key slot."; "An identifier slot is automatically required."; "The presence of an identifier slot makes a class eligible for being referenced rather than inlined." | Uniqueness is scoped to "an entire document" — not across documents. |
| `inlined` | Yes, 1781-1797, domain `slot_definition`, range boolean | "True means that keyed or identified slot appears in an outer structure by value. False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere." Comments: "classes without keys or identifiers are necessarily inlined as lists"; "only applicable in tree-like serializations, e.g json, yaml". | The "no identifier → always inlined" rule is also stated in https://linkml.io/linkml/schemas/inlining.html (`docs/schemas/inlining.md` line 53: "Note that if the range class does not declare an identifier then `inlined` is always true") and implemented in `SchemaView.is_inlined` (`packages/linkml_runtime/src/linkml_runtime/utils/schemaview.py` 2088-2125: inlined if `inlined`/`inlined_as_list` asserted directly or via slot `is_a`/`mixins` ancestry, "or the slot's range is a class with no identifier/key slot"). |
| `inlined_as_list` | Yes, 1799-1817 | "True means that an inlined slot is represented as a list of range instances. False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance." Comment: "The default loader will accept either list or dictionary form as input. This parameter controls internal representation and output." | Also a third "SimpleDict" form for keyed classes with one extra slot. |
| `represents_relationship` | Yes, 2540-2554, domain `class_definition`, range boolean, alias `is_reified` | "true if this class represents a relationship rather than an entity". Comment: "in the context of property graphs, this should be used when a class is used to represent an edge that connects nodes". | **`status: testing`**. Used only by `typedbgen.py` (see 1.5). Listed among `class_definition` slots at 3120. |
| `relational_role` | Yes, 2556-2566, domain `slot_definition`, range `relational_role_enum`, alias `reification_role` | "the role a slot on a relationship class plays, for example, the subject, object or predicate roles". Comments: "this should only be used on slots that are applicable to class that represent relationships"; "in the context of property graphs, this should be used on edge classes to indicate which slots represent the input and output nodes". | **`status: testing`**. **Not consumed by any generator, validator, or runtime code** (grep of `packages/linkml/src/linkml` and `packages/linkml_runtime/src/linkml_runtime`, excluding the generated metamodel itself, returns no hits). Listed among `slot_definition` slots at 3038. |
| `relational_role_enum` | Yes, 3375-3396 | Five permissible values: `SUBJECT` ("connects a relationship to its subject/source node", meaning `rdf:subject`), `OBJECT` ("object/target node", `rdf:object`), `PREDICATE` ("predicate/property", `rdf:predicate`), `NODE` ("connects a symmetric relationship to a node that represents either subject or object node"), `OTHER_ROLE` ("connects a relationship to a node that is not subject/object/predicate"). | The brief's rule table should decide what to do with `NODE` (symmetric edges) and `OTHER_ROLE` (n-ary) — reject or handle. |
| `is_a` | Yes, 515-531, range `definition` | "A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. ... When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded" | Single inheritance; a strict tree per class — good for label stacking. |
| `mixins` | Yes, 556-571, multivalued, range `definition`, alias `traits` | "A collection of secondary parent classes or slots from which inheritable metaslots are propagated from." Comment: "mixins act in the same way as parents (is_a). They allow a model to have a primary strict hierarchy, while keeping the benefits of multiple inheritance" | If mixins are allowed, the rule table must say whether mixin names also become labels. |
| `multivalued` | Yes, 1501-1510, domain `slot_definition`, range boolean | "true means that slot can have more than one value and should be represented using a list or collection structure." | — |
| `exact_mappings` | Yes, `mappings.yaml` line 48 (declared as `exact mappings`, is_a `mappings`, range `uriorcurie`, multivalued, `inherited: false`, `slot_uri: skos:exactMatch`) | "A list of terms from different schemas or terminology systems that have identical meaning." | Applies to any `element` via `common_metadata`; zero-cost to add later, as the brief assumes. |
| `union_of` | Yes, `meta.yaml` 1285-1294, domain/range `element`, multivalued | "indicates that the domain element consists exactly of the members of the element in the range." **Note: "this only applies in the OWL generation"** (line 1291). Narrowed per element: `class_definition.union_of` range `class_definition` (3138-3139), same for slot/type. | Not honoured by JSON Schema/Pydantic validation; unsuitable for polymorphic ranges in the validator path. |
| `any_of` | Yes, 1070-1080, is_a `boolean_slot`, range `expression`, `exact_mappings: [sh:or]` | "holds if at least one of the expressions hold". Carried by `slot_expression`/`anonymous_slot_expression` (range `anonymous_slot_expression`), `type_expression` (2714-2725), `class_expression` (2923), `path_expression` (2933). | Honoured by `jsonschemagen` (`get_subschema_for_slot` line 819: `slot_is_boolean = any([slot.any_of, slot.all_of, slot.exactly_one_of, slot.none_of])`). This is the polymorphic-range mechanism that validation actually understands. |
| `type_designator` | **No metaslot of this name.** The metaslot is `designates_type`, aliases `["type designator"]`, 1928-1937, domain `slot_definition`, range boolean | "True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition" | https://linkml.io/linkml/schemas/type-designators.html: the type slot's value "MUST be either 'Organization' or any of the transitive subclasses (by following `is_a` or `mixins`)"; range may be `string`, `uri`, `curie`, `uriorcurie`. `jsonschemagen` always includes range-class descendants when the range has a type designator (`jsonschemagen.py` 752-757); `SchemaView.get_type_designator_slot` exists. The brief should use the term `designates_type`. |

`status: testing` appears 30 times in `meta.yaml`, so it is a common marking rather than a deprecation signal; it does mean the semantics may change and that tooling support is not guaranteed.

### 2.2 How `linkml.validator` validates instance YAML/JSON

Package: `packages/linkml/src/linkml/validator/` (https://github.com/linkml/linkml/tree/main/packages/linkml/src/linkml/validator; note the repo is now a monorepo — `linkml-runtime` was merged in on 2025-12-01 per the archived runtime README, and lives at `packages/linkml_runtime`). Docs: https://linkml.io/linkml/data/validating-data.html.

**Architecture.** `Validator.__init__(schema, validation_plugins, strict)` (`validator.py` 27-43). `iter_results_from_source()` (83-118): builds one `ValidationContext(schema, target_class)`, calls `plugin.pre_process(context)` on each plugin, then `for index, instance in enumerate(loader.iter_instances()): for plugin in plugins: for result in plugin.process(instance, context): ... yield result`, then `post_process`. The docs (`docs/data/validating-data.rst` line 73): "the :class:`linkml.validator.Validator` ... does not do any validation itself. Instead, it simply orchestrates validation according to a set of validation plugins." `ValidationContext` (`validation_context.py` 55-63) holds the `SchemaDefinition`, a `SchemaView`, the target class, and lazily builds a JSON Schema validator (via `JsonSchemaGenerator(schema, mergeimports=True, top_class=target, not_closed=..., include_range_class_descendants=...)`, lines 73-97) and a Pydantic model. It holds no registry of seen instances or identifiers.

**Convenience API.** `linkml.validator.validate(instance, schema, target_class)` and `validate_file(file, schema, target_class)` (`__init__.py` 88-156) build a default validator with `[JsonschemaValidationPlugin(closed=closed)]` (line 85; `closed=True` by default). `validate_file` accepts `.csv`, `.tsv`, `.yaml`, `.yml`, `.json`; "Each document within a YAML file is treated as an individual instance to validate. If the top-level of a JSON file is an array, each element of the array is treated as an instance" (131-135).

**CLI.** `linkml-validate --schema S --target-class C data...` or `--config file.yaml` (`docs/data/validating-data.rst` 104-182). Default config plugins: `{"JsonschemaValidationPlugin": {"closed": True}}` (`cli.py` line 26). `--fix` runs `linkml_runtime.processing.referencevalidator.ReferenceValidator.normalize()` first ("Normalize a YAML/JSON data file to conform to the schema (type coercion, collection form restructuring)", `cli.py` 53-59) and then the normal Validator.

**Plugins present in `linkml/validator/plugins/`** (directory listing at head; `plugins/__init__.py` exports the first four):

| Plugin | What it does | Source |
|---|---|---|
| `JsonschemaValidationPlugin(closed=False, include_range_class_descendants=True, json_schema_path=None, allow_null_for_optional_enums=False)` | Generates JSON Schema from the LinkML schema (or reads a file) and runs `jsonschema` `iter_errors` per instance. "If True, use an open world assumption and allow the range of a slot to be any descendant of the declared range. Note that if the range of a slot has a type designator, descendants will always be included." | `jsonschema_validation_plugin.py` 15-113 |
| `PydanticValidationPlugin(closed=False)` | Generates a Pydantic model and calls `model_validate`. "this plugin provides less complete validation than JsonschemaValidationPlugin ... it will fail fast on errors and only report the first error found." | `pydantic_validation_plugin.py` 9-49 |
| `RecommendedSlotsPlugin()` | Walks the instance (following inlined dict/list slots) and warns when a `recommended` slot is missing. | `recommended_slots_plugin.py` 8-45 |
| `InstantiatesValidationPlugin()` | Schema-level check of `instantiates` annotations (`must_not_have_id_slot`, `must_be_inlined`); results yielded once. | `instantiates_validation_plugin.py` 1-135 |
| `ShaclValidationPlugin(closed=False, shacl_path=None, raise_on_conversion_error=False)` | Generates SHACL, converts the instance to a Python object then an RDF graph, runs `pyshacl`. Present in the directory but **not exported** from `plugins/__init__.py` `__all__`; requires `pyshacl`. | `shacl_validation_plugin.py` 16-116 |

Loaders: `json_loader.py`, `yaml_loader.py`, `delimited_file_loader.py`, `passthrough_loader.py`.

### 2.3 Referential integrity: not checked, within or across documents

**Evidence from the JSON Schema generator.** For a slot whose range is a class, `get_type_info_for_slot_subschema` (`packages/linkml/src/linkml/generators/jsonschemagen.py` 736-762) branches on `self.schemaview.is_inlined(slot)`: if inlined, it emits a `$ref` to the class (or its non-abstract descendants); if **not inlined**, it does

```python
id_slot = self.schemaview.get_identifier_slot(slot.range)
return self.get_type_info_for_slot_subschema(id_slot)
```

i.e. the reference is typed exactly as the target class's identifier slot (e.g. `string`, or `string` with `format: uri` for `uriorcurie`). JSON Schema has no construct to assert that a string value equals some other object's identifier, so a well-formed but dangling reference validates. The docs confirm the design ("`inlined: false` ... the range of the has_subtypes slot is a list of strings, where each string is a *reference* to a separate object", `docs/schemas/inlining.md` 51).

**Evidence from the plugins.** None of the five plugins indexes identifiers or resolves references (full read of each file above). A grep of `linkml/validator/` for `referential|dangling|foreign|resolve|exists` finds only import-resolution and plugin-class-resolution code (`cli.py` 13, 29-48, 283) and the `instantiates` plugin's "could not be resolved in the schema" message about class names.

**Evidence from the "ReferenceValidator".** Despite its name, `linkml_runtime.processing.referencevalidator.ReferenceValidator` is a "Reference implementation for validations and normalization" of LinkML spec parts 5 and 6 (`packages/linkml_runtime/src/linkml_runtime/processing/referencevalidator.py` line 1). Its `normalize_reference()` (728-731) does `pk_slot = self._identifier_slot(target); return self.normalize_type(input_object, types[pk_slot.range])` — it coerces the reference value to the identifier's *type* and nothing more. Its `ConstraintType` enum (`processing/validation_datamodel.py` 398 ff.) has Type, MinCount, Required, Recommended, MaxCount, SingleValued, MultiValued, Deprecated, MaxLength, Pattern, Permissible-value, DesignatesType, Rule, Expression constraints — no referential-integrity constraint.

**Within one document.** Because `iter_results_from_source` validates each top-level instance independently and JSON Schema cannot cross-reference, bundling the whole catalogue as one document does not add a reference check. The brief's sentence "`linkml.validator` checks that a reference looks like an identifier, not that the target exists, unless the whole catalogue is bundled into one validation run" is therefore half right: the first clause is confirmed, the exception clause is **not** true.

**Across documents.** Nothing in the validator holds state between instances or files (`ValidationContext` carries schema artefacts only; `Validator` has no cross-instance store).

**Where reference checks do exist in the ecosystem:** linkml-store's opt-in `Database._validate_referential_integrity` (section 1.3) and its Neo4j adapter's per-edge endpoint existence query. Both are outside `linkml.validator`.

### 2.4 Implications for the brief

1. Tier 1 (shape) is correctly owned by `linkml.validator`. Note that the default path *does* generate a JSON Schema internally (`ValidationContext.json_schema_validator`); the brief's assumption "without a generated JSON Schema in the loop" holds only in the sense that no hand-maintained JSON Schema is needed.
2. Tier 2 (reference) must be owned entirely by the generator, with no fallback to bundling. Remove the "unless bundled" clause from the Error Tiers section.
3. Polymorphism in validation: use `any_of` on slot ranges or `designates_type` on the range class (both honoured by `jsonschemagen`); do not rely on `union_of` (OWL only). `include_range_class_descendants=True` is the plugin default, so `range: PrimitiveTask` already admits instances of subclasses when validating inlined objects.
4. The rule table should name `designates_type`, not `type_designator`, and should give a disposition for `relational_role` values `PREDICATE`, `NODE`, `OTHER_ROLE`.
5. Since no generator reads `relational_role`, the component will be the first consumer; `status: testing` on both edge metaslots is a documented risk to record in an ADR.

---

## Could not verify

- Whether the linkml-store Neo4j adapter fails or silently stores nested (inlined) objects: inferred from the Cypher parameter path in `neo4j_collection.py` 118-121 and Neo4j's property-type rules, not executed.
- Whether KGX expands node `category` with Biolink ancestors before writing labels: `get_biolink_ancestors` exists (`kgx/utils/kgx_utils.py` 461-477) but its use in the Transformer path was not traced.
- KGX edge with missing endpoint being silently dropped by `MATCH ... MERGE`: inferred from Cypher semantics; no KGX log statement covers it.
- The linkml-store package version string (dynamic versioning in `pyproject.toml`); the release tag v0.3.2 (2026-04-28) is taken from the GitHub releases API.
- The metamodel docs page for `exact_mappings` reports domain "CommonMetadata and UnitOfMeasure"; this came through a summarising fetch and was not checked against the rendered HTML. The `mappings.yaml` source is authoritative and is what the table cites.
- No claim is made about linkml-store's DuckDB/MongoDB adapters' handling of references beyond `_validate_referential_integrity`.

## Sources consulted

Cloned at these commits (shallow), 2026-09-10:

- linkml/linkml `c10d16a3d6dbf0c89819093fed2465b267b6ce38` (2026-09-10); latest release v1.11.1 (2026-05-20). https://github.com/linkml/linkml
- linkml/linkml-model `35c91fb01382bb1c562e6179823241e836b29519` (2026-08-25); v1.11.0 (2026-05-14). https://github.com/linkml/linkml-model
- linkml/linkml-store `e4023ed3a210545a424a8ca2ebea6d5039b871fe` (2026-04-28); v0.3.2 (2026-04-28). https://github.com/linkml/linkml-store
- biolink/kgx `0dee1bf2f0f964f8be3bc529fcb67eb20974f2bb` (2026-05-28); v2.7.0 (2026-05-28). https://github.com/biolink/kgx
- linkml/linkml-runtime `7f98f22080dceca3abed8130a9de07d030fd2e59` (2025-12-10, archived; code now in linkml monorepo `packages/linkml_runtime`). https://github.com/linkml/linkml-runtime

Docs pages fetched: https://linkml.io/linkml/generators/index.html · https://linkml.io/linkml/faq/tools.html · https://linkml.io/linkml/howtos/model-property-graphs.html · https://linkml.io/linkml/schemas/inlining.html · https://linkml.io/linkml/schemas/type-designators.html · https://linkml.io/linkml/data/validating-data.html · https://linkml.io/linkml-model/latest/docs/represents_relationship/ · https://linkml.io/linkml-model/latest/docs/relational_role/ · https://linkml.io/linkml-model/latest/docs/exact_mappings/ · https://linkml.io/linkml-store/how-to/Use-Neo4j.html · https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/meta.yaml
