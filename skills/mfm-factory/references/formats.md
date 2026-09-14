# Starting formats

Use **MFM Data Model 1** (`mfm-data-model/1`) and **MFM Architecture 1**
(`mfm-architecture/1`). These small JSON-compatible formats extend the project's
existing concepts. YAML is a readable rendering, not another authority.
The canonical definitions are [Pydantic models](../scripts/formats.py); generated
[Data Model JSON Schema](data-model.schema.json) and
[Architecture JSON Schema](architecture.schema.json) describe their document shape.
Format versions are independent of user-facing content revisions and skill releases.
The [small order example](example.json) illustrates both documents; it deliberately
labels its missing failure and persistence coverage and is not a complete product design.

These are newly selected formats, **not payloads accepted by legacy Factory /v1**.
Discover service support before publishing. Never relabel an old artifact or force
one of these documents into an older import command. Migration preserves originals.

## Authority and identity

The service envelope owns project, spec variant, architecture variant where relevant,
immutable revision, authoring inputs, actor and reason. Content does not duplicate
that envelope. A model has no user-assigned name. One spec variant owns one model;
architecture variants are named alternatives within that scope. Revisions start at 1;
an absent artifact is “No version yet”. Saving changed content creates a revision,
regardless of completeness. Unchanged downstream content retains its revision.
There is no draft selection layer. Questions describe incomplete design honestly.

Use stable lowercase IDs, not display names or paths, for graph references. Retain
identity through ordinary edits. Renames, splits, merges and retirement preserve
history in the service; the current graph contains current responsibility owners.
Construction records the exact spec/model/architecture tuple it actually uses.
Authoring provenance does not prohibit later reuse after agent assessment.

## Data Model

Define concepts, their logical attributes, identity, relationships, lifecycle and
invariants. Attribute types are deliberately small: text, identifier, integer,
decimal, boolean, date, datetime and bytes. Define units, precision, time zones,
allowed values and domain meaning in rules. Use relationships for structured
concepts rather than embedding storage layouts. Identity lists attribute IDs;
state its scope and uniqueness in invariants. Value concepts can use their values
as identity; do not invent surrogate IDs merely to satisfy the format.

Relationship cardinality describes targets per source. Record the reverse
constraint explicitly when relevant. `many` permits zero; `one-or-more` does not.
Concept and invariant IDs are model-wide; attribute and relationship IDs are local
to their concept. `spec_refs` refer to the exact spec supplied by the service.
Lifecycle is plain language initially; a state-machine language can follow an
actual need. Invariants are named semantic obligations, not claimed executable proofs.

Keep tables, indexes, HTTP bodies, event encodings and migrations in Architecture.
An empty concepts array can represent a product with no domain data; explain that
choice to the user rather than inventing entities.

## Architecture

Author one explicit graph; derive diagrams and construction context from it.

| Collection | Meaning |
| --- | --- |
| `components` | Responsibilities, containment parent, upstream references, technology, deployment and permitted effects. One root; containment cannot cycle. |
| `contracts` | Shared interface payload definitions using JSON Schema Draft 2020-12. Include error payloads. |
| `interfaces` | Component-owned required or provided ports, request/event/data-access kind, input/output/error contracts and behavioral semantics. |
| `connections` | Required-to-provided interface links and their transport and behavior. Runtime cycles are allowed. |
| `mappings` | How components, interfaces or contracts represent logical concepts and preserve invariants, including physical persistence choices. |
| `ownership` | Component-owned repository paths. Record exclusive ownership at the actual construction scope. |
| `obligations` | Component, contract, composition and operational checks the implementation must satisfy. |
| `scenarios` | Repeatable product flows: setup, ordered exchanges through connection IDs, expected behavior and final outcome. |

All architecture collection IDs share one namespace. Containment determines
ownership/integration scope; interface connections describe interaction. Neither
runtime direction nor graph traversal alone defines task scheduling. For events,
the publisher requires delivery and the receiving handler provides that interface;
model a broker as a component when its behavior matters. Model external systems
explicitly so a mock can replace their boundary without hiding the interaction.

Prefer local `$defs`/`$ref` within each payload schema. External contract references
must resolve to retained exact artifacts in the run; never depend on a moving URL.
JSON Schema describes payload shape; interface behavior and scenario expectations
describe effects, sequencing and failure semantics. Generate OpenAPI for HTTP
bindings where useful; do not make it a second authored source for shared payloads.

Start Factory dogfooding with **Next.js, FastAPI and PostgreSQL**, using the project's
existing Docker workflow. Record exact dependencies in the architecture and lockfiles.
Other projects must make their stack choice explicitly. This is an initial learning
scope, not a permanent universal technology constraint. LinkML, UML/XMI, ArchiMate,
SysML, graph databases and a general-purpose workflow interpreter are not prerequisites.

## Validation limits

The generated schemas validate document shape. The reference models additionally
check unique IDs, local references, containment and connection direction. Service
integration must resolve upstream IDs against exact input documents, validate the
embedded JSON Schemas, and check canonical ownership paths. These are structural
checks. They do not establish semantic agreement, scenario coverage, performance,
or correctness. Do not introduce a mandatory compatibility certificate.

Designs may contain questions and incomplete scenario coverage. Before construction,
the agent examines those gaps with the user and establishes the scenario scope.
The required mock milestone concerns execution evidence for that scope; it is not
an authoring admission gate. See [construction](construction.md).
