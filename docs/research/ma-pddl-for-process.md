# MA-PDDL and the multi-agent question for the process module

Research note, 2026-09-17.

## Question

Three parts. What is MA-PDDL made of? How is it used, with syntax? Does a language or planner exist that combines hierarchy, multiple agents, and time? A fourth part covers recent work that plans for several robots with PDDL and a language model. Part 5 says what this means for the one question in `docs/research/pddl-for-process.md` that raised it: whether a method must be able to say that two of its subtasks are performed by the same robot.

## Sources

| Key | Source | How cited |
|---|---|---|
| Kovács 2012 | Kovács, D. L. "A Multi-Agent Extension of PDDL3.1". Proc. 3rd Workshop on the International Planning Competition (WS-IPC 2012), ICAPS 2012, pp. 19-27. Read from the BME repository copy; grammar and example are images in the PDF and were read from rendered pages. | § and PDF page 1-9 |
| BNF 2015 | Kovács, D. L. "Complete BNF definition of MA-PDDL with privacy", CoDMAP, 2015-02-21. Internet Archive copy. | § and page |
| CoDMAP | Komenda, Štolba, Kovács. "The International Competition of Distributed and Multi-Agent Planners (CoDMAP)". AI Magazine 37(3), 2016, pp. 109-115. The competition website, Internet Archive capture of 2020-02-21, and its conversion scripts. | AI Magazine page; "website"; script name and line |
| CoDMAP files | `domains/codmap15/logistics00/` in github.com/aig-upf/universal-pddl-parser-multiagent, a mirror of the competition domains. | file name |
| MA-STRIPS | Brafman, Domshlak. "From One to Many: Planning for Loosely Coupled Multi-Agent Systems". ICAPS 2008, pp. 28-35. | page, Definition |
| Crosby 2014 | Crosby, Petrick. "Temporal Multiagent Planning with Concurrent Action Constraints". ICAPS DMAP Workshop 2014, pp. 16-24. Crosby, Jonsson, Rovatsos, "A Single-Agent Approach to Multiagent Planning", ECAI 2014: abstract only, PDF unreachable; its notation read from the aig-upf parser repository, whose README says it implements that paper. | page; file name |
| FMAP | Torreño, Onaindia, Sapena. "FMAP: Distributed Cooperative Multi-Agent Planning". Applied Intelligence 41(2), 2014; arXiv 1501.07250. | § |
| MA-HTN | Cardoso, Bordini. "A Multi-Agent Extension of Hierarchical Task Network". WESAAC 2016 preprint of the ADCAIJ 2017 article, whose site was unreachable. Cardoso, Bordini, "Decentralised Planning for Multi-Agent Programming Platforms", AAMAS 2019, pp. 799-807. | page, Listing |
| HDDLGym | La, Mon-Williams, Shah. "HDDLGym: A Tool for Studying Multi-Agent Hierarchical Problems Defined in HDDL with OpenAI Gym". arXiv 2505.22597, 2025; venue not verified. | § |
| HDDL 2.1 | Pellier, Albore, Fiorino, Bailon-Ruiz. arXiv 2306.07353, 2023. | §, Definition |
| ANML | Smith, Frank, Cushing. "The ANML Language". ICAPS KEPS Workshop 2008. | page |
| FAPE | Bit-Monnot, Ghallab, Ingrand, Smith. "FAPE: a Constraint-based Planner for Generative and Hierarchical Temporal Planning". arXiv 2010.13121, 2020. | § |
| TWOSTEP | Bai, Singh, Traum, Thomason. "TWOSTEP: Multi-agent Task Planning using Classical Planners and Large Language Models". arXiv 2403.17246 v2, 2025; venue not stated in the PDF. | § |
| LLM+P | Liu et al. "LLM+P: Empowering Large Language Models with Optimal Planning Proficiency". arXiv 2304.11477, 2023, arXiv only. | § |
| LaMMA-P | Zhang, Qin, Wang, Dong, Li. "LaMMA-P: Generalizable Multi-Agent Long-Horizon Task Allocation and Planning with LM-Driven PDDL Planner". arXiv 2409.20560 v2; project page says ICRA 2025. | § |
| PIP-LLM | Shi, Wu, Kumar, Sukhatme. "PIP-LLM: Integrating PDDL-Integer Programming with LLMs for Coordinating Multi-Robot Teams Using Natural Language". arXiv 2510.22784, 2025; venue not stated. | § |
| PLANTOR | Saccon et al. "Combining Large Language Models and Symbolic Reasoning for Multi-Robot Temporal Planning through Explainable Knowledge Bases". arXiv 2502.19135 v2; venue not verified. | § |
| T-HTN | Parimi, V. "T-HTN: Timeline based HTN Planning for Multi-Agent Systems". CMU Robotics Institute Master's thesis, 2021. Not peer reviewed. | chapter |

