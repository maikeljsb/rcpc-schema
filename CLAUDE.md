# rcpc-schema

LinkML model of the Product Process Graph, one module per file under `schema/`. `CAPABILITY-MAP.md` indexes the modules; each has a `SPEC-<id>.md` beside it.

## Read before working

- Any schema work: `docs/ideas/linkml-product-process-graph-schema.md` (the brief, authoritative), then `CAPABILITY-MAP.md`, then the module's `SPEC-<id>.md`.
- Adding or changing a class, slot, enum, or `is_a`: `docs/research/linkml-metamodel-conformance-and-inheritance.md`.
- Reasoning about how the model becomes a Neo4j graph: `docs/research/linkml-neo4j-and-metamodel.md`.
- Task parameters: `docs/research/parameter-kinds-mapping.md`.
- Resource module: `docs/ideas/robot-entry-as-type.md` and the CRS paper, `docs/research/2026_01-ITcon-Li.pdf`.

## How work proceeds

- Gated spec-driven development: Specify, Plan, Tasks, Implement, each reviewed by the user before the next. On "proceed with SPEC-<module>", reply with the assumptions and numbered open questions and stop; the spec is written after the answers.
- Recommend the plainest mechanism that meets the stated requirement, described in plain words.
- Commit only when told to, with Conventional Commits 1.0.0. `uv run pytest` passes first; a schema change rebuilds `dist/` and `docs/model/` in the same commit.
