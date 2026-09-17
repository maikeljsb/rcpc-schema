# PDDL and HDDL as the source for the process module

Research note, 2026-09-17, replacing the draft of 2026-09-16.

## Question

What should `schema/process.yaml` look like if PDDL 2.1, HDDL, and HDDL 2.1 are treated as a genuine source of inspiration, given `common.yaml`, `product.yaml`, and `resource.yaml` as the foundation? Part 1 describes the languages. Part 2 derives, component by component, what each becomes in LinkML. Part 3 lists the changes to the foundation and the brief that follow. Part 4 lists what stays open. The brief (`docs/ideas/linkml-product-process-graph-schema.md`) is a prior input of the same standing as the three modules; where its decisions differ from what the sources give, part 2 names the difference.

## Sources

| Key | Source | How cited |
|---|---|---|
| HDDL | Höller, Behnke, Bercher, Biundo, Fiorino, Pellier, Alford. "HDDL – A Language to Describe Hierarchical Planning Problems", arXiv 1911.05499v1 (2019); published as "HDDL: An Extension to PDDL for Expressing Hierarchical Planning Problems", AAAI 2020, DOI 10.1609/aaai.v34i06.6542. Read in the arXiv version. | § and page of the arXiv version, Definition number, or grammar rule number from §4 |
| HDDL-IPC | IPC 2020 hierarchical track: HDDL addendum (github.com/panda-planner-dev/ipc2020-domains) and plan output format (ipc2020.hierarchical-task.net/data/format.pdf) | item, or format.pdf page |
| HDDL21 | Pellier, Albore, Fiorino, Bailon-Ruiz. "HDDL 2.1: Towards Defining a Formalism and a Semantics for Temporal HTN Planning", arXiv 2306.07353v1 (2023). States that it reports no syntax (§5, p. 4). | § and page, Definition number |
| HDDL21-BNF | "Annex: Full HDDL 2.1 Syntax", `bnf.tex` in github.com/pellierd/HDDL2.1, main branch. The repository README calls itself a "language proposal". Cited only to say what is proposed. | section |
| Transport | `benchmarks/Transport/domain.hddl` and `benchmarks/Transport/problem-1.hddl` in github.com/pellierd/HDDL2.1, main branch, fetched 2026-09-16. Attested syntax in this note is taken from these two files and from the examples in the HDDL paper. | file and element |
| PDDL21 | Fox, Long. "PDDL2.1: An Extension to PDDL for Expressing Temporal Planning Domains", JAIR 20 (2003) 61-124. | § and JAIR page |
| LinkML | `linkml` 1.11.1 as installed, probed 2026-09-16 with `linkml-lint`, `linkml-validate`, `gen-json-schema`. | appendix row |
| Foundation | `schema/common.yaml`, `schema/product.yaml`, `schema/resource.yaml`, their specs, and the brief, at commit `e938d82`. | file and section |

Paper quotations were taken from text extracted from the PDFs and spot-checked against that text on 2026-09-17. Not reached: the AAAI-published HDDL PDF (requirement-flag names are from the preprint and the IPC addendum) and PDDL 1.2. Nothing below depends on either.

## Part 1. What HDDL is made of

HDDL extends "the STRIPS fragment (language level 1) of the PDDL2.1 definition" (HDDL §1, p. 1) with compound tasks and methods. HDDL 2.1 adds PDDL 2.1's durative actions and numeric functions (HDDL21 §2, p. 2). The components are given in the order a domain file lists them, then the problem file, then a solution. Each is stated from the paper's definition, its grammar rule, and a line of the Transport benchmark.

### 1.1 Domain and problem

A domain is "(L, TP, TC, M)": a predicate logic, the primitive tasks, the compound tasks, and the methods (HDDL Def. 2, §2, p. 2). A problem is "(D, sI, tnI, g)": a domain, an initial state, an initial task network, and an optional goal (Def. 3). The domain is lifted and the problem grounds it: "Lifted problems are a compact representation of their ground instantiations ... we define solutions based on their grounding" (§2, p. 3). Transport keeps them in two files, `domain.hddl` and `problem-1.hddl`.

### 1.2 Types and typed parameters

Types are declared with optional supertypes, and every other list is typed: "we wanted to enforce a typed model and therefore allow for untyped elements only in the type definition" (HDDL §4, p. 7; rules 11-13, 19). A constant "can have several types, e.g. truck and vehicle to support a type hierarchy" (§2, p. 2). `either` unions primitive types and is allowed wherever a type is (rule 21; PDDL21 A.1, p. 115, without nesting). The type `object` "carries no special meaning" (HDDL-IPC item 2).

Transport:
```lisp
(:types
  location target locatable - object
  vehicle package - locatable)
```
Every parameter list in the file is typed, for instance `(:task deliver :parameters (?p - package ?l - location))`.

Numbers are not types. PDDL 2.1: "Numeric expressions are not allowed to appear as terms in the language (that is, as arguments to predicates or values of action parameters)" and "Numbers are no longer considered to be an implicit type ... This ensures that there are only finitely many ground action instances" (PDDL21 §3, p. 68; A.1, p. 115).

### 1.3 Predicates and functions

Predicates are relation schemas over typed variables (HDDL rules 15-16). Functions, from PDDL 2.1 and admitted in HDDL 2.1, are numeric, "of type Object^n → R" (PDDL21 §3, p. 68; HDDL21-BNF `:functions`). Their values are set in the problem's `:init` and read in conditions and durations.

Transport:
```lisp
(:predicates
  (road ?l1 ?l2 - location)
  (at ?x - locatable ?v - location)
  (in ?x - package ?v - vehicle)
  (has-petrol-station ?l - location)
  (ready-loading ?v - vehicle))
(:functions
  (road-length ?l1 ?l2 - location)
  (fuel-demand ?l1 ?l2 - location)
  (fuel-left ?v - vehicle)
  (capacity ?v - vehicle)
  (package-size ?p - package))
```

### 1.4 Primitive tasks: actions and durative actions

"An action a is a tuple (name, pre, eff)"; "for each task name name(a) there exists only a single action using it as its name (this way, names can be used as unique identifiers)" (HDDL §2, p. 2). The grammar reuses the task head: `(:action <task-def> [:precondition <gd>] [:effect <effect>])` (rules 42-44; the grammar spells `:effects`, the example and every file `:effect`). A durative action adds a duration and annotates every condition and effect with `at start`, `at end`, or `over all` (PDDL21 A.3, p. 117). "The duration is an implicit parameter of the durative action and must be supplied in a plan" (PDDL21 A.3, p. 118). Only primitive tasks have durations: "Only when a task t is primitive, then duration(t) is given by the duration δ of the action that achieves t" (HDDL21 §3, p. 3).