Quotations were taken from text extracted from the PDFs and spot-checked against that text on 2026-09-17. Not reached: the live CoDMAP site, the ADCAIJ 2017 full text, the ECAI 2014 PDF, FMAP's syntax report, Aries' documentation. Nothing below depends on them beyond what is marked.

## Part 1. What MA-PDDL is made of

MA-PDDL is one optional requirement added to PDDL 3.1, designed to be "a new, additional, optional extension (a PDDL-requirement), not a completely new language" and "in accordance with the design philosophy of the language, i.e. neutrally expressing the 'physics' of the domain and including no advice for planners" (Kovács 2012 §2.3, p. 5). It has five parts.

### 1.1 Agents are objects with associated actions

"A new :multi-agent PDDL-requirement is introduced to indicate the presence of multiple agents in the domain. Agents are considered objects (or constants) that may have associated actions, goals and utilities (metric definitions)" (§3.1, p. 5). There is no agent declaration: "those and only those objects are considered agents, which have at least one associated action-schema" (§3.1, p. 5).

### 1.2 An action names its agent

One optional field is inserted in the action head, and the same in the durative action head:
```
<action-def> ::= (:action <action-symbol>
                   [:agent <agent-def>]
                   [:parameters (<typed list (variable)>)]
                   <action-def body>)
<agent-def>  ::= <name> | <variable> | <type> | <variable> - <type>
```
(§3.1, p. 5; durative form p. 6.) "If a type or a variable is given, then the action-schema is associated to every object whose type is a subset of the given type or the type of the variable." The agent variable "may appear in the body of the action-schema (in conditions and effects) just like any other action-parameter" (§3.1, p. 5). Actions are inherited down the type hierarchy and can be redefined for subtypes, "polymorphism" (§3.1, pp. 5-6).

### 1.3 Concurrency is a precondition about another agent's action

An action formula may appear anywhere a goal description may:
```
<GD> ::= <action formula(term)>
<GD> ::= (not <action formula(term)>)
<action formula(t)> ::= (<action-symbol> t t*)
```
"The first argument (term) should be always the agent executing the referenced action ... If during execution a grounded reference to an action A needs to be positive for the conditions of a grounded action B to hold, then this means that A needs to be executed in parallel with B for B's respective effects to take place. Otherwise, if the grounded reference to A needs to be negative ... then A should not be executed in parallel with B" (§3.1, p. 6). A built-in `num` counts concurrently executing actions matching a pattern (§3.1, p. 6). This generalises Boutilier and Brafman's concurrent action lists (§3.1, p. 6). For durative joint actions, consistency "should focus on the exact time instants and intervals when (pre)conditions need to hold ... The way this is achieved is beyond the scope of this paper" (§3.1, p. 6).

### 1.4 Goals and utilities per agent

A problem has one or more goals and zero or more metrics, each optionally attributed to an agent or a type:
```
<goal>        ::= (:goal [:agent <agent-def>] :condition <emptyOr (pre-GD)>)
<metric-spec> ::= (:metric [:agent <agent-def>] :utility <optimization> <metric-f-exp>)
```
(§3.2, pp. 6-7.) Which planner plans for which agent is deliberately outside the description: "It is the responsibility of the planner to know for whom it plans" (§3.2, p. 7).

