# LinkML metamodel, the property-graph how-to, and inheritance

*Research note, 2026-09-12. Answers three questions raised while planning `schema/resource.yaml` and `schema/product.yaml`: what the core metaclasses of the LinkML metamodel are and how the resource constructs map onto them; what the official property-graph how-to offers our projection rule table; and which inheritance features the modules should use. Primary sources only: the linkml-model `meta.yaml` source, linkml.io docs pages and their Markdown sources in the linkml repository, and the installed toolchain (LinkML 1.11.1). Every claim about tool behaviour was probed; probe files live under the session scratchpad `probes/` directory and are quoted in full or in the relevant part. This note extends `docs/research/linkml-neo4j-and-metamodel.md` (2026-09-10); where that note already covers a metaslot, this one cites its section instead of repeating it.*

## Verdicts

**Q1. The metamodel and the resource constructs.** The metamodel index names four core metaclasses, in this order: `SchemaDefinition`, `ClassDefinition`, `SlotDefinition`, `TypeDefinition`. A schema is one `SchemaDefinition` holding named classes, slots, and types. `EnumDefinition` is not on that list; it is an additional `Definition` subclass that this project uses (`ParameterKind` in common, the status enum in resource) and is covered in its own subsection. All of these are `Element`s (named, with `description`); classes, slots, and enums are also `Definition`s (with `is_a`, `abstract`, `mixin`, `mixins`), types are not. The point the project most needs to hold on to: every class, slot, type, and enum is named once at schema level and is global to the merged schema. A name under a class's `slots:` is a reference to that global slot, and `slot_usage` is the only place a slot is refined for one class. Every construct the resource module needs exists and behaves as planned, with two findings. (1) `ifabsent: RobotStatus(idle)` is the right syntax, but it produces no `default` in generated JSON Schema, and `linkml-validate` does not treat an absent `status` as present; only generated Python and Pydantic classes apply it. So the projection component must apply `ifabsent` itself when it writes `status`, and this should be a metamodel rule in the rule table, not a named-slot rule. (2) `inlined: true` must be stated on `activity` and the other three group slots. Without it, `SchemaView.is_inlined` returns False for a range class that has an identifier, the JSON Schema types the slot as a string, and a nested group object fails validation. Everything else matched expectation: `minimum_value: 1` becomes JSON Schema `minimum: 1` and rejects `count: 0`; a multivalued string slot becomes an array of strings; `offers` becomes an array of strings and a dangling capability id validates; `slot_usage: {description: {required: true}}` on one class does not touch another. `linkml-lint` with no config file runs the `recommended` bundle: any warning fails the run (exit 1, `--max-warnings 0`), `standard_naming` accepts CamelCase classes and enums, snake_case slots, and snake_case permissible values such as `out_of_service`, and `recommended` fires on any class, slot, enum, or type without a `description`. The repo has no `.linkmllint.yaml`, so this bundle is what `uv run linkml-lint schema/` and `tests/test_lint.py` enforce.

**Q2. The property-graph how-to.** Nothing in it changes our rule table. Its two projections are the two halves of ours: the "simple" projection (a class-ranged slot is an edge named after the slot) is our reference-slot rule, and the "standard PG pattern" (an edge is an instance of an Edge class carrying properties) is our `represents_relationship` rule. Its concrete mechanics, `class_uri: rdf:Statement`, `subject`/`predicate`/`object` with `slot_uri`, and `designates_type` on `predicate`, are one way to say what `represents_relationship` and `relational_role` already say in the metamodel, and the existing note (section 2.1) settled that we use the metamodel. Verdict per item is in section Q2 below; the only "adopt" items are two sentences of advice, not structure: edges should not carry identifiers, which fixes `Precedence` as an edge class and confirms that a `Subtask` occurrence, which does carry an id because ordering points at it, is a node; and node identifiers are minted by the data author and referenced, not inlined, which is our `id` convention. One clarification for the rule table came out of reading it against `RobotUnit`: an identified object that is inlined in the document (the four group slots) projects exactly as a reference does, node plus edge; `inlined` changes the document shape, never the graph. The brief's rule table only says identifier-less inlined objects flatten; it should also say identified ones do not.

**Q3. Inheritance.** LinkML offers `is_a` (single parent, on classes and slots), `mixins` (secondary parents, no tree constraint), `abstract`, `slot_usage` refinement, `union_of` (OWL generation only), and polymorphism through `designates_type`; the FAQ claims "inheritance/polymorphism" and "object-oriented modeling features" without naming any of them. Probed: an abstract `RobotGroup` parent stays in `$defs` of the generated JSON Schema and can even be validated against directly with `-C RobotGroup`, so `abstract` buys no validation guarantee. Its children do inherit both its slots and its `slot_usage` (`description` required propagated to `Activity`). A slot whose range is the abstract parent is emitted as `$ref: RobotGroup` by `gen-json-schema` but `linkml-validate` accepts a child instance in it, so the shipped `dist/` schema and the validator would disagree on polymorphic slots. A `HasDimensions` mixin unfolds its four slots into `PhysicalProperty` and `BuildingComponent` in JSON Schema exactly as listing the four global slots on both classes would, and adds a class the rule table would have to give a label decision for. Recommendation, keeping it simple: the resource module uses none of these features; five plain classes, global slots reused, `slot_usage` for per-class `required`. Product uses `is_a` only, `Wall is_a BuildingComponent`, and only when a kind needs a slot the others lack, as the brief already says; `BuildingComponent` itself stays concrete because IFC components without a kind are instances of it. Avoid `abstract` (no effect on validation, adds a label with no instances), `mixins` (a second parent kind the rule table must handle), `union_of` (OWL only), and `designates_type` (the class is always known from `-C` and the slot range).

---

## Q1 evidence

The metamodel index, https://linkml.io/linkml-model/latest/docs/meta/, opens: "LinkML is self-describing. Every LinkML schema consists of elements that instantiate classes in this metamodel." Under the heading "Core metaclasses:" it lists exactly four, in this order: SchemaDefinition, ClassDefinition, SlotDefinition, TypeDefinition. This section follows that order. `EnumDefinition` is not one of the four; it is covered separately in 1.2 because the project uses it.

Source for the tables: `meta.yaml` fetched 2026-09-12 from https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/meta.yaml (3435 lines). Line numbers below refer to that file. The copy installed with LinkML 1.11.1 (`.venv/Lib/site-packages/linkml_runtime/linkml_model/model/schema/meta.yaml`, 3406 lines) differs only by three added prefixes and one reordered block, so the same names are present; line numbers there shift by up to 29. Domain, range, and inheritance facts were read with `SchemaView` over the fetched file (`probes/meta_table.py`, `probes/meta_classes.py`).

### 1.1 The four core metaclasses and their shared ancestors

Names in `meta.yaml` are snake_case (`class_definition`); the docs and generated Python use CamelCase (`ClassDefinition`). Same thing.