Transport, one of each:
```lisp
(:action noop
  :parameters (?v - vehicle ?l2 - location)
  :precondition (at ?v ?l2)
  :effect ())

(:durative-action drive
  :parameters (?v - vehicle ?l1 ?l2 - location)
  :duration (= ?duration (road-length ?l1 ?l2))
  :condition (and
    (at start (at ?v ?l1))
    (at start (road ?l1 ?l2))
    (at start (>= (fuel-left ?v) (fuel-demand ?l1 ?l2))))
  :effect (and
    (at start (not (at ?v ?l1)))
    (at start (at ?v ?l2))
    (at start (decrease (fuel-left ?v) (fuel-demand ?l1 ?l2)))))
```
`drive`'s duration depends on its parameters through a function; `pick-up` in the same file has a constant, `:duration (= ?duration 1)`, and uses `over all` to hold the vehicle in place for the whole action, `(over all (at ?v ?l))`. `over all` holds on the open interval; a fact needed over the closed interval takes `at start`, `over all`, and `at end` together (PDDL21 §5, p. 72).

### 1.5 Compound tasks

"A compound task is simply a task name, i.e., an atom. In contrast to primitive tasks its purpose is not to induce a state transition, but to reference a pre-defined mapping to one or more task networks by which that compound task can then be refined. They do thus not use preconditions or effects" (HDDL §2, p. 2). They are declared explicitly with typed parameters, so that a misspelt primitive is not silently read as an abstract task and so that argument types are stated rather than inferred from the methods (§3, pp. 3-4).

Transport:
```lisp
(:task deliver :parameters (?p - package ?l - location))
(:task get-to :parameters (?v - vehicle ?l - location))
(:task load :parameters (?v - vehicle ?l - location ?p - package))
(:task unload :parameters (?v - vehicle ?l - location ?p - package))
```

### 1.6 Methods

"A decomposition method m ∈ M is a tuple (c, tn, VC) consisting of a compound task name c, a task network tn, and a set of variable constraints VC" (HDDL §2, p. 2). Grammar (rules 26-30):
```
(:method <name>
  :parameters (<typed list (variable)>)
  :task (<task-symbol> <term>*)
  [:precondition <gd>]
  <tasknetwork-def>)
```
"The parameters of a method are supposed to include all parameters of the abstract task that it decomposes and those of the tasks in its network of subtasks. The separate definition of method parameters enables e.g. the restriction of the abstract task's parameters to subtypes of their original definition" (§4, p. 7). Several methods may refine one task; Transport has `m-unload` and `m-unload-and-refuel` for `unload`, and five methods for `get-to`.

Transport:
```lisp
(:method m-deliver
  :parameters (?p - package ?l1 ?l2 - location ?v - vehicle)
  :task (deliver ?p ?l2)
  :ordered-subtasks (and
    (get-to ?v ?l1)
    (load ?v ?l1 ?p)
    (get-to ?v ?l2)
    (unload ?v ?l2 ?p)))
```

On method preconditions the authors write: "The feature is somehow problematic. First, because it is (at least from our experience) usually used to guide the search and thus often breaks with the philosophy of PDDL to specify a model that does not include advice" (§3, p. 5), and of SHOP-style if-else chains that they are "advice to the planner, which should not be part of the domain description language for a domain independent planner" (§3, p. 5). The feature is kept under a requirement flag because it is widely used. Transport declares `:method-preconditions` but no method in the file has one. Where a method applies only in a certain state, Transport puts the condition on a primitive: `m-i-am-there` decomposes `get-to` into the single action `noop`, whose precondition is `(at ?v ?l2)`.

### 1.7 The task network

"A task network tn over a set of task names X is a tuple (I, ≺, α, VC)": I "a finite (possibly empty) set of task identifiers", ≺ "a strict partial order over I", α mapping identifiers to task names, VC variable constraints that "can bind two task parameters to be (non-)equal and it can constrain a task parameter to be (non-)equal to a constant, or to (not) be of a certain type" (HDDL Def. 1, §2, p. 2). Identifiers exist "because any task can occur multiple times within the same task network, but the partial order needs to be able to differentiate between them" (§2, p. 2).

Grammar (rules 31-41), shared by methods and the problem's initial network:
```
<tasknetwork-def> ::= [:[ordered-][sub]tasks <subtask-defs>]
                      [:order[ing] <ordering-defs>]
                      [:constraints <constraint-defs>]
<subtask-def>     ::= (<task-symbol> <term>*) | (<subtask-id> (<task-symbol> <term>*))
<ordering-def>    ::= (<subtask-id> "<" <subtask-id>)
<constraint-def>  ::= () | (not (= <term> <term>)) | (= <term> <term>)
```

Four facts about it:

- **Three ways to write the order**, `:ordered-subtasks`, `:subtasks` alone, and `:subtasks` with labels and `:ordering`; section 1.8 gives each with its example.
- **Labels are optional in the syntax, identifiers are not in the formalism.** Rule 36 admits both forms; Definition 1 always has I.
- **Arguments are method variables or constants.** "all variables defined in the method's parameter section may be used as parameters of the subtasks" (§3, p. 4); `<term> ::= <name> | <variable>` (rules 58-59). In `m-deliver` every subtask argument is a method parameter.
- **Constraints are (in)equalities.** "our current definition only allows for equality and inequality constraints" (§3, p. 6); the type constraint of Definition 1 has no syntax. The paper's example is `:constraints (not (= ?li ?ld))` on `m-direct` (§3, p. 6). Transport writes none.

An empty network is allowed, `:subtasks ()` (rule 35), and the paper's example of one carries a method precondition: `m-already-there` with `:precondition (tAt ?l)` and `:subtasks ()` (§3, p. 5).

HDDL 2.1 defines ordering over events: `Co` is "a set of temporal qualitative ordering constraints over the start or the end events of the tasks in I" with the point-algebra relations `<, ≤, >, ≥, =, ≠` (HDDL21 Def. 6, §2, p. 3). The paper gives no syntax; the annex proposes `(< (end t1) (start t2))` (HDDL21-BNF, Ordering). Transport orders whole tasks only.

### 1.8 Writing the order: `:ordered-subtasks` and `:subtasks`

The task network of 1.7 has three surface forms for the same partial order ≺, and HDDL files use all three. The grammar admits them through one rule, `[:[ordered-][sub]tasks <subtask-defs>]` (rule 32), so the keyword chosen says how ≺ is to be read.