### 1.5 Privacy, added in 2015

The 2015 BNF adds two mutually exclusive requirements. Under `:unfactored-privacy` one domain and problem serve all agents and private predicates, constants, and objects are tagged per agent with `(:private <agent-def> ...)`. Under `:factored-privacy` each agent has its own single-agent domain and problem holding only its own private items: "A factored description is single-agent. Only the private predicates/constants/objects of the agent for which the MA-PDDL description was factored are indicated" (BNF 2015 §2.2, p. 4). The privacy notion is MA-STRIPS's: an atom is internal to an agent if no other agent's action mentions it, public otherwise (MA-STRIPS p. 29).

### 1.6 The paper's worked example

Two agents must lift a table together (Kovács 2012 §3.3, p. 7):
```lisp
(define (domain ma-lift-table)
  (:requirements :equality :negative-preconditions
                 :existential-preconditions :typing :multi-agent)
  (:types agent) (:constants table)
  (:predicates (lifted ?x - object) (at ?a - agent ?o - object))
  (:action lift :agent ?a - agent :parameters ()
    :precondition (and (not (lifted table)) (at ?a table)
                       (exists (?b - agent)
                         (and (not (= ?a ?b)) (at ?b table) (lift ?b))))
    :effect (lifted table)))

(define (problem ma-lift-table-1)
  (:domain ma-lift-table)
  (:objects a b - agent)
  (:init (at a table) (at b table))
  (:goal :agent agent :condition (lifted table)))
```
"The only, trivially simple solution is when both lift the table starting at time 0: [0:(lift a) 0:(lift b)]" (p. 7). `(lift ?b)` in the precondition is the joint-action device of 1.3.

## Part 2. How MA-PDDL is used

MA-PDDL's one real use is the CoDMAP competition of 2015, "meant to be a preliminary version of possible future Multiagent Planning (MAP) track at the IPC" (website). The competition chose the language and added privacy: "We chose MA-PDDL (Kovacs 2012) and extended it with a partitioning definition and a definition of privacy of objects and predicates" (CoDMAP p. 110). It restricted it heavily: "deterministic non-durative model (STRIPS-compatible)" and "cooperative agents (only common and public goals; common metrics; no joint-actions)" (website); "All actions were discrete time and nondurative" (CoDMAP p. 110). So the parts of MA-PDDL that were exercised are 1.2 and 1.5; 1.3 and 1.4 were not.

### 2.1 An unfactored domain

The competition's Logistics domain, complete for its types, predicates, and one truck action (CoDMAP files, `logistics00/domain.pddl`):
```lisp
(define (domain logistics)
  (:requirements :typing :multi-agent :unfactored-privacy)
  (:types
    location vehicle package city - object
    airport - location
    truck airplane - vehicle)
  (:predicates
    (at ?obj - object ?loc - location)
    (in ?obj1 - package ?veh - vehicle)
    (:private ?agent - truck
      (in-city ?agent - truck ?loc - location ?city - city)))

  (:action drive-truck
    :agent ?truck - truck
    :parameters (?loc-from - location ?loc-to - location ?city - city)
    :precondition (and
      (at ?truck ?loc-from)
      (in-city ?truck ?loc-from ?city)
      (in-city ?truck ?loc-to ?city))
    :effect (and
      (not (at ?truck ?loc-from))
      (at ?truck ?loc-to))))
```
The website's reading: "In the domain, the agents are represented by a lifted typed expression, such as (in the action def.) :agent ?airplane - airplane, which means that all objects of type airplane are agents. In the problem, the respective objects or constants are used instead."

### 2.2 An unfactored problem

