# MFM Data Model local artifact — experimental 0.1

This is a logical modeling artifact, separate from MFM Spec format 0.5. It adds
no spec node kinds. `model.yaml` carries definitions and relationships; a sibling
`NOTES.md` records the modeling session and handoff. Both are ordinary local files.
Field structure is defined by `scripts/model.py`; JSON Schema is derived with
`python scripts/model.py --schema`. Python 3.10+, Pydantic 2, and PyYAML 6 are
required; respect the project's execution policy when running the script.

## Document

| Field | Meaning |
| --- | --- |
| `format_version` | The quoted string `"0.1"`. |
| `id`, `title` | Stable model identity and human name. |
| `revision` | Explicit revision within this model, never a moving latest alias. |
| `status` | `draft` or `published`; initial work remains draft. |
| `spec` | `id`, exact `revision`, and `location` of the governing specification. A relative location is relative to `model.yaml`. |
| `scope` | Nonempty list of governing spec node ids covered by this model. Partial coverage is explained in the notes. |
| `authority` | The designated data-design role and participating users, described in prose; not a session id or access-control credential. |
| `concepts` | Nonempty list of concept definitions. |
| `open_questions` | Unresolved model-wide questions; may be empty. |
| `publication` | Null for drafts; for published models, an attributable `actor` and `reason`. Records a decision, does not authenticate it. |

Local ids use lowercase kebab case. A model reference is its id plus revision;
a concept reference additionally names its concept id. Revisions are opaque
identifiers resolved by the owning project. Published revisions must resolve to
unchanged content, through version control or immutable exports. The checker
rejects obvious moving aliases but cannot prove immutability or publication authority.

## Concept

Each concept contains `id`, `definition`, `identity`, `lifecycle`, `spec_refs`,
`relationships`, `invariants`, and `open_questions`. All fields are explicit,
including empty lists. Identity and lifecycle are nonempty prose: describe their
scope and rules, or explicitly state what is unresolved. Definitions describe
domain instances; these files are not instances or a database schema.

A relationship has an `id` unique within its concept, a `target` concept id,
`cardinality`, and `meaning`. Cardinalities count targets per source instance:
`one`, `zero-or-one`, `many` (zero or more), or `one-or-more`. Conditional rules
belong in invariants; do not introduce a state-machine language to encode them.
Use relationships only for concepts in this model. Reference external spec
definitions in prose and `spec_refs` until their modeling boundary is settled.

An invariant has an `id` unique across the model and a nonempty `statement`.
These are semantic obligations for architecture review, not executable predicates.
Spec references link concepts to the requirements that justify them; they do not
assert that a proposed model choice has already been approved in the spec.

For example, an allocation might relate to one resource and one-or-more users.
Its invariant could say that allocations never exceed the resource's capacity,
with capacity units and the overlapping time interval defined explicitly. A later
architecture chooses how to preserve that obligation under concurrent writes.

## Validation boundary

The checker rejects malformed fields, unknown fields, blank prose, duplicate YAML
keys, duplicate concept or invariant ids, duplicate relationship ids within a
concept, and dangling relationship targets. Published models require a publication
record and no unresolved questions. It does not check source existence, semantic
completeness, satisfiability, actual approval, compatibility, or runtime behavior.

Run the existing spec validator separately and resolve `scope` and `spec_refs`
against the identified source revision. Do not interpret a successful model check
as proof of those external links. Relationships may contain cycles: a logical
domain graph is not the spec's acyclic component dependency graph.

## Evolution

Preserve ids when meaning remains the same. Record changed meaning and affected
consumers before publishing another revision; preserve old snapshots. Do not
reuse a retired id for an unrelated concept or invariant. This first format does
not automate compatibility, migrations, publication, or downstream adoption.
The exact handling of those obligations must be designed with the owning project.