**Total order, `:ordered-subtasks`.** "When the :ordered-subtasks keyword is used, the given list of subtasks is supposed to be totally ordered" (HDDL §3, p. 4). The list order is ≺; no labels and no `:ordering` block. Transport writes its main method this way:
```lisp
(:method m-deliver
  :parameters (?p - package ?l1 ?l2 - location ?v - vehicle)
  :task (deliver ?p ?l2)
  :ordered-subtasks (and
    (get-to ?v ?l1)
    (load ?v ?l1 ?p)
    (get-to ?v ?l2)
    (unload ?v ?l2 ?p)))
```

**No order, `:subtasks` without `:ordering`.** The occurrences may run in any order or interleave. Transport:
```lisp
(:method m-unload-and-refuel
  :parameters (?v - vehicle ?l - location ?p - package)
  :task (unload ?v ?l ?p)
  :subtasks (and
    (drop ?v ?l ?p)
    (refuel ?v ?l)))
```
The file's own comment on it: "They can be done in whatever order (even in paralell?)".

**Partial order, `:subtasks` with labels and `:ordering`.** "In the other cases, ordering relations may be defined explicitly. This is done by including ids into the task definition that can then be referenced in the ordering definition ... The ordering constraints are defined via the task ids. They have to induce a partial order" (§4, p. 7). The paper's example (§3, p. 5):
```lisp
(:method m-drive-to-via
  :parameters (?li ?ld - location)
  :task (get-to ?ld)
  :subtasks (and (t1 (get-to ?li)) (t2 (drive ?li ?ld)))
  :ordering (and (t1 < t2)))
```
Why the paper adds this form beside SHOP's nested ordered and unordered lists: "Consider an ordering over five task identifiers t1,...,t5, where t1 < t4, t2 < t4, t2 < t5, and t3 < t5. This ordering cannot be expressed with SHOP's nested ordered/unordered constructs" (§3, p. 5). Transport has no method in this form; HDDL 2.1's annex keeps the form and adds event decorations to the ids (1.7).

**Infix in the paper, prefix in the tools.** The paper's grammar writes the pair as `(<subtask-id> "<" <subtask-id>)`, `(t1 < t2)` (rule 39). The IPC 2020 domains and the parsers that read them write `(< t1 t2)`, and the HDDL 2.1 annex does the same (`(<d-task> <task-id> <task-id>)`, HDDL21-BNF, Ordering). Appendix B.4 records a parser rejecting the infix form. An exporter writes the prefix form.

**The three forms are interchangeable.** A total order is a partial order with every pair stated, so `m-deliver` could be written in the third form with three constraints and labels, and a network with no ordering is the third form with an empty `:ordering`. Appendix B shows the same method written once with `:ordered-subtasks` (B.1) and once, from a document that carries pairs, in the labelled form with a fifth unordered step (B.4); both solve. Which form a document shape can produce is therefore a question of convenience for the author and the exporter, not of expressiveness: only the third form can write the five-task order above, and it can write everything the other two can.

### 1.9 The problem: objects, initial state, initial task network, goal

Grammar (rules 70-84): `:objects`, an optional `:htn` block that reuses `<tasknetwork-def>` with an optional `:parameters` list, `:init`, and an optional `:goal`. "Since a state-based goal definition is often not included in HTN planning, we made the goal definition optional" (§4, p. 8). The initial network "may not necessarily be ground" (Def. 3). Its arguments "have to be defined as constants in s0 or in a dedicated parameter list" (§4, p. 7).

Transport problem-1, condensed:
```lisp
(:objects
  city-loc-0 city-loc-1 city-loc-2 - location
  truck-0 - vehicle
  package-0 package-1 - package)
(:htn
  :tasks (and
    (deliver package-0 city-loc-0)
    (deliver package-1 city-loc-2))
  :ordering ( )
  :constraints ( ))
(:init
  (road city-loc-0 city-loc-1)
  (= (road-length city-loc-0 city-loc-1) 22)
  (at package-0 city-loc-1)
  (= (package-size package-0) 23)
  (at truck-0 city-loc-2)
  (ready-loading truck-0)
  (= (capacity truck-0) 100))
```
The two `deliver` tasks are unordered, so, in the paper's words on its identical example, "their subtasks may be executed interleaved" (HDDL §3, p. 6). There is no `:goal`.

### 1.10 A solution

"Informally, solutions are executable, ground, primitive task networks that can be obtained from the problem's initial task network via applying decomposition methods, adding ordering constraints, and grounding" (HDDL §2, p. 3). Decomposition replaces one identifier by the method's network and passes every ordering the removed task had onto the inserted tasks (Def. 5, §2, p. 3). The paper defines no output format. The IPC 2020 format, "not part of the HDDL standard" (format.pdf, p. 1), writes a solution as primitive lines `<id> <action> <args>`, a `root <ids>` line, and one decomposition line per compound, `<id> <task> <args> -> <method> <child ids>` (format.pdf, pp. 1-2). A PDDL 2.1 plan step is `t:(name args)[d]`, the chosen duration in brackets (PDDL21 §7.1, p. 91).

### 1.11 What the papers say beyond the grammar

- **Physics, not advice.** PDDL 2.1 follows McDermott's maxim that a language "should focus on expressing the physical properties of the world, not advice to the planner" (PDDL21 §1, p. 62). HDDL applies it to method preconditions (1.6) and to method effects, which it drops (§3, p. 6).
- **Requirements flags.** A domain declares the features it uses; Transport declares `:method-constraints :numeric-fluents :timed-initial-literals :durative-actions :method-preconditions :negative-preconditions :hierarchy :typing`.
- **Time.** HDDL 2.1 uses integer dates, because "using rationals without adding further conditions can yield to an undecidable planning problem" (HDDL21 footnote 4, p. 3).

## Part 2. What each component becomes in `process.yaml`

Same order as part 1. Each entry says what the foundation already provides, what LinkML shape the component takes, what is recommended and on what basis, and where a prior brief decision differs. "Probe" refers to the appendix.

### 2.1 Domain and problem

Foundation. `product.yaml` and `resource.yaml` documents are the problem's `:objects` and `:init` (2.2, 2.3). The brief's "catalogue" is the domain; its "instance side" is the problem plus the solution.

Shape. Catalogue classes for 1.4 to 1.7 in `process.yaml`. Two ground classes for 1.9 and 1.10, one per catalogue task class, each pointing at its definition and carrying bindings. A ground compound with no method and no children is an initial task, `:htn`; with them it is a decomposed one, a plan line. The IPC line `<id> <task> <args> -> <method> <child ids>` fixes what the ground compound carries: task, bindings, method, children.