Objects, with each agent private to itself (`logistics00/probLOGISTICS-10-0.pddl`, init and goal abbreviated):
```lisp
(define (problem logistics-10-0) (:domain logistics)
  (:objects
    apt1 apt2 apt3 apt4 - airport
    pos1 pos3 pos4 - location
    obj11 obj12 obj13 ... - package
    (:private apn1 apn1 - airplane)
    (:private tru1 tru1 - truck cit1 - city)
    (:private tru2 cit2 - city tru2 - truck pos2 - location)
    ...)
  (:init (at apn1 apt1) (at tru1 pos1) (in-city tru1 pos1 cit1) ...)
  (:goal (and (at obj31 pos3) (at obj33 apt3) ...)))
```
"By convention, a PDDL object representing an agent was private to that given agent. If it was not, other agents of the same PDDL type would be able to ground and use the other agent's actions" (CoDMAP p. 110). Fact privacy follows three rules, "maximally concealing grounding": a public predicate over public objects is public; over at least one private object it is private to that agent; a private predicate is always private (p. 110).

### 2.3 The factored form and the agent list

For the distributed track, "Each agent has its own (single-agent) domain and problem. Only predicates known to the agent are defined in the domain, private predicates are enclosed in a (:private ...) expression" (website). Input files are `domain-agent_1.pddl, problem-agent_1.pddl, ...` plus a list of agent names and addresses. Plain PDDL is converted to and from MA-PDDL by scripts; the agent list travels as an `.addl` file of the form `(define (problem P) (:domain D) (:agents a1 a2 ...))` or one name per line (`ma-to-pddl.py`, `write_addl`, `write_agent_list`). The distributed output is one plan per agent with integer timestamps, "actions at the same timestamp are considered parallel. All actions are considered to have duration of 1 timestep" (website), for example `10: (load-truck tru1 pkg1 loc1)`.

### 2.4 Who reads it

The centralised-track planners "had to read the input in MA-PDDL, either factored or unfactored" (CoDMAP p. 111). The winner, ADP, "ignored the partitioning and the privacy predefined in MA-PDDL" and decomposed the problem itself (p. 114). FMAP, a distributed planner, uses its own dialect: "we write a domain and a problem file for each agent ... The problem files, however, are extended with an additional :shared-data section" (FMAP §3), and "does not yet explicitly manage time constraints nor durative actions" (§4.4). A 2017 survey calls MA-PDDL "the first attempt to create a de facto standard specification language for MAP tasks". Joint actions, the part of MA-PDDL that says two agents act together, remained future work: "A partitioning related extension is to allow joint actions, which have to be performed by two or more agents at the same time" (CoDMAP p. 114).

### 2.5 Concurrency constraints outside MA-PDDL

Crosby's notation puts concurrency on object-action pairs rather than in preconditions. Domain side (`maze_dom_cn.pddl`): `(:requirements :typing :concurrency-network :multi-agent)`, actions with `:agent ?a - agent`, and
```lisp
(:concurrency-constraint v2
  :parameters (?b - boat ?x - location)
  :bounds (2 inf)
  :actions ((row 1 2)))
```
Problem side, in Crosby and Petrick's version: `(:capabilities (R1 navigate-robot-side pick-heavy ...) ...)` says which actions an agent may perform, and `(:concurrencies (kit1 deliver-kit 2 2) ...)` says "not more than max and at least min agents can simultaneously utilise object o via the actions in the action list" (Crosby 2014 p. 19). The encoding is compiled to PDDL 2.1 durative actions with a `(free ?a)` predicate "used to make sure that each agent only ever performs a single action at a time" (p. 20), the same device as `robot-entry-as-type.md`'s export.

## Part 3. Hierarchical, multi-agent, and temporal together

No peer-reviewed language definition combines all three. Each pair exists.

