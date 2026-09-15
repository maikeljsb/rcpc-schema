# rcpc-schema

LinkML model of the Product Process Graph, one module per file under `schema/`. `CAPABILITY-MAP.md` indexes the modules; each has a `SPEC-<id>.md` beside it.

Always read: `docs/ideas/linkml-product-process-graph-schema.md` (the brief, authoritative) and `CAPABILITY-MAP.md`.

## Index

Where things are. Open an entry when the work at hand needs it.

- Module specs: `SPEC-<id>.md` beside the map, one per module.
- LinkML metamodel, conformance, inheritance: `docs/research/linkml-metamodel-conformance-and-inheritance.md`.
- LinkML to Neo4j projection: `docs/research/linkml-neo4j-and-metamodel.md`.
- Task parameter kinds: `docs/research/parameter-kinds-mapping.md`.
- Resource module sources: `docs/ideas/robot-entry-as-type.md`, CRS paper `docs/research/2026_01-ITcon-Li.pdf`.
- Product module sources: `docs/research/ifc43-for-product.md`, `docs/research/topologicpy-for-product.md`.
- Plans and task lists: `tasks/`, finished ones under `tasks/archive/`.

## How work proceeds

- Gated spec-driven development with the `agent-skills:spec-driven-development` skill. Invoke it at the start of any module work and continue at the phase the repository is in; if the prompt does not say which, ask the user. Phase 1 answers and research findings go into the brief before the spec is written.
- Recommend the plainest mechanism that meets the stated requirement, described in plain words.
- Commit only when told to, with Conventional Commits 1.0.0. A commit touching `schema/`, `scripts/`, `tests/`, or `examples/` passes `uv run pytest` first and rebuilds `dist/` and `docs/model/` in the same commit. The plan or todo checkbox commit is always separate from the schema commit.
- A class and a same-named slot write the same generated docs page on a case-insensitive filesystem and break CI on Linux; flag the collision before committing and rename the slot.