**Ancestors.** `element` (line 2618) is "A named element in the model", abstract, and mixes in `extensible`, `annotatable`, and `common_metadata` (lines 2625-2628). `common_metadata` (2578) is the mixin that carries `description` (260), `title`, `comments`, `notes`, `see_also`, `aliases`, the `*_mappings`, `status`, `rank`, and the rest of the descriptive metadata. `definition` (2762) is "abstract base class for core metaclasses", `is_a: element`, and adds `is_a` (515), `abstract` (532), `mixin` (542), `mixins` (556). Classes and slots (and enums, 1.2) are `definition`s; types are only `element`s, which is why a type has `typeof` instead of `is_a`.

**How they relate.** A `SchemaDefinition` holds the indexes `classes`, `slots`, `types` (and `enums`). A `ClassDefinition` lists slot names in `slots` and refines them in `slot_usage`. A `SlotDefinition` has a `range` that is a class, a type, or an enum. A `TypeDefinition` has `typeof` pointing at a parent type. `is_a` and `mixins` apply to classes and slots alike (their domain is `definition`).

#### SchemaDefinition (line 2643)
"A collection of definitions that make up a schema or a data model." `is_a: element`.

| Metaslot | Line | Range | Meaning (source) |
|---|---|---|---|
| `id` | 819 | uri | "The official schema URI" |
| `name` | 139 | ncname (refined for schemas) | "a unique name for the schema that is both human-readable and consists of only characters from the NCName set" |
| `version` | 839 | string | "particular version of schema" |
| `description` | 260 | string | "a textual description of the element's purpose and use" (from `common_metadata`) |
| `imports` | 848 | uriorcurie, multivalued | "A list of schemas that are to be included in this schema" |
| `prefixes` | 2406 | prefix | "A collection of prefix expansions that specify how CURIEs can be expanded to URIs" |
| `default_prefix` | 882 | string | "The prefix that is used for all elements within a schema" |
| `default_range` | 894 | type_definition | "default slot range to be used if range element is omitted from a slot definition" |
| `classes` / `slots` / `types` / `enums` | 957 / 942 / 917 / 929 | the four definition metaclasses | "An index to the collection of all ... definitions in the schema" |

Skipped on purpose (RDF, provenance, or tooling metadata): `license`, `emit_prefixes`, `default_curi_maps`, `subsets`, `metamodel_version`, `source_file`, `source_file_date`, `source_file_size`, `generation_date`, `slot_names_unique` (testing), `settings`, `bindings` (testing). Note the metaslot for the slot index is spelled `slot_definitions` in the metamodel (line 942) but is written `slots:` in schema YAML.

#### ClassDefinition (line 3095)
"an element whose instances are complex objects that may have slot-value assignments." `is_a: definition`, mixes in `class_expression`.

| Metaslot | Line | Range | Inherited | Meaning (source) |
|---|---|---|---|---|
| `slots` | 1014 | slot_definition, multivalued | no | "collection of slot names that are applicable to a class" |
| `slot_usage` | 1030 | slot_definition, keyed by slot name | no | "the refinement of a slot in the context of the containing class definition." Comment: "Many slots may be reused across different classes, but the meaning of the slot may be refined by context." |
| `attributes` | 1231 | slot_definition | no | "Inline definition of slots" (a slot declared inside a class; still global in the merged schema, see 1.2) |
| `is_a` | 515 | definition | no | "A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided" |
| `mixins` | 556 | definition, multivalued | no | "A collection of secondary parent classes or slots from which inheritable metaslots are propagated from." |
| `abstract` | 532 | boolean | no | "Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes." |
| `mixin` | 542 | boolean | no | "Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins." |
| `tree_root` | 1296 | boolean | no | "Indicates that this is the Container class which forms the root of the serialized document structure" (banned by SPEC-common) |
| `represents_relationship` | 2540 | boolean | yes | "true if this class represents a relationship rather than an entity" (status testing; see the 2026-09-10 note, 2.1) |
| `union_of` | 1285 | class_definition | no | "indicates that the domain element consists exactly of the members of the element in the range." Note: "this only applies in the OWL generation" |
| `unique_keys` | 1310 | unique_key | no | "A collection of named unique keys for this class" (not needed; one `identifier` per class) |

Skipped on purpose: `class_uri`, `subclass_of` (deprecated), `defining_slots`, `rules`, `classification_rules`, `slot_names_unique`, `disjoint_with`, `children_are_mutually_disjoint`, `extra_slots`, `alias`, and the boolean class expressions `any_of`, `all_of`, `exactly_one_of`, `none_of` on classes.

#### SlotDefinition (line 2992)
"an element that describes how instances are related to other instances." `is_a: definition`, mixes in `slot_expression` (2942), which is where `range`, `required`, `multivalued`, `inlined`, and the value constraints come from. "Inherited: yes" means the value propagates down `is_a`/`mixins` and into `slot_usage`.

| Metaslot | Line | Range | Inherited | Meaning (source) |
|---|---|---|---|---|
| `range` | 1455 | element (a class, type, or enum) | yes | "defines the type of the object of the slot" |
| `required` | 1743 | boolean | yes | "true means that the slot must be present in instances of the class definition" |
| `recommended` | 1756 | boolean | yes | "true means that the slot should be present in instances of the class definition, but this is not required" |
| `multivalued` | 1501 | boolean | yes | "true means that slot can have more than one value and should be represented using a list or collection structure." |
| `identifier` | 1895 | boolean | yes | "True means that the slot is the identifier slot of its class." Comments: "An identifier slot is automatically required."; "The presence of an identifier slot makes a class eligible for being referenced rather than inlined." |
| `key` | 1871 | boolean | yes | "True means that the slot is the 'singular unique key' ... of its class" (the brief uses it for parameter maps) |
| `inlined` | 1781 | boolean | yes | "True means that keyed or identified slot appears in an outer structure by value. False means that only the key or identifier for the slot appears within the domain" |
| `inlined_as_list` | 1799 | boolean | yes | "True means that an inlined slot is represented as a list of range instances. False means ... a dictionary, whose key is the slot key or identifier" |
| `minimum_value` / `maximum_value` | 2107 / 2120 | Anything | yes | "For ordinal ranges, the value must be equal to or higher than this" / "lower than this" |
| `ifabsent` | 1583 | string | yes | "function that provides a default value for the slot." The listed forms include `int(value)`, `string(value)`, `[Tt]rue`, `[Ff]alse`, and `EnumName(PermissibleValue) -- enum value` |
| `pattern` | 2147 | string | yes | "the string value of the slot must conform to this regular expression" |
| `minimum_cardinality` / `maximum_cardinality` | 1675 / 1686 | integer | yes | "the minimum number of entries for a multivalued slot" / "the maximum ..." |
| `any_of` | 1070 | anonymous_slot_expression | no | "holds if at least one of the expressions hold" (the polymorphic-range form the validator honours; 2026-09-10 note, 2.1) |
| `designates_type` | 1928 | boolean | yes | "True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition" |
| `relational_role` | 2556 | relational_role_enum | yes | "the role a slot on a relationship class plays" (status testing; 2026-09-10 note, 2.1) |
| `is_a` / `mixins` / `abstract` | 515 / 556 / 532 | definition | no | same meaning as for classes; slots may form their own hierarchy |