| Language or planner | Hierarchical | Multi-agent | Temporal | Kind |
|---|---|---|---|---|
| MA-PDDL (Kovács 2012, BNF 2015) | no | yes: `:agent`, per-agent goals, action formulas | yes in the grammar: `:durative-action` keeps `[:agent]`; durative joint-action semantics left open; CoDMAP used none of it | language definition |
| Crosby and Petrick 2014 | no | yes: `:capabilities`, `:concurrencies` | yes: integer durations, compiled to PDDL 2.1 | encoding plus translation |
| FMAP | no | yes: one PDDL 3.1 pair per agent, `:shared-data` | no | planner input |
| MA-HTN (Cardoso and Bordini) | yes: SHOP2-style operators and methods | yes: `agent` header, `conflict` and `dependency` lists naming other agents' actions | no: durations appear only as motivation | grammar in a paper, translator from JaCaMo |
| HDDLGym (2025) | yes: HDDL | yes: an `agent` type, `?agent - agent` parameters, a `none` action | no | modified HDDL for a Gym environment |
| HDDL 2.1 | yes | no construct; agents only in the motivation | yes: durations, point-algebra ordering, non-interference | formalism, no syntax reported |
| ANML, FAPE | yes: decomposition through action propositions and subtasks | no construct; rovers and robots are ordinary object values | yes: intervals, durations, timelines | language and planner |
| T-HTN (2021) | yes | yes: multi-robot, robots as timelines | yes: deadlines | Master's thesis, not peer reviewed |
| PLANTOR (2025) | two levels | yes: robots as Prolog constants | yes: durative actions | formalism and planner over Prolog, not PDDL |

What the sources say about the missing corner:

- MA-PDDL keeps durative actions and intended a durative competition category, but CoDMAP restricted itself to "non-durative" (Part 2), and no hierarchy exists anywhere in it.
- MA-HTN adds to SHOP2 an `agent` owner per domain and, on operators only, `conflict ::= $action-name $agent-name` and `dependency ::= $action-name $agent-name` (MA-HTN Listing 1, p. 6): "only operators can cause conflicts, methods cannot" (p. 5). Its grammar has no durations; its later system DOMAP runs "an instance of the SHOP2 planner" per agent with contract-net allocation (AAMAS 2019 p. 800).
- HDDLGym marks agents by type inside HDDL, `vehicle - agent`, and gives every agent action an `?agent - agent` parameter and a `none` action per step (HDDLGym §4). It is the Transport domain of `pddl-for-process.md` with the vehicle type declared an agent.
- HDDL 2.1 motivates itself by "agents coordination in HTN problems" and gives `=` in its ordering algebra and a non-interference condition for simultaneous snap actions (HDDL 2.1 §1, Def. 6, §3), but has no agent construct and "did not explicitly report a syntax" (§5).
- ANML and FAPE model a robot as an object value in state variables; exclusivity comes from timeline consistency or from a unit reusable resource, `[all] resource :uses q ;` (ANML p. 4). The words "agent" and "actor" do not occur in the ANML paper.

The closest thing to all three in a PDDL-family grammar is therefore HDDL with the robot as a typed parameter, which is what HDDLGym does and what the Transport benchmark already does with `?v - vehicle`, plus HDDL 2.1's durations. Nothing in that combination is a language-level agent construct; the agent is a type.

## Part 4. Recent work: several robots, PDDL, and a language model

Four works from 2023 onward. None uses MA-PDDL; none cites Kovács. In all four the robot is either a typed object in plain PDDL or absent from the PDDL altogether.

**TWOSTEP.** "We propose decomposing an N-agent planning problem into N single-agent planning problems" (TWOSTEP §III). A language model writes each helper agent's subgoal in English and then as a PDDL `(:goal ...)`; Fast Downward plans; each plan's end state is the next agent's start state; a post-hoc algorithm decides which steps can run in parallel (§III, §IV.C). The method "works with single agent domains without any modifications" (§IV.B.3). Its multi-agent baseline is plain PDDL with an `agent` parameter added to every action, and "does not support true parallelization and proposes one agent action at each timestep since it would require significant domain modifications" (§IV.B.2). The GRIPPERS problem it shows is ordinary PDDL, `(:objects robot1 - robot rgripper1 lgripper1 - gripper ...)`, and the helper agent's identity lives in the prompt, not the file (Appendix B).

**LLM+P.** The single-agent method TWOSTEP builds on. The language model writes only the problem file; the robot is implicit in `(arm-empty)` (LLM+P §III.B).