Recommendation. Two ground classes as above, with `children` on the ground compound. Basis: the IPC format for the slot list; placing `children` on the parent is this note's reading of HDDL's one `<tasknetwork-def>` for methods and the initial network, not a statement in a source. Names are open (part 4).

### 2.2 Types and typed parameters

Foundation. The object types are the identified classes: `BuildingComponent` with `Connector is_a` it, `Space`, `Storey`, `RobotUnit` and its machine nodes, `CapabilityType`. `common.ParameterKind` is the type vocabulary for parameters; its values are `position`, `component_reference`, `quantity`.

Shape. A keyed `ParameterDeclaration` class, key the parameter name, one slot for the kind. Probe: a keyed class with one other slot validates in the one-line form `parameters: {to: space}`, which reads as `?to - space`, and in the full form `{to: {parameter_kind: space}}`; the list form is rejected unless the slot says `inlined_as_list`. Slot names `name` and `kind` belong to product in the merged schema, so the declaration's slots need other names.

Recommendation. `ParameterKind` becomes object kinds: `component`, a reference to a `BuildingComponent` or subclass, and `space`, a reference to a `Space`; `position` and `quantity` leave the enum. Basis: PDDL forbids numbers as parameter values (1.2), and the foundation holds the positions and quantities a task needs as functions of objects (2.3): a component's `target_location`, `supply_location`, `current_location`, `weight`; a robot's `load_capacity`, `precision`. Every parameter is then a reference, so it projects as an edge and is existence-checked at tier 2. A `Space` has no coordinates today, so a leaf handed a `Space` has a node, not a point; that belongs to the derivation slice.

Brief difference. The brief's checked assumption "a closed set of parameter kinds covers every primitive in the reference" was checked with `position` and `component_reference` (`parameter-kinds-mapping.md` §1). It still holds, with different kinds. The same note's §2 item 4 excludes a resource reference as a kind, and the brief binds the robot through a special slot, `assigned_unit`. In Transport the vehicle is an ordinary parameter threaded through `deliver`, `m-deliver`, and every action (1.5, 1.6). HDDL Def. 3 lets a network stay unground until later, so a robot parameter bound at stage two is within the formalism. Adding `robot` as a kind would make every binding one construct and let a method say two subtasks use one robot by repeating the variable; keeping `assigned_unit` keeps the brief's decision as written. Left as a question (part 4).

### 2.3 Predicates and functions

Foundation. Every reference and enum slot is a predicate: `located_in`, `contained_in`, `connects`, `derived_from`, `part_of`, `offers`, `status`, `permanence`, `material`. Every `Quantity`, `Position`, or `Interval` slot is a function value, `(= (weight c) 12.5)`; a `Position` is three functions, which is the flattening rule `target_location_x_coord`. Transport's `(>= (capacity ?v) (package-size ?p))` has both operands in the foundation: `load_capacity` on `PhysicalProperty`, `weight` on `BuildingComponent`.

Shape. Nothing in `process.yaml`. Comparisons across them are the planner's or a tier 3 query's.

Recommendation. No process slot for any predicate or function the foundation holds. Basis: the foundation. The brief's Capacity kind is such a comparison and belongs in `CHECKS.md` when specified. No brief difference.

### 2.4 Primitive tasks

Foundation. `CapabilityType` in common; `Quantity` for the duration.

Shape. `PrimitiveTask` with `id`, the action name; `parameters`, the keyed map of 2.2; `requires`, a multivalued reference to `CapabilityType`, the one condition the model states; `duration`, an inlined `Quantity`; `description`. No precondition or effect slots: the brief defers effects and component state, and the sources place them in a formula language the brief excludes. `requires` is the `over all` condition `(over all (offers ?r <capability>))` that the export in `robot-entry-as-type.md` writes; the `free` lock there is the export's.

Recommendation. As above, `duration` required. Basis: HDDL 2.1 puts durations on primitive tasks only (1.4), and every Transport primitive but `noop` carries one. Limit to record: `(= ?duration (road-length ?l1 ?l2))`, a duration depending on the parameters, has no expression in a `Quantity`; the model states one value per primitive. The action name is the BT leaf's registration name, so `id` keeps the pattern `^[A-Za-z][A-Za-z0-9]*$`. No brief difference.

### 2.5 Compound tasks

Shape. `CompoundTask` with `id`, `parameters` as in 2.2, `description`. Nothing else, as 1.5 says.

Recommendation. Parameters declared, and a tier 2 check that every subtask's arguments match its task's declared parameters in number and kind. Basis: HDDL's argument for explicit declarations (1.5). Primitive and compound ids share one namespace, since a method's network is "over the names TP ∪ TC" (HDDL Def. 2); tier 2 checks that no name is both. No brief difference.

### 2.6 Methods

Foundation. `MaterialName` in common joins product's `material` to the method's applicability.

Shape. `Method` with `id`; `task`, a reference to `CompoundTask`, HDDL's `:task`; `parameters`, the keyed map of 2.2; `subtasks` and `ordering` (2.7); `description`. Applicability: the brief's `applies_to`, a list of material strings, is HDDL's type constraint on a parameter (1.7, Definition 1) realised through the method's own declaration of that parameter, which HDDL says exists to restrict "the abstract task's parameters to subtypes" (1.6). Its place is therefore the method's declaration of its component parameter, an optional slot beside the kind: `c: {parameter_kind: component, applies_to: [Brick]}`. On the method it is ambiguous once a method has two component parameters.

Recommendation. Applicability on the parameter declaration. Basis: HDDL §4, p. 7 and Def. 1. Brief difference: the brief's default puts `applies_to` on `Method`; the list and its matching by membership are unchanged, only the place moves.

No method preconditions and no method effects. Basis: 1.6 and 1.11; the brief agrees.

`subtasks` required with at least one. Basis: HDDL allows an empty network but its example gives it meaning through a method precondition, which is excluded here, and Transport writes the "already there" case as a `noop` primitive with a precondition (1.6). Brief difference: the brief's tier 3 example "a method has an empty network without declaring it" presumes a declaration that does not exist; replace it.

### 2.7 The task network

Shape. Three classes.