Skipped on purpose: `slot_uri`, `subproperty_of`, `domain`, `domain_of`, `inherited`, `readonly`, `singular_name`, `list_elements_unique`, `list_elements_ordered`, `shared`, `alias`, `owner` (deprecated), `is_usage_slot` (deprecated), `usage_slot_name`, `symmetric`, `reflexive`, `locally_reflexive`, `irreflexive`, `asymmetric`, `transitive`, `inverse`, `is_class_field`, `transitive_form_of`, `reflexive_transitive_form_of`, `role`, `slot_group`, `is_grouping_slot`, `path_rule`, `disjoint_with`, `children_are_mutually_disjoint`, `union_of`, `type_mappings`, `range_expression`, `enum_range`, `bindings`, `structured_pattern`, `unit`, `implicit_prefix`, `value_presence`, `equals_*`, `exact_cardinality`, `has_member`, `all_members`, `all_of`, `exactly_one_of`, `none_of`, `array`.

#### TypeDefinition (line 2734)
"an element that whose instances are atomic scalar values that can be mapped to primitive types." `is_a: element` (not `definition`), mixes in `type_expression`.

| Metaslot | Line | Range | Inherited | Meaning (source) |
|---|---|---|---|---|
| `typeof` | 2260 | type_definition | no | "A parent type from which type properties are inherited" |
| `base` | 2274 | string | yes | "python base type in the LinkML runtime that implements this type definition" (root types only; `linkml:types` supplies it for `string`) |
| `uri` (`type_uri`) | 2286 | uriorcurie | yes | "The uri that defines the possible values for the type definition" (root types only) |
| `pattern` / `minimum_value` / `maximum_value` | 2147 / 2107 / 2120 | | yes | same as on slots, applied to every slot of the type |

Skipped on purpose: `repr`, `union_of`, `structured_pattern`, `unit`, `implicit_prefix`, `equals_*`, the boolean type expressions. The linter's `root_type_checks` requires `base` and `uri` on root types only; `MaterialName` has `typeof: string`, so it is a child type and needs neither.

### 1.2 EnumDefinition: an additional Definition subclass this project uses