**LaMMA-P.** "Each robot type has a pre-defined domain for its available actions. The domain defines two types: robot and object" (LaMMA-P §IV); every operator has `?robot - robot` as a parameter, and there is one domain and one problem per robot per subtask, `(:domain robot2)`. A language model merges the robots' plans into a timestamped schedule, `0.000: (GotoObject robot1 microwave) 0.000: (GotoObject robot2 egg) ...` (Fig. 2). It cites TWOSTEP as "restricted to single-agent or two-agent systems" (§II).

**PIP-LLM.** Plans at team level in PDDL "without referring to any specific robots" (PIP-LLM §III), then assigns robots to subtasks by integer programming over travel cost, workload, and capability. It criticises TWOSTEP and LaMMA-P for relying "on pure syntactic segmentation and analysis of natural language commands for task decomposition" (§I).

**PLANTOR**, for time, leaves PDDL for a Prolog knowledge base with two levels of durative actions and robots as constants, "a restricted form of hierarchical temporal planning with only two hierarchical levels" (PLANTOR §4).

## Part 5. What this means for the process module

The question that led here: must a method be able to say that two of its subtasks are performed by the same robot, and if so does the robot have to be a declared parameter rather than a slot filled at stage two?

What the sources settle:

- **The construct for "the same robot" is variable repetition, in every language that has it.** MA-PDDL's `:agent ?truck` variable "may appear in the body of the action-schema just like any other action-parameter" (Kovács 2012 §3.1, p. 5); HDDLGym threads `?agent - agent` through tasks and methods; MA-HTN names the other agent's action in a `dependency`; Transport threads `?v`. No language has a slot for it that is not a parameter. Basis: Parts 1 to 3.
- **A language-level agent construct adds three things, none of which the process module needs now.** MA-PDDL's `:agent` field exists to partition actions among agents for planner assignment and privacy (1.2, 1.5); action formulas in preconditions exist for joint actions where two agents act on one thing at once (1.3); per-agent goals and utilities exist for competitive or mixed settings (1.4). The brief has cooperative robots, common goals, no privacy, and defers joint actions with the Capacity and component-state kinds. Basis: Part 1 against the brief's Two-Stage Allocation section.
- **What survives when those are removed is a typed parameter.** CoDMAP's own scripts convert MA-PDDL back to "plain pddl + a list of agents" (website), and the recent multi-robot work uses `?robot - robot` in plain PDDL (Part 4). HDDLGym reaches hierarchy plus agents by declaring a type `agent` in HDDL. Basis: Parts 2 to 4.
- **Joint actions are the one thing a parameter cannot express and MA-PDDL can.** Two robots lifting one beam is `(lift ?b)` in `lift`'s precondition (1.6), or Crosby's `(kit1 deliver-kit 2 2)` (2.5). HDDL 2.1's `=` ordering can say two subtasks start together but not that they are one joint action. Basis: 1.3, 2.5, Part 3.

Recommendation, resting on the above and on `pddl-for-process.md` question 3. A `robot` parameter kind on primitives and methods is the sources' construct for "same robot", and it is the only one; a separate `assigned_unit` slot cannot state it. Nothing in MA-PDDL beyond the typed parameter is warranted by the brief's scope. Joint actions stay out until a cooperative method exists; when one does, the construct to look at first is HDDL 2.1's `=` on start events combined with the robot parameter, and only if that fails, MA-PDDL's action formula. The decision remains the user's, since it changes a brief decision and common's enum, as `pddl-for-process.md` part 3 records.

Closed 2026-09-17, with `pddl-for-process.md` part 4 question 3:

1. One robot across subtasks is needed, by any Transport-style method, and is written by threading the method's robot variable. Joint actions, two robots on one component at once, stay out until a cooperative method exists.
2. Every primitive declares its robot parameter, as Transport and HDDLGym do. The value is a machine id; the planner binds it and stage two may rewrite it; no separate `assigned_unit` slot.