`Subtask`, identified: `id`, the HDDL `<subtask-id>`; the task it stands for; `arguments`. Basis for identification: Definition 1 always has identifiers (1.7). The task is a `PrimitiveTask` or a `CompoundTask`, and no parent class is allowed in this schema set. Probe: an `any_of` range renders as two strings and checks nothing; two reference slots with an `exactly_one_of` rule reach tier 1 when the rule carries a precondition, and do not when it carries none. Recommendation: two slots plus the rule. Basis: probe.

`ArgumentBinding`, keyed by the parameter name of the referenced task, one string value: a method parameter name or an object id. Basis: 1.7, arguments are method variables or constants. Tier 2 resolves which and checks that `Method.parameters` covers every variable used.

`OrderingConstraint`, a class marked `represents_relationship`, no identifier, two slots `before` and `after` with `relational_role` SUBJECT and OBJECT over `Subtask`, meaning `before` ends before `after` starts. Probe: such a class lints, validates, and renders as a plain object. Recommendation: whole-task ordering, HDDL's `(t1 < t2)`. Basis: both HDDL grammars order whole tasks and Transport does too; ordering over start and end events is HDDL 2.1's Definition 6 with a proposed syntax no benchmark uses (1.7). Two optional event slots or an operator slot are additive later. Brief difference: the brief's default "ordering is over start and end events from the start" is reversed. Name: the sources call the construct an ordering constraint; the map's `Precedence` is the retired reference's word for a narrower relation.

Total order. Transport writes total orders with `:ordered-subtasks` and nothing else; the explicit form needs a constraint per pair. The sources treat both as first-class. A flag whose edges the component derives from list order would be a rule keyed on a named slot, which the brief reserves for `count`; the explicit form needs no rule. Recommendation: the explicit form. Basis: the brief's own projection rule, not the sources, which are indifferent.

Constraints, `(not (= ?a ?b))`: not needed by the brief's examples; a `ParameterConstraint` class later.

Acyclicity: "have to induce a partial order" is a whole-network property, tier 3.

### 2.8 The problem side

Shape. The two ground classes of 2.1. Bindings: one keyed class, key the parameter name, one value slot per kind, exactly one filled. Probe: the exactly-one rule fires in list form or when its precondition names a slot that stays inside the object; in a dict-form map the key is lifted out, so a precondition on it never fires. Under 2.2 every value is a reference, so a single reference slot would do if the kind is read from the declaration at tier 2.

Ordering among roots and among children. Transport authors ordering between the initial tasks, `:ordering ( )`, and no HDDL file writes ordering among a decomposition's children; Definition 5 derives it from the method (1.10). Whether ground documents carry the derived copy is open (part 4).

Required keys. The catalogue is hand-authored; the ground side is planner output. Product adopted required-everywhere for pipeline output. Recommendation: the same split here. Basis: this note's reading; the sources say nothing about document shape.

The robot binding. Under the brief, `assigned_unit` on the ground primitive, range `RobotUnit`, pointing at a machine id that the `count` expansion yields and no document holds; checked at tier 2 against the expanded ids. Under the alternative in 2.2, the same value is the binding of a `robot` parameter. Either way the check is tier 2.

Example. The instance example names ids from `examples/product/` and machine ids from `examples/resource/`, since those documents are the objects. Basis: this note's reading of 2.1.

### 2.9 A solution

Shape. The ground primitive may carry the planned duration, PDDL's `[d]`, beside the catalogue's value. Basis: PDDL21 §7.1 by analogy; no HDDL source speaks to a document carrying it. The IPC decomposition line is the ground compound of 2.1.

### 2.10 Beyond the grammar

No `:goal`: the parentless ground compounds are the problem statement (1.9). No `:requirements`: the schema declares what it supports. No effects, no state preconditions, no formula language: physics in the documents, comparisons in queries (1.11). Integer time: `Quantity` is a float; an exporter rounds.

## Part 3. Changes to the foundation and the brief

Derived from part 2. "Decided by the sources" means a passage or a probe settles it; the rest are this note's recommendations.

**common**
1. `ParameterKind` leaves common for process (part 4, question 7); its values are `component`, `location`, `robot` (question 4). `dist/common.schema.json` and `docs/model/common/` regenerate; no document uses a kind yet.
2. Nothing else changes in common.

**capability map**
3. `Precedence` leaves the process row; under part 4 question 8 ordering is a property of the method and no class replaces it. The row names every class (question 6).

**brief**
4. Domain Structure: add that the catalogue is the HDDL domain, product and resource documents are the problem's objects and initial state, parentless ground compounds are the initial task network, and the rest of the instance side is the decomposition tree (2.1). The path stays `Method` to `PrimitiveTask`, one edge per subtask carrying its position (question 8).
5. Decisions Taken by Default, "Ordering is over start and end events from the start": reversed to whole-task ordering (2.7). Decided by the sources.
6. Decisions Taken by Default, "Method applicability is `applies_to`": the list moves from the method to the method's component parameter declaration (2.6). Decided by the sources.
7. Error Tiers: replace "a method has an empty network without declaring it" with "a subtask lists too few parameters for its task, or one that is neither a method parameter nor an object" (2.6).
8. Preconditions as Relation Kinds, "Acts on component": the pattern is a parameter of an object kind (2.2); Capacity is a function comparison (2.3).
9. Key Assumptions: the parameter-kinds item is reopened and answered by this note.
10. Decisions Taken by Default, "Stage-two allocation is one edge, `assigned_unit`", becomes the `robot` parameter's binding on the `PrimitiveTaskInstance` (question 3).

**product, resource**
None. Product's three location slots are what lets positions leave the parameter kinds; resource's `offers`, `status`, and CRS quantities are the predicates and functions the export reads.

## Part 4. Open questions