Not one of the four core metaclasses on the index page. It is a metaclass of its own (https://linkml.io/linkml-model/latest/docs/EnumDefinition/, "Class: EnumDefinition", `is_a: definition`, mixes in `enum_expression`), held in the `SchemaDefinition.enums` index (line 929), and used by this project for `ParameterKind` in common and the status enum in resource. Because it is a `definition`, it has `is_a`, `mixins`, `abstract`, and `description` like a class or slot. A slot uses an enum by naming it as `range`.

#### EnumDefinition (line 2800)
"an element whose instances must be drawn from a specified set of permissible values." `is_a: definition`, mixes in `enum_expression` (2779).

| Metaslot | Line | Range | Meaning (source) |
|---|---|---|---|
| `permissible_values` | 641 | permissible_value, keyed by `text` | "A list of possible values for a slot range" |
| `permissible_value.text` | 783 | string | "The actual permissible value itself" (the YAML key) |
| `permissible_value.description` | 260 | string | from `common_metadata`, which `permissible_value` (3269) mixes in |
| `permissible_value.meaning` | 800 | uriorcurie | "the value meaning of a permissible value" (ontology mapping; skip for now) |
| `is_a` / `mixins` | 515 / 556 | | also available on enums and, separately, on permissible values |

Skipped on purpose (dynamic enums and code sets): `enum_uri`, `code_set`, `code_set_tag`, `code_set_version`, `pv_formula`, `include`, `minus`, `inherits`, `reachable_from`, `matches`, `concepts`, `permissible_value.unit`, `implements`, `instantiates`.

### 1.3 What is schema-global

`SchemaDefinition.slots`, `classes`, `types`, and `enums` are indexes "to the collection of all ... definitions in the schema" (lines 917-957). `element.name` is "the unique name of the element within the context of the schema" (139). So:

- A slot is declared once, under `slots:`, and is global. `ClassDefinition.slots` is a "collection of slot names" (1014): the entries are references, not definitions. The linter's `no_undeclared_slots` rule (`rules.py` 220-241) turns this into an error: "Slot 'x' from class 'C' not found in schema 'slots' declaration."
- `slot_usage` is "the refinement of a slot in the context of the containing class definition" (1030). It is keyed by the global slot's name and may set any inherited metaslot (`required`, `range`, `inlined`, `minimum_value`, ...) for that class only. The probe in 1.4 shows `description` required on `Activity` and optional on `PhysicalProperty` from one global `description` slot.
- `attributes` (1231) declares a slot inline inside a class. After import merging it is still one named slot in the schema, so two classes each declaring an attribute `name` collide unless `slot_names_unique` handling applies. The repo convention (declare everything under `slots:`) avoids the question.
- `imports` (848) merges whole schemas: every class, slot, type, and enum of `common` is present, by name, in a module that imports it. The probe JSON Schema for `resource_probe.yaml` has `ParameterKind`, `Position`, `Quantity`, `CapabilityType` in `$defs` although the probe never mentions them. This is why SPEC-common bans redefining `id` or `description` in another module: the second definition would be a second global slot with the same name.
- Types and enums are global in the same way; `default_range` (894) names one global type that every slot without a `range` gets.

### 1.4 Applying the metaclasses: the resource constructs, probed

Probe schema `probes/resource_probe.yaml` (imports `linkml:types` and a scratch copy of `common.yaml`):

```yaml
enums:
  RobotStatus:
    description: The runtime state of one machine.
    permissible_values:
      idle: {description: Available for work.}
      deployed: {description: Working on a task.}
      charging: {description: Charging.}
      out_of_service: {description: Not available.}
classes:
  RobotUnit:
    description: One robot product entry.
    slots: [id, count, status, aliases, activity, physical_property]
    slot_usage:
      activity: {required: true}
  Activity:
    description: The activity group.
    slots: [id, description, offers]
    slot_usage:
      description: {required: true}
  PhysicalProperty:
    description: The physical property group.
    slots: [id, description, manufacturer, length]
slots:
  count: {range: integer, minimum_value: 1, required: true, description: ...}
  status: {range: RobotStatus, ifabsent: RobotStatus(idle), description: ...}
  aliases: {multivalued: true, description: ...}
  activity: {range: Activity, inlined: true, description: ...}
  physical_property: {range: PhysicalProperty, inlined: true, description: ...}
  offers: {range: CapabilityType, multivalued: true, required: true, description: ...}
  manufacturer: {description: ...}
  length: {range: Quantity, description: ...}
```

`resource_probe_noinline.yaml` is the same file with `inlined: true` removed from `activity` only.

**`uv run gen-json-schema probes/resource_probe.yaml`**, relevant fragments of `$defs`:

```
$defs keys: ['Activity', 'CapabilityType', 'ParameterKind', 'PhysicalProperty', 'Position', 'Quantity', 'RobotStatus', 'RobotUnit']
RobotUnit.count    {"minimum": 1, "type": "integer", ...}
RobotUnit.status   {"$ref": "#/$defs/RobotStatus", ...}
RobotUnit.aliases  {"items": {"type": "string"}, "type": ["array", "null"], ...}
RobotUnit.activity {"$ref": "#/$defs/Activity", ...}
RobotUnit.physical_property {"anyOf": [{"$ref": "#/$defs/PhysicalProperty"}, {"type": "null"}], ...}
RobotUnit.required ['id', 'count', 'activity']
Activity.offers    {"items": {"type": "string"}, "type": "array", ...}
Activity.required  ['id', 'description', 'offers']
PhysicalProperty.required ['id']
PhysicalProperty.length {"anyOf": [{"$ref": "#/$defs/Quantity"}, {"type": "null"}], ...}
RobotStatus {"enum": ["idle", "deployed", "charging", "out_of_service"], "title": "RobotStatus", "type": "string", ...}
any 'default' key anywhere: False
```

**`uv run gen-json-schema probes/resource_probe_noinline.yaml`**:

```
RobotUnit.activity {"description": "The activity group of this entry.", "type": "string"}
```

**`uv run linkml-validate -s probes/resource_probe.yaml -C RobotUnit <data>`**:

```
data/valid.yaml            (count 2, nested activity, offers: [locomote, grip, does_not_exist], length: {value: 3.0, unit: m})
  No issues found                                                                   exit 0
data/count_zero.yaml       (count: 0)
  [ERROR] ... 0 is less than the minimum of 1 in /count                             exit 1
data/activity_as_string.yaml (activity: sam100_activity)
  [ERROR] ... 'sam100_activity' is not of type 'object' in /activity                exit 1
data/activity_missing_description.yaml (activity without description; physical_property without description)
  [ERROR] ... 'description' is a required property in /activity                     exit 1
```

Against the no-inline schema:

```
data/activity_as_string.yaml   No issues found                                      exit 0
data/valid.yaml                [ERROR] ... {'id': 'sam100_activity', ...} is not of type 'string' in /activity   exit 1
```

**`ifabsent`**: `probes/resource_probe_status_required.yaml` adds `required: true` under `status` (keeping `ifabsent`). Validating `data/valid.yaml`, which has no `status`:

```
[ERROR] ... 'status' is a required property in /                                    exit 1
```

Generated code does apply the default. `gen-python` line 112: `status: Optional[Union[str, "RobotStatus"]] = 'idle'`. `gen-pydantic` line 168: `status: Optional[RobotStatus] = Field(default=RobotStatus.idle, ...)`. Constructing `RobotUnit(id="sam100", count=1, activity=...)` from the generated dataclass gives `status = RobotStatus(text='idle', ...)`.

**`SchemaView`** (the calls the projection component will make), `probes/` output:

```
resource_probe           RobotUnit.activity        range=Activity        inlined=True is_inlined()=True  multivalued=None required=True
resource_probe           Activity.offers           range=CapabilityType  inlined=None is_inlined()=False multivalued=True required=True
resource_probe           PhysicalProperty.length   range=Quantity        inlined=None is_inlined()=True  (Quantity has no identifier)
resource_probe           RobotUnit.count           range=integer         min=1
resource_probe           RobotUnit.status          range=RobotStatus     ifabsent=RobotStatus(idle)
resource_probe_noinline  RobotUnit.activity        range=Activity        inlined=None is_inlined()=False
identifier slot of Activity: id | of Quantity: None
```

**Readings.**

1. `minimum_value: 1` on an integer slot is the right metaslot. It becomes `"minimum": 1` and the validator enforces it.
2. `ifabsent: RobotStatus(idle)` is the exact syntax for an enum default (`meta.yaml` 1583-1600, form `EnumName(PermissibleValue)`). It is not emitted into JSON Schema and the validator does not fill it in. A required slot with an `ifabsent` still fails when absent. The default lives in generated Python and Pydantic only. **Consequence for the design:** keep `status` optional with `ifabsent`, and make the projection component write the `ifabsent` value when the slot is absent. Reading `induced_slot(...).ifabsent` is a metamodel read, so this is a general rule for any primitive or enum slot, not a second named-slot rule.
3. A multivalued slot with the schema default range is `array` of `string`. `"type": ["array", "null"]` appears because the slot is optional.
4. `inlined: true` is needed on every slot whose range has an identifier and whose value is written by value. `SchemaView.is_inlined` is False without it (the range has an identifier, so nothing forces inlining), the JSON Schema types the slot as `string`, and a nested object is rejected. The 2026-09-10 note (2.1) already records the rule; this probe shows the failure mode.
5. `offers` without `inlined` is an array of strings, and `does_not_exist` validates. Referential integrity is the generator's tier 2 job, as the existing note established (2.3).
6. `slot_usage: {description: {required: true}}` on `Activity` puts `description` in `Activity.required` and leaves `PhysicalProperty.required` at `['id']`. One global slot, two per-class requirements.
7. Optional class-ranged slots become `anyOf [$ref, null]`; required ones a bare `$ref`. Optional enum slots get a bare `$ref` (no null) because the plugin's `allow_null_for_optional_enums` is False by default. Cosmetic, but it explains the difference between `status` and `physical_property` above.

### 1.5 Applying the metaclasses: what `linkml-lint` enforces

Source: installed `linkml/linter/cli.py`, `linter.py`, `rules.py`, `config/default.yaml`, `config/recommended.yaml` (LinkML 1.11.1). Diffed against GitHub main on 2026-09-12: `recommended.yaml` and `cli.py` are identical; main's `rules.py` adds two rules (`no_invalid_slot_group`, `no_undeclared_subsets`) that are disabled in `default.yaml` and not in `recommended.yaml`, so they do not affect the result.

**Which config runs.** `cli.py` line 16: `DEFAULT_CONFIG_FILES = [".linkmllint.yaml", ".linkmllint.yml"]`; lines 105-119: if `--config` is not given, the CLI looks for those two names in the current working directory, and otherwise uses `{"extends": "recommended"}`. `linter.py` 74-81 merges `recommended.yaml` over `default.yaml`, in which every rule is `disabled`. The repo has no `.linkmllint.yaml` (checked at the repo root; `tests/test_lint.py` runs `linkml-lint <module>` with no config flag), so the recommended bundle is what runs.

**The recommended bundle** (`config/recommended.yaml`):

| Rule | Level | What it checks (`rules.py`) |
|---|---|---|
| `recommended` | warning | every class, slot, enum, type, and subset (`all_elements(imports=False)`) has each metaslot the metamodel marks `recommended`; in practice that is `description` (plus `ucum_code` on units and `alias_predicate` on structured aliases, which we do not use). Permissible values are not checked ("todo PVs are not checked", line 128). |
| `no_xsd_int_type` | error | no type with `uri: xsd:int` |
| `no_invalid_slot_usage` | error | every `slot_usage` key is a slot of that class |
| `no_undeclared_slots` | error | every slot listed under a class is declared globally |
| `no_undeclared_ranges` | error | every slot range and `default_range` is a declared class, type, or enum |
| `one_identifier_per_class` | error | at most one `identifier: true` among a class's induced slots |
| `one_key_per_class` | error | at most one `key: true` |
| `root_type_checks` | error | `typeof` targets exist; root types have `base` and `uri` |
| `standard_naming` | warning | see below |
| `canonical_prefixes` | warning | declared prefixes agree with the `merged` prefixmaps context |

**Exit code.** `cli.py` 140-156: `exit 2` if any error, `exit 1` if warnings exceed `--max-warnings` (default 0) and `--ignore-warnings` is not set. So a single warning fails `tests/test_lint.py`.

**`standard_naming` patterns** (`rules.py` 38-45, 379-396): classes and enums `[A-Z][a-zA-Z0-9]+`; slots `[a-z][_a-z0-9]+`; permissible values `[a-z][_a-z0-9]+` unless `permissible_values_upper_case: true`, then `[A-Z][_A-Z0-9]+`. All patterns require at least two characters (the `+` after the first character), which is why `x` failed and `x_coord` was chosen (SPEC-common decision 9).

**Probe, planned names.** `uv run linkml-lint probes/resource_probe.yaml` (CamelCase classes and enum, snake_case slots, `out_of_service`):

```
✓ No problems found
exit 0
```

`uv run linkml-lint probes/inherit_probe.yaml` (abstract, mixins, is_a): `✓ No problems found`, exit 0. `uv run linkml-lint schema/` from the repo root: `✓ No problems found`, exit 0.

**Probe, names the style avoids.** `probes/lint_bad.yaml` declares enum `robot_status` with values `idle`, `OUT_OF_SERVICE`, `out-of-service`, `Deployed`; class `robot_unit`; slots `CountOf` and `x`; and class `NoDescription` and slot `x` without descriptions:

```
  warning  Class 'NoDescription' does not have recommended slot 'description'  (recommended)
  warning  Slot 'x' does not have recommended slot 'description'  (recommended)
  warning  Class has name 'robot_unit'  (standard_naming)
  warning  Slot has name 'CountOf'  (standard_naming)
  warning  Slot has name 'x'  (standard_naming)
  warning  Enum has name 'robot_status'  (standard_naming)
  warning  Permissible value of Enum 'robot_status' has name 'OUT_OF_SERVICE'  (standard_naming)
  warning  Permissible value of Enum 'robot_status' has name 'out-of-service'  (standard_naming)
  warning  Permissible value of Enum 'robot_status' has name 'Deployed'  (standard_naming)

✖ Found 9 problems in 1 schema
exit 1
```

So the planned shape passes: `RobotUnit`, `PhysicalProperty`, `RobotStatus`, `out_of_service`, `physical_property`, `offers`. The two things that would fire are a missing `description` on any class, slot, enum, or type, and a permissible value in upper snake case. Permissible values without a description do not fire, but SPEC-common's "every element has a description" rule covers them anyway.

---

## Q2 evidence

Source: https://linkml.io/linkml/howtos/model-property-graphs.html and its Markdown `docs/howtos/model-property-graphs.md` in linkml/linkml main (460 lines, fetched 2026-09-12); line numbers refer to the Markdown. The 2026-09-10 note, section 1.2, already quotes the two tables and the Edge class; the tables are repeated here only so the per-item verdicts can point at rows.

### 2.1 The two projections

Simple projection (lines 73-79), "each edge is a slot":

| Graph Element | LinkML |
|---|---|
| Node | instance of a Class |
| Edge | Attribute-Value Assignment |
| Predicate (Edge Label) | Attribute |
| Node Property | Attribute-Value Assignment |
| Edge Property | *not represented* |

Standard PG pattern (lines 228-234), "classes for nodes, and classes for edges":

| Graph Element | LinkML |
|---|---|
| Node | instance of a (Node) Class |
| Edge | instance of an (Edge) Class |
| Predicate (Edge Label) | (Edge) Class |
| Node Property | Attribute-Value Assignment on Node instance |
| Edge Property | Attribute-Value Assignment on Edge instance |

Our rule table is the union of the two: a class-ranged slot on a node class is an edge named after the slot (simple projection, row "Edge"), and a class marked `represents_relationship` is an edge carrying its non-role slots (standard pattern, rows "Edge" and "Edge Property"). The how-to presents them as alternatives for one schema; nothing in it forbids using both, and its own second schema still has plain attributes on nodes.

### 2.2 The Node/Edge base-class pattern

Lines 182-224: `Node` is `abstract: true` with `id` (identifier, `uriorcurie`), `name` (`slot_uri: rdfs:label`), `category` (`slot_uri: rdf:type`, `designates_type: true`), and `types` (multivalued string). `Edge` is `abstract: true` with `class_uri: rdf:Statement`, `subject`/`object` (range `Node`, `slot_uri: rdf:subject`/`rdf:object`), and `predicate` (`uriorcurie`, `slot_uri: rdf:predicate`, `designates_type: true`). A `Graphs` container holds `nodes` and `edges` as inlined lists. Domain classes are `Person is_a Node`, `ActedIn is_a Edge` with attribute `role` (lines 256-275). A later variant (397-433) adds a separate `type` designator so that edge classes can be finer than predicates (`AnatomicalHasPart is_a HasPart`, with `slot_usage` narrowing `subject`/`object`).

Design notes the how-to states (lines 239-252): "nodes have identifiers, and references to nodes from edges are not inlined. Data providers are expected to mint these."; "edges do not have identifiers. This makes it harder for an edge to reference another edge."; "we use the RDF reification vocabulary for URIs, but we could use anything here."; "we use `name` for a human-readable name, and map this to `rdfs:label` (not to be confused with neo4j labels)"; "`Node` uses a `category` as a type designator"; "We also allow any number of types to be associated with a node (akin to 'labels' in neo4j)". Line 277: "edges are 'first-class', and nodes no longer 'own' the edges. From a graph database perspective, there is no such distinction, but this has implications for e.g. Pydantic and JSON representations." Line 454: "We are currently exploring options for allow features such as auto-asserting PG style models when mapping to RDF-star."

### 2.3 Verdict per item

| Item in the how-to | Verdict | Reason |
|---|---|---|
| Simple projection: class-ranged slot is an edge labelled by the slot | already covered | It is our reference-slot rule. `RobotUnit.activity` becomes `-[:ACTIVITY]->`, `Activity.offers` becomes one `-[:OFFERS]->` per value. |
| Simple projection cannot carry edge properties | already covered | That is why `Precedence` is a class marked `represents_relationship`, not a slot on the task. |
| Standard pattern: edge is an instance of an Edge class, edge properties are its slots | already covered | Our `represents_relationship` rule (2026-09-10 note, 2.1). |
| `Node`/`Edge` abstract base classes | ignore | They exist so that generic tooling can find nodes and edges by ancestry. Our component finds them by `identifier` and `represents_relationship` on each class, so the base classes would add two labels with no instances and an `is_a` on every class. Q3 shows `abstract` has no validation effect either. |
| `class_uri: rdf:Statement`, `slot_uri: rdf:subject/predicate/object` | ignore | RDF vocabulary for an RDF serialisation we do not produce in the first slice. The brief bans graph and RDF vocabulary in the model; `relational_role: SUBJECT/OBJECT` says the same thing inside the metamodel. If RDF export arrives later, `class_uri`/`slot_uri` can be added without touching the rule table. |
| `designates_type: true` on `predicate` and `category` | ignore | The how-to needs it because all edges share one `Edge` class in one `edges` list and the type must be read from the data. Our documents are validated per class with `-C`, every slot range names one class, and the edge type is the class name. No type field in the data, nothing for the component to read. |
| `types` multivalued string "akin to labels in neo4j" | ignore | Labels come from the class and its `is_a` chain in our table, from the schema, never from data. A data-carried label list would be exactly the linkml-store/KGX convention the 2026-09-10 note rejected (1.6). |
| `name` mapped to `rdfs:label` | ignore | SPEC-common decision 5: no `label` slot; ids are readable. |
| "nodes have identifiers ... references to nodes from edges are not inlined. Data providers are expected to mint these." | adopt (already our convention) | Matches `id` authored per instance and reference slots without `inlined`. Worth quoting in `PROJECTION.md` as outside confirmation. |
| "edges do not have identifiers. This makes it harder for an edge to reference another edge." | adopt as a rule-table check | Confirms `Precedence` should have no `id` (an edge class with an identifier is unprojectable: Neo4j relationships have no uniqueness constraint keyed by a property in the same sense, and nothing may point at an edge). It also confirms the brief's `Subtask` choice: a subtask occurrence carries an id because ordering constraints point at it, so it is a node, and `Precedence` is the edge between two such nodes. The component should reject a `represents_relationship` class that has an identifier, with that reason. |
| `Graphs` container with `nodes`/`edges` lists | ignore | SPEC-common decision 10: no container, no `tree_root`; documents are lists validated with `-C`. |
| Finer edge classes than predicates (`AnatomicalHasPart is_a HasPart`, `slot_usage` on `subject`/`object`) | ignore for now | We have one edge class per relationship kind and the class name is the edge type, so there is no predicate/class split to manage. `slot_usage` narrowing `subject`/`object` ranges is a good pattern if a second edge class ever shares role slots; note it, do not build it. |
| Direction: "nodes no longer own the edges ... implications for Pydantic and JSON" | already covered | Our reference slots do sit on the owning node (`RobotUnit.activity`, `PrimitiveTask.requires`), which is the how-to's simple projection; `Precedence` is a first-class edge object. Both shapes are in the table; the document shape follows the metamodel, not a house preference. |
| Assertions vs quotes, RDF-star | ignore | Concerns RDF serialisation of reified edges. Not a first-slice output. |

### 2.4 Does it apply to Precedence, Subtask, and RobotUnit's groups?

**Precedence (edge class).** The how-to's edge properties are "Attribute-Value Assignment on Edge instance" (line 234). Our `Precedence` carries which event of the earlier task and which of the later (start or end); those are its non-role slots and become edge properties by the same rule. The how-to's `Edge` uses `subject`/`object` slots ranging over `Node`; ours use `relational_role: SUBJECT`/`OBJECT` and range over the subtask class. Same shape, metamodel words. Multivalued slots on an edge class: the how-to has none, and Neo4j relationship properties may be lists of primitives but not of nodes, so the component should accept multivalued primitive slots on an edge class and reject multivalued class-ranged ones. This is a rule the brief's table does not yet spell out.

**Subtask (node).** The how-to's caution that "edges do not have identifiers" is the reason `Subtask` occurrences are nodes: they have an id, and `Precedence` points at them. This matches the brief's Decisions Taken by Default ("Subtask occurrences carry a real identifier and become nodes by the standard rule, because ordering constraints point at them").

**RobotUnit to group nodes.** Under the simple projection `RobotUnit.activity` with range `Activity` is an edge labelled by the slot. The how-to's example uses references (line 123: "We are using references rather than inlining here"), and says nothing about an identified object written inline. Our groups are identified and inlined. The metamodel is clear that `inlined` is "only applicable in tree-like serializations, e.g json, yaml" (2026-09-10 note, 2.1). So the projection of an identified object is the same whether it arrives inline or by reference: a node under its own label, an edge from the holder named after the slot. Only identifier-less objects (`Quantity`, `Position`) flatten. The brief's Recommended Direction says "identifier-less inlined objects are flattened to prefixed properties"; it should add the sentence "identified objects project as nodes whether inlined or referenced". The `count` rule then applies the same group nodes to every machine node, as `robot-entry-as-type.md` already draws.

**Anything about identifiers or node labels.** Identifiers: nodes need them, edges should not have them, data providers mint them (lines 239-241). Labels: the how-to treats `types` as data (line 249) and warns not to confuse `rdfs:label` with Neo4j labels (line 244). Our labels are schema-derived from the class and `is_a`; the how-to gives no rule for that because it never leaves the modelling layer.

---

## Q3 evidence

Sources: https://linkml.io/linkml/schemas/inheritance.html (Markdown `docs/schemas/inheritance.md`, 128 lines) and https://linkml.io/linkml/faq/why-linkml.html (Markdown `docs/faq/why-linkml.md`, 505 lines), both fetched 2026-09-12; `meta.yaml` as in Q1; probes below.

### 3.1 What LinkML offers

| Feature | Metaslot and source | What the docs say |
|---|---|---|
| `is_a` on classes | `meta.yaml` 515, domain `definition` | "can be used to define a backbone hierarchy for your class. All inheritable metamodel slots are propagated down the is_a hierarchy." (inheritance.md 5). "While multiple inheritance is not allowed, mixins can be provided" (meta.yaml 515-531). |
| `is_a` on slots | same metaslot; `SlotDefinition` is a `definition` | "Slots can also be organized in hierarchies using `is_a`." (inheritance.md 34). `SchemaView.is_inlined` follows slot `is_a`/`mixins` ancestry (2026-09-10 note, 2.1). |
| `mixins` / `mixin` | 556 / 542 | "Mixin parents operate similarly to `is_a` parents, but they do not have the constraint of forming a tree." (72). Uses: "generalize a set of attributes that can apply to classes in different parts of the class hierarchy", "reduce duplication", avoid "the diamond problem" (74-77). Rule: "`is_a` SHOULD only connect either (1) two mixins (2) two non-mixin elements" (109). |
| `abstract` | 532 | "another class (or slot) can use the abstract class (or slot) as part of its inheritance hierarchy, but the abstract class itself cannot be directly instantiated." (38). "Some generators may choose to utilize abstract tags, e.g to mask generation of abstract classes." (59). The wording "may choose" is exact: see 3.2, the JSON Schema generator does not. |
| `slot_usage` refinement | 1030 | "if Person uses `slot_usage` ... to refine the meaning of a generic slot in the context of Person, then these will be materialized for Person." (126-128). `gen-linkml --materialize-attributes` writes the induced slots out (118-122). |
| `union_of` | 1285 | "this only applies in the OWL generation" (meta.yaml 1291; 2026-09-10 note, 2.1). Not mentioned on the inheritance page. |
| Polymorphism via `designates_type` | 1928 | Not on the inheritance page; covered by the type-designators page and the 2026-09-10 note, 2.1. |

**The FAQ's claims.** Under "Why should I use LinkML over JSON-Schema?" (why-linkml.md 120-137) the first bullet is "You want to make use of inheritance/polymorphism", with "you can always compile your LinkML schema down to JSON-Schema!" (124-125). Under Frictionless Data (413): "LinkML supports object-oriented modeling features." The page names none of `is_a`, `mixins`, `abstract`, `slot_usage`, `union_of`, or `designates_type` (confirmed by grep of the source and by fetching the rendered page). It makes no claim about how the features survive compilation; the `is_a` definition in `meta.yaml` (515-531) does: "When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded".

### 3.2 Probe (a): an abstract `RobotGroup` parent

`probes/inherit_probe.yaml` (imports the scratch `common.yaml`):

```yaml
classes:
  RobotGroup:
    abstract: true
    description: One group of Construction Robot Schema attributes.
    slots: [id, description]
    slot_usage:
      description: {required: true}
  Activity:
    is_a: RobotGroup
    description: The activity group.
    slots: [offers]
    slot_usage:
      offers: {required: true}
  Safety:
    is_a: RobotGroup
    description: The safety group.
    slots: [safety_barrier]
  HasDimensions:
    mixin: true
    description: Length, width, height, and weight.
    slots: [length, width, height, weight]
  PhysicalProperty:
    is_a: RobotGroup
    mixins: [HasDimensions]
    description: The physical property group.
    slots: [manufacturer]
  BuildingComponent:
    description: A component of the building.
    mixins: [HasDimensions]
    slots: [id, material]
  Wall:
    is_a: BuildingComponent
    description: A wall.
    slots: [thickness]
  RobotUnit:
    description: One robot product entry.
    slots: [id, group, groups]
slots:
  ...  # offers, safety_barrier, length/width/height/weight (Quantity), manufacturer, material (MaterialName), thickness (Quantity)
  group:  {range: RobotGroup, inlined: true}
  groups: {range: RobotGroup, multivalued: true, inlined: true, inlined_as_list: true}
```

**`uv run gen-json-schema probes/inherit_probe.yaml`**:

```
$defs keys: ['Activity', 'BuildingComponent', 'CapabilityType', 'HasDimensions', 'ParameterKind', 'PhysicalProperty', 'Position', 'Quantity', 'RobotGroup', 'RobotUnit', 'Safety', 'Wall']
RobotGroup:        properties=['description', 'id']                                   required=['id', 'description']
Activity:          properties=['description', 'id', 'offers']                         required=['offers', 'id', 'description']
Safety:            properties=['description', 'id', 'safety_barrier']                 required=['id', 'description']
HasDimensions:     properties=['height', 'length', 'weight', 'width']                 required=None
PhysicalProperty:  properties=['description', 'height', 'id', 'length', 'manufacturer', 'weight', 'width']  required=['id', 'description']
BuildingComponent: properties=['height', 'id', 'length', 'material', 'weight', 'width'] required=['id']
Wall:              properties=['height', 'id', 'length', 'material', 'thickness', 'weight', 'width'] required=['id']
RobotUnit.group  {"anyOf": [{"$ref": "#/$defs/RobotGroup"}, {"type": "null"}], ...}
RobotUnit.groups {"items": {"$ref": "#/$defs/RobotGroup"}, "type": ["array", "null"], ...}
```

With `--include-range-class-descendants`:

```
RobotUnit.group = {"anyOf": [{"$ref": "#/$defs/Activity"}, {"$ref": "#/$defs/Safety"}, {"$ref": "#/$defs/PhysicalProperty"}, {"type": "null"}], ...}
```

**`linkml-validate`**:

```
-C RobotGroup  data/group_instance.yaml (id, description, offers: [grip])
  [ERROR] ... Additional properties are not allowed ('offers' was unexpected) in /   exit 1
-C Activity    data/group_instance.yaml
  No issues found                                                                   exit 0
-C Activity    data/group_no_description.yaml (id, offers)
  [ERROR] ... 'description' is a required property in /                             exit 1
-C RobotUnit   data/unit_group_activity.yaml (group: {id, description, offers: [grip]})
  No issues found                                                                   exit 0
```

**`SchemaView`**: `induced_slot("description","Activity").required = True`; `class_ancestors("PhysicalProperty") = ['PhysicalProperty', 'HasDimensions', 'RobotGroup']`; with `mixins=False`, `['PhysicalProperty', 'RobotGroup']`; `class_descendants("RobotGroup") = ['RobotGroup', 'Activity', 'Safety', 'PhysicalProperty']`.

**Readings.**

1. The abstract class is in `$defs` and is a complete, closed object schema of its own. `-C RobotGroup` validates a document against it and rejects `offers` as an extra property. `abstract` does not stop instantiation in the JSON Schema path; the docs' "some generators may choose" is literal.
2. Children inherit slots and `slot_usage`. `Activity.required` contains `description` from the parent's `slot_usage` and `offers` from its own. Inheritance is unfolded into each child, as the `is_a` definition promises for "a framework without polymorphism".
3. A slot ranging over the abstract parent is a polymorphism trap. `gen-json-schema` by default emits `$ref: RobotGroup`, so `dist/` JSON Schema would reject an `Activity` object in `group` (it has `offers`). `linkml-validate` accepts it, because the validation plugin's `include_range_class_descendants` defaults to True (2026-09-10 note, 2.2). Two of our outputs would disagree. The fix would be to pass `--include-range-class-descendants` in `scripts/build.py`, or, simpler, never write a slot whose range is an abstract parent. The resource design's four named slots (`activity`, `physical_property`, `safety`, `operational_requirement`) already avoid it.
4. Against the brief's rule "`is_a` becomes stacked labels": with the abstract parent, every group node would carry `:RobotGroup:Activity`. The label costs nothing and would let a query touch "any group", but nothing in the brief asks for that query, and the component would also have to decide whether an abstract class gets a uniqueness constraint (it should not, or `sam100_activity` and a hypothetical `sam100_activity` Safety node would collide under one label; in practice ids are per class, so a shared parent label would make id uniqueness across the four groups a new promise). That is a rule-table question the abstract parent creates and the flat design does not.

### 3.3 Probe (b): a `HasDimensions` mixin versus reusing global slots

From the same probe: `PhysicalProperty` and `BuildingComponent` both list `length`, `width`, `height`, `weight` in their JSON Schema `properties`, once each, typed `anyOf [$ref Quantity, null]`. `HasDimensions` also lands in `$defs` as a class with four optional properties and no `id`. `gen-doc` gives it a "Mixin Usage" table listing both classes (3.4).

What a schema-level slot reused by two classes means: the slot is one global `SlotDefinition` (Q1, 1.3). Listing it under two classes gives both classes that slot with the same `range`, `multivalued`, `inlined`, `description`. `slot_usage` on either class may then set `required`, narrow the `range`, or add `minimum_value` for that class only; the other class is untouched. The mixin adds nothing to that: `HasDimensions.slots` is itself four references to the same global slots. The only things a mixin adds are (i) one line, `mixins: [HasDimensions]`, instead of four slot names, (ii) a class that documentation and the rule table must account for, and (iii) a shared place to hang a `slot_usage` that both users would get (for example `length` required on both). Our dimensions are optional in both modules, so (iii) does not arise. For the rule table, a mixin is a second kind of parent: `class_ancestors` returns it unless `mixins=False` is passed, so the component must decide whether `HasDimensions` becomes a label. The brief only decided `is_a`. Not using mixins keeps that decision from ever being needed.

### 3.4 Probe (c): how `gen-doc` renders it

`uv run gen-doc -d probes/out/docs probes/inherit_probe.yaml`. `RobotGroup.md` line 16: `* __NOTE__: this is an abstract class and should not be instantiated directly`. `Activity.md` 52-54: `## Inheritance` / `* [RobotGroup](RobotGroup.md)` / `    * **Activity**`. `PhysicalProperty.md` 89-91: `* [RobotGroup](RobotGroup.md)` / `    * **PhysicalProperty** [ [HasDimensions](HasDimensions.md)]`. `HasDimensions.md`: a "Class Properties" table with `| Mixin | Yes |` and a "Mixin Usage" table listing `PhysicalProperty` and `BuildingComponent`. `index.md` nests children under their `is_a` parent with indentation (`RobotGroup` over `Activity`, `PhysicalProperty`, `Safety`; `BuildingComponent` over `Wall`); the mixin is listed flat. Each slot row in a class page carries an "Inheritance" column reading `direct` or the name of the ancestor it came from.

One line: `gen-doc` shows `is_a` as an indented tree in the index and an "Inheritance" bullet list on the class page, mixins as a bracketed suffix on that bullet plus a "Mixin Usage" table, and `abstract` as one note line.

### 3.5 Recommendation

Kept short, one reason each.

**Resource module: none of these features.** Five concrete classes, `RobotUnit` plus the four groups, each listing `id` and its own slots from the global `slots:` block, with `slot_usage` for the per-class `required` (`offers` on `Activity`, `activity` on `RobotUnit`). Reason: the probes show an abstract parent adds a label with no instances, a rule-table question about constraints, and no validation benefit; the four named slots already make the class of every group known.

**Product module: `is_a` only, and only when needed.** `Wall is_a BuildingComponent` when `Wall` needs `thickness`; `BuildingComponent` stays concrete and instantiable. Reason: it is the one inheritance feature the rule table already handles (stacked labels `:BuildingComponent:Wall`), JSON Schema unfolds it cleanly (the `Wall` probe above), and the brief already restricts subclassing to kinds that need slots. Do not make `BuildingComponent` abstract: IFC components without a modelled kind are instances of it. Do not give any slot the range of a subclass-bearing class unless every document validates through `-C`; if a slot must range over `BuildingComponent` and accept `Wall` objects inline, build with `--include-range-class-descendants` so `dist/` agrees with the validator. Reference slots (`derived_from`, `contained_in`, the component-reference parameter) are strings and are unaffected.

**Shared dimension slots: reuse the global slots.** Declare `length`, `width`, `height`, `weight` once, in whichever module first needs them (resource, per the brief), or in common if product needs them in the same slice, and list them on each class. Reason: the generated JSON Schema is identical to the mixin version, and no class exists that the rule table has to explain.

**Avoid.** `abstract`: no validation effect (3.2, reading 1) and an empty label. `mixins`: a second parent kind for the rule table and the docs, for a saving of three lines. `union_of`: OWL generation only. `designates_type`: unnecessary because the class is always fixed by `-C` or by the slot range, and it would put a type string into every document that the component would then have to trust. Slot `is_a`: nothing in the design has two slots that specialise one another; if `SchemaView.is_inlined` ever has to follow slot ancestry, that is one more thing to explain.

---

## Could not verify

- Whether `gen-json-schema` with `--include-range-class-descendants` is what `scripts/build.py` should pass: this note only shows the default and the flag's output on the probe; the repo's build script was not changed or run.
- Whether `SchemaView.all_elements()` (used by the linter's `recommended` rule) includes the schema header itself. The probe with a schema that has a `description` did not test a header without one. Read from `rules.py` 135 only.
- The metamodel docs index page was fetched through a summarising fetch; the list of core metaclasses it shows and its one-line description are as reported by that fetch. The `meta.yaml` source is what the tables cite.
- Line numbers cite `meta.yaml` from linkml-model `main` on 2026-09-12, not the installed 1.11.1 copy (29 lines shorter). Names and definitions were checked to be present in both; installed line numbers may differ by up to 29.
- Neo4j's behaviour with a list of node references as a relationship property (2.4, "reject multivalued class-ranged slots on an edge class") is inferred from Neo4j's property-type rules, not executed; the same caveat as the 2026-09-10 note.
- The `ifabsent` default is applied by the generated dataclass at construction time; whether `linkml_runtime`'s YAML loader into that dataclass also applies it for a document lacking `status` was not run. The `gen-python` default value and the construction probe are the evidence.

## Sources consulted

Fetched 2026-09-12:

- https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/meta.yaml (3435 lines; cited by line throughout Q1 and Q3)
- https://linkml.io/linkml-model/latest/docs/meta/ (the "Core metaclasses:" list and its opening sentence)
- https://linkml.io/linkml-model/latest/docs/EnumDefinition/
- https://linkml.io/linkml/howtos/model-property-graphs.html and its source https://raw.githubusercontent.com/linkml/linkml/main/docs/howtos/model-property-graphs.md (lines 26-79, 123, 178-252, 277, 383-454)
- https://linkml.io/linkml/schemas/inheritance.html and its source https://raw.githubusercontent.com/linkml/linkml/main/docs/schemas/inheritance.md (lines 5, 34, 38, 53-61, 69-77, 109, 116-128)
- https://linkml.io/linkml/faq/why-linkml.html and its source https://raw.githubusercontent.com/linkml/linkml/main/docs/faq/why-linkml.md (lines 120-137, 413)
- https://raw.githubusercontent.com/linkml/linkml/main/packages/linkml/src/linkml/linter/cli.py (lines 16, 105-121, 140-156), `linter/linter.py` (37-40, 74-81), `linter/rules.py` (38-45, 113-149, 220-241, 368-427), `linter/config/default.yaml`, `linter/config/recommended.yaml`

Installed toolchain, `C:\Users\go25qoh\Repos\rcpc-schema\.venv\Lib\site-packages\`: `linkml` and `linkml-runtime` 1.11.1; `linkml/linter/rules.py`, `cli.py`, `config/default.yaml`, `config/recommended.yaml` (diffed against main, see 1.5); `linkml_runtime/linkml_model/model/schema/meta.yaml` (3406 lines).

Repository files read: `docs/ideas/linkml-product-process-graph-schema.md` (Recommended Direction, Decisions Taken by Default); `docs/ideas/robot-entry-as-type.md`; `SPEC-common.md` (decisions 5, 9, 10); `schema/common.yaml`; `docs/research/linkml-neo4j-and-metamodel.md` (sections 1.2, 1.6, 2.1, 2.2, 2.3); `tests/test_lint.py` (lines 12-16); `pyproject.toml`.

Probe files, all under the session scratchpad `probes/` (not in the repository): `common.yaml` (copy), `resource_probe.yaml`, `resource_probe_noinline.yaml`, `resource_probe_status_required.yaml`, `lint_bad.yaml`, `inherit_probe.yaml`, `meta_table.py`, `meta_classes.py`, `data/valid.yaml`, `data/count_zero.yaml`, `data/activity_as_string.yaml`, `data/activity_missing_description.yaml`, `data/group_instance.yaml`, `data/group_no_description.yaml`, `data/unit_group_activity.yaml`, and generated outputs under `out/` (`*.schema.json`, `resource_probe.py`, `resource_probe_pydantic.py`, `docs/`, `meta_classes.txt`).