1. What are the ground classes called? **Decided 2026-09-17.** `PrimitiveTaskInstance` and `CompoundTaskInstance`. Neither HDDL's "ground" nor the brief's "instantiated" was taken; the suffix says the record is one occurrence of the catalogue task it points at.
2. Do ground documents carry ordering constraints among a compound's children, or does the component derive them from the method? **Decided 2026-09-17, following HDDL.** Ground documents carry ordering constraints only between root tasks, as the `:htn` block does. A compound's children take their order from the method the compound points at, by HDDL Def. 5; no copy is written, so nothing can drift.
3. Does the robot become a parameter kind, bound at stage two, replacing `assigned_unit`? **Decided 2026-09-17.** Yes. `robot` is a parameter kind whose value is a machine id such as `sam100_1`; every primitive declares its robot parameter and a method threads one variable to every subtask that must use the same robot. The planner binds it, and stage two may rewrite it with another machine of the same entry; a method's variable is bound once on the ground compound and its children inherit it. There is no separate `assigned_unit` slot. Allocation stays capability-based for now; robot-dependent durations and quality-based choice are later additions whose facts resource already holds (`speed`, `productivity`, `load_capacity`). Tier 2 checks the value against the machine ids the component derives from the entry id and `count`.
4. Is `position` kept as a third kind for a waypoint no object owns, or do `component` and `space` suffice (2.2)? **Decided 2026-09-17.** The kinds are `component`, `location`, and `robot`; `position` and `quantity` leave the enum. `location` ranges over `Space` for now and is named so that a finer location object can join later without renaming the kind. Every position a primitive reads is a slot on the component; every quantity is a fact on the robot or the component.

    Recorded with it, on method variables. A method declares every variable its subtasks use, a superset of the parameters of the task it decomposes, as HDDL §3, p. 4 requires and its own `m-deliver` shows with `?lp`; tier 2 checks the declaration. Variables the task does not hand down, `?lp` there and `?from` here, are given values by the planner, which grounds them and keeps the groundings in which the subtasks' preconditions hold against the state (HDDL §2, pp. 2-3; Def. 4 and 6). Our primitives carry no precondition but `requires`, so an HDDL export of the catalogue binds `?r` through `offers` and could bind `?to` through `located_in`, but has nothing to bind `?from`. This is a limit on the export until the component-state kind gives primitives an `at` relation, not a gap in the schema, which stores whatever the planner bound.
7. Does anything move into common? **Decided 2026-09-17.** No. The parameter declaration and binding classes stay in process, their only consumer. `ParameterKind` moves out of common into process for the same reason: nothing else reads it, and its values `component`, `location`, `robot` name classes common cannot see. Common loses the enum and gains nothing; part 3 items 1 and 2 are superseded by this.

5. Do process classes carry `record_type`, as product's do? **Decided 2026-09-17.** Yes, on every process class, reusing the slot product declares; LinkML locks its value to each class's own name. The brief's inheritance policy, no `designates_type`, is thereby reversed for process as it was for product.
8. Is an occurrence in a method a node of its own, and if so, does it point at a shared definition of its primitive task? **Decided 2026-09-17: B.** The occurrence is an entry inside the method: `Method` holds `subtasks` as an ordered list, each entry a task name followed by its parameter sequence, as HDDL's `(t1 (move ?r ?l0 ?from))` with the position standing for the id, and `ordering` as a list of position pairs, `[[1, 2], [2, 3], [3, 4]]`, a property of the method: `rep_b.yaml` in B.3 exactly. `Subtask` is the entry class, without key or identifier; the brief's rule for unkeyed lists changes so that the position is the key, and the entry is flattened onto the method and is not a node. There is no `OrderingConstraint` class: `ordering` is an array slot of two dimensions, the only LinkML construct that admits a list of pairs (Appendix A). Tier 1 then checks only that it is a list; that each pair names two existing positions is a tier 2 check. The projection rule table has no case for an array slot yet and needs one, since a Neo4j property holds flat lists only. One hop from `Method` to the task it uses, two parallel edges when the same task occurs twice, told apart by position. `rep_b.yaml` validates against a LinkML schema of this shape (Appendix A). Planning is indifferent to all three shapes (B.4), so the choice rests on the graph alone. Not taken: A, the occurrence as a `Subtask` node pointing at a shared `PrimitiveTask` node with ordering as edges between occurrences; C, the occurrence as the primitive node itself with no shared definition record. Consequences: ordering between root instances in a ground document, HDDL's `:htn`, can take the same shape, a keyed list of entries referencing `CompoundTaskInstance`s and an `ordering` map, so no second form is needed; every export writes the explicit labelled form with ids `t1` to `tn` made from the positions, as B.4 does; the definition of each primitive stays a shared `PrimitiveTask` record, as under A.

6. Is the capability map row amended for `ParameterDeclaration`, `ArgumentBinding`, the binding class, and `OrderingConstraint`, or left as a summary? **Decided 2026-09-17.** The row names every class, as the product and resource rows do: `PrimitiveTask`, `CompoundTask`, `Method`, `Subtask` as its list entry (question 8), `PrimitiveTaskInstance`, `CompoundTaskInstance`, the keyed `Parameter` class, and the `ParameterKind` enum. A subtask's parameters are a plain list of strings, HDDL's parameter sequence, so no class carries them; tier 2 checks the count and each entry against the task's declaration. `Precedence` leaves the row and no ordering class replaces it (question 8). The common row loses `ParameterKind`.

## Appendix A. LinkML probes

`linkml` 1.11.1, 2026-09-16, throwaway schema in the session scratchpad.

| Construct | Result |
|---|---|
| Keyed class (`key: true`) with one other slot, dict form `parameters: {target: position}` | Validates; JSON Schema renders `additionalProperties: anyOf [class, enum]`, LinkML's SimpleDict form |
| Same class, list form, no `inlined_as_list` | Rejected: "is not of type 'object'" |
| Slot with `any_of` two class ranges | Lints and validates; renders `anyOf [string, string]`; checks nothing a single reference slot does not |
| Class rule `exactly_one_of` over two reference slots, no precondition | Renders `then` with no `if`; both-set and none-set documents pass |
| Same rule with precondition `id: required` | Both-set fails "valid under each of", none-set fails "not valid under any"; renders `if`/`then`/`oneOf` |
| Same rule on a keyed class in a dict-form map, precondition on the key slot | Never fires: the key is lifted out of the object |
| `represents_relationship: true` class with two `relational_role` slots and no identifier | Lints, validates, renders a plain object |
| Slot with `array: {exact_number_dimensions: 2, dimensions: [{alias: pair}, {exact_cardinality: 2}]}`, range string, for `ordering: [[t1, t2], [t2, t3]]` (2026-09-17) | Validates. So do a triple, a flat list of strings, and integer pairs: the generator emits `items` of any type and says so, "this is currently too lax, in that it will validate ANY array" (jsonschemagen.py, linkml issue 2188). A bare string is rejected. A dimension written `{}` is rejected by the YAML loader, "Empty list elements are not allowed" |
| Ordinary `multivalued: true` string slot given `[[t1, t2]]` | Rejected: "is not of type 'string'" |
| `rep_b.yaml` (B.3) against a schema of its shape: `subtasks` an unkeyed `inlined_as_list` class whose `parameters` is a multivalued string slot, the method's `parameters` a keyed class in dict form, `ordering` the array slot above with range integer (2026-09-17) | "No issues found"; a copy with a list where `primitive_task` wants a string and a bare string for `ordering` is rejected, as is a map written where the subtask's parameter list belongs |

## Appendix B. Experiment: does planning need `Subtask` as a record of its own?

Run 2026-09-17 in the session scratchpad. Question: part 2.7 makes `Subtask` an identified record because ordering constraints must point at an occurrence. Does anything on the planning side need that, or is it only a graph concern? Method: write one method in two document shapes, export both to an HDDL `:method` block with one script, diff the outputs, and solve the resulting domain with an HTN planner. Planner: Aries through `unified-planning`, installed for the run with `uv run --with "unified-planning[aries]"`, the same route `robot-entry-as-type.md` used. Domain follows the user's framing: the material prefab selects the compound task `prefab`, refined by `m-prefab`.

### B.1 Domain and problem

`domain.hddl`, with the method in its first, totally ordered form:
```lisp
(define (domain construction)
  (:requirements :hierarchy :typing :negative-preconditions)
  (:types component location robot - object)
  (:predicates
    (at-robot ?r - robot ?l - location)
    (at ?c - component ?l - location)
    (holding ?r - robot ?c - component)
    (target ?c - component ?l - location)
    (placed ?c - component))

  (:task prefab :parameters (?c - component))

  (:method m-prefab
    :parameters (?c - component ?r - robot ?l0 ?from ?to - location)
    :task (prefab ?c)
    :ordered-subtasks (and
      (move ?r ?l0 ?from)
      (attach ?r ?c ?from)
      (move ?r ?from ?to)
      (detach ?r ?c ?to)))

  (:action move
    :parameters (?r - robot ?from ?to - location)
    :precondition (at-robot ?r ?from)
    :effect (and (not (at-robot ?r ?from)) (at-robot ?r ?to)))

  (:action attach
    :parameters (?r - robot ?c - component ?l - location)
    :precondition (and (at-robot ?r ?l) (at ?c ?l))
    :effect (and (holding ?r ?c) (not (at ?c ?l))))

  (:action detach
    :parameters (?r - robot ?c - component ?l - location)
    :precondition (and (at-robot ?r ?l) (holding ?r ?c) (target ?c ?l))
    :effect (and (not (holding ?r ?c)) (at ?c ?l) (placed ?c))))
```
`problem.hddl`:
```lisp
(define (problem prefab-wall) (:domain construction)
  (:objects wall1 - component  r1 - robot  base depot site - location)
  (:htn :tasks (and (prefab wall1)) :ordering ( ) :constraints ( ))
  (:init (at-robot r1 base) (at wall1 depot) (target wall1 site)))
```
`(target wall1 site)` stands for product's `located_in`; `(at wall1 depot)` for the space of `supply_location`. Without them `?to` and `?from` would be free, as part 4 question 4 records.

### B.2 Solver

`solve.py`:
```python
import sys
from unified_planning.io import PDDLReader
from unified_planning.shortcuts import OneshotPlanner, get_environment
get_environment().credits_stream = None
d, p = sys.argv[1], sys.argv[2]
problem = PDDLReader().parse_problem(d, p)
print("kind:", problem.kind.features)
with OneshotPlanner(problem_kind=problem.kind) as planner:
    print("planner:", planner.name)
    res = planner.solve(problem)
    print("status:", res.status)
    if res.plan is not None:
        print(res.plan)
```
Output for `domain.hddl`, `problem.hddl`:
```
kind: {'HIERARCHICAL', 'FLAT_TYPING', 'TASK_ORDER_TOTAL'}
planner: aries
status: PlanGenerationResultStatus.SOLVED_SATISFICING
Hierarchical SequentialPlan:
    move(r1, base, depot)
    attach(r1, wall1, depot)
    move(r1, depot, site)
    detach(r1, wall1, site)
```
`?r`, `?l0`, `?from`, `?to` were bound by the preconditions against the initial state; the task handed the method only `?c`.

### B.3 The three document shapes

B.1 wrote the method in the `:ordered-subtasks` form with four steps, to get a solvable baseline. From here on the method has a fifth step, `report`, unordered with respect to the rest, so that the order is partial and the labels have work to do; and the exporter always writes the labelled `:subtasks` form with `:ordering` pairs, because that is what a document carrying ordering as pairs can produce (section 1.8).

`rep_a.yaml`, representation A: `Subtask` records with ids and ordering records pointing at them:
```yaml
methods:
  - id: m_prefab
    task: prefab
    parameters: {c: component, r: robot, l0: location, from: location, to: location}
    subtasks: [m_prefab_t1, m_prefab_t2, m_prefab_t3, m_prefab_t4, m_prefab_t5]
    ordering:
      - {before: m_prefab_t1, after: m_prefab_t2}
      - {before: m_prefab_t2, after: m_prefab_t3}
      - {before: m_prefab_t3, after: m_prefab_t4}
subtasks:
  - {id: m_prefab_t1, primitive_task: move,   parameters: [r, l0, from]}
  - {id: m_prefab_t2, primitive_task: attach, parameters: [r, c, from]}
  - {id: m_prefab_t3, primitive_task: move,   parameters: [r, from, to]}
  - {id: m_prefab_t4, primitive_task: detach, parameters: [r, c, to]}
  - {id: m_prefab_t5, primitive_task: report, parameters: [r]}
```
`rep_b.yaml`, representation B: no `Subtask` records; the method holds `subtasks` as an ordered list of occurrences, each a task name followed by its parameter sequence, as HDDL writes `(move ?r ?l0 ?from)`, and the ordering as pairs of list positions. Both shapes keep HDDL's word `subtasks`; A lists ids of records, B lists the occurrences themselves. Both are the lifted method as it sits in the catalogue, the input to planning, not its result:
```yaml
methods:
  - id: m_prefab
    task: prefab
    parameters: {c: component, r: robot, l0: location, from: location, to: location}
    subtasks:
      - {primitive_task: move,   parameters: [r, l0, from]}
      - {primitive_task: attach, parameters: [r, c, from]}
      - {primitive_task: move,   parameters: [r, from, to]}
      - {primitive_task: detach, parameters: [r, c, to]}
      - {primitive_task: report, parameters: [r]}
    ordering: [[1, 2], [2, 3], [3, 4]]
```

`rep_c.yaml`, representation C: every occurrence is its own primitive node. The node carries the task name as a plain value and its own bindings, and points at the nodes that follow it, so ordering is an edge from node to node. No shared record for `move` exists; the two `move`s are two nodes. Where the definition of `move` lives, its parameter kinds, precondition, effect and duration, is not settled by this shape; the exporter below takes it from the `ACTION_PARAMS` table for all three shapes:
```yaml
methods:
  - id: m_prefab
    task: prefab
    parameters: {c: component, r: robot, l0: location, from: location, to: location}
    subtasks: [m_prefab_t1, m_prefab_t2, m_prefab_t3, m_prefab_t4, m_prefab_t5]
primitives:
  - {id: m_prefab_t1, name: move,   parameters: [r, l0, from], before: [m_prefab_t2]}
  - {id: m_prefab_t2, name: attach, parameters: [r, c, from],      before: [m_prefab_t3]}
  - {id: m_prefab_t3, name: move,   parameters: [r, from, to], before: [m_prefab_t4]}
  - {id: m_prefab_t4, name: detach, parameters: [r, c, to],        before: []}
  - {id: m_prefab_t5, name: report, parameters: [r],                     before: []}
```

### B.4 Exporter

`export.py`, one function for all three shapes:
```python
import sys, yaml
ACTION_PARAMS = {"move": ["r", "from", "to"], "attach": ["r", "c", "l"], "detach": ["r", "c", "l"], "report": ["r"]}

def occurrences(doc, m):
    if "primitives" in doc:  # representation C: primitive nodes carry name, bindings and what follows them
        by_id = {p["id"]: p for p in doc["primitives"]}
        occ = [{"primitive_task": by_id[i]["name"], "parameters": by_id[i]["parameters"]} for i in m["subtasks"]]
        pos = {i: n + 1 for n, i in enumerate(m["subtasks"])}
        order = [(pos[i], pos[j]) for i in m["subtasks"] for j in by_id[i]["before"]]
    elif isinstance(m["subtasks"][0], str):  # representation A: ids of Subtask records
        by_id = {s["id"]: s for s in doc["subtasks"]}
        occ = [by_id[i] for i in m["subtasks"]]
        pos = {i: n + 1 for n, i in enumerate(m["subtasks"])}
        order = [(pos[o["before"]], pos[o["after"]]) for o in m.get("ordering", [])]
    else:                # representation B: entries are the occurrences, positions are the labels
        occ = m["subtasks"]
        order = [tuple(p) for p in m.get("ordering", [])]
    return occ, order

def hddl_method(doc):
    m = doc["methods"][0]
    occ, order = occurrences(doc, m)
    params = " ".join(f"?{k} - {v}" for k, v in m["parameters"].items())
    lines = [f"(:method {m['id'].replace('_', '-')}", f"  :parameters ({params})", f"  :task ({m['task']} ?c)", "  :subtasks (and"]
    for n, o in enumerate(occ, 1):
        assert len(o["parameters"]) == len(ACTION_PARAMS[o["primitive_task"]])  # tier 2: arity
        args = " ".join(f"?{v}" for v in o["parameters"])
        lines.append(f"    (t{n} ({o['primitive_task']} {args}))")
    lines.append("  )")
    lines.append("  :ordering (and " + " ".join(f"(< t{a} t{b})" for a, b in order) + "))")
    return "\n".join(lines)

for f in sys.argv[1:]:
    print(hddl_method(yaml.safe_load(open(f))))
    print("=====")
```
Run: `uv run --with pyyaml python export.py rep_a.yaml > out_a.txt`, the same for B and C, then `diff out_a.txt out_b.txt` and `diff out_a.txt out_c.txt`. Both diffs are empty. All three produce:
```lisp
(:method m-prefab
  :parameters (?c - component ?r - robot ?l0 - location ?from - location ?to - location)
  :task (prefab ?c)
  :subtasks (and
    (t1 (move ?r ?l0 ?from))
    (t2 (attach ?r ?c ?from))
    (t3 (move ?r ?from ?to))
    (t4 (detach ?r ?c ?to))
    (t5 (report ?r))
  )
  :ordering (and (< t1 t2) (< t2 t3) (< t3 t4)))
```
A first version wrote the ordering in the paper's infix form, `(t1 < t2)` (HDDL §4, rule 39). The reader rejected it: `SyntaxError: Invalid expression in ordering, expected 'and' or '<'`. The IPC 2020 form `(< t1 t2)` is what the parser accepts and what the HDDL 2.1 annex also writes; an exporter must use it.

### B.5 Solving the partially ordered domain

`domain_partial.hddl` is `domain.hddl` with the exported method in place of the original and a `report` action with empty precondition and effect. Output:
```
kind: {'HIERARCHICAL', 'TASK_ORDER_PARTIAL', 'FLAT_TYPING'}
planner: aries
status: PlanGenerationResultStatus.SOLVED_SATISFICING
Hierarchical SequentialPlan:
    move(r1, base, depot)
    report(r1)
    attach(r1, wall1, depot)
    move(r1, depot, site)
    detach(r1, wall1, site)
```
`report` was placed second, which only the partial order allows.

### B.6 Finding

Planning does not distinguish the three shapes: the exported HDDL is identical, and the labels the partial order needs come equally from A's ids, from B's list positions and from C's node ids. The reason for `Subtask` as a record is therefore the graph alone. With A, ordering is a traversable edge between `Subtask` nodes and the path from `Method` to `PrimitiveTask` is two hops. With B, `Method -[:SUBTASK {label, arguments}]-> PrimitiveTask` is one hop, two parallel edges carry the two `move`s, and ordering becomes a property on the method, a list of label pairs, which needs an array slot and a projection rule case (Appendix A). B costs a second shape for ordering wherever the ordered things are nodes, root instances for example, where an edge class is the natural form. Part 2.7's recommendation was reopened as part 4 question 8 and decided for B there.

Shape C, every occurrence its own primitive node with ordering edges between them, `move -> attach -> move -> detach -> report`, is the catalogue given the shape the result already has: in the result every `PrimitiveTaskInstance` is a distinct record, and C makes every occurrence a distinct record in the method as well. Ordering between task names would not work, since `m-prefab` uses `move` twice and `attach -> move` would close a cycle on one node; ordering between occurrences does, which is why HDDL writes it between labels, `t1 (move ?r ?l0 ?from)` and `t3 (move ?r ?from ?to)`, never between task names (§4, p. 7). A and C both make the occurrence a node and keep the two `move`s apart by identity. They differ in one thing: under A the occurrence points at a shared `PrimitiveTask` record that defines `move` once, under C no such record exists in the document and the definition lives elsewhere, on each node or in the schema as a class. B keeps the occurrence inside the method. In the result the order between child instances is not stored under any shape but inherited from the method (Def. 5, part 4 question 2). HDDL's word for the occurrence is subtask.
