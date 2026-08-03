---
name: mfm-spec
description: >-
  Use when working with hosted MFM Spec: a spec stored in the MadeForMachine service
  and read, mutated, validated, and versioned through MCP tools. Use for
  service-backed spec authoring, minimal-context reads,
  fine-grained spec mutations, validation, history, and evaluation notes. Do not use
  for local file-backed specs; use the mfm-spec-local skill for that.
version: 0.5.0
status: alpha
public: true
connector: mfm
requires: [mfm_spec_project, mfm_spec_read, mfm_spec_validate, mfm_spec_mutate, mfm_spec_rename, mfm_spec_merge, mfm_spec_split, mfm_spec_retire, mfm_spec_write, mfm_spec_history, mfm_spec_import, mfm_spec_export]
license: MIT
---

# MFM Spec

MFM Spec is the hosted MadeForMachine product that uses the MFM Spec format as its
portable artifact, but keeps the canonical working spec in a service-backed revision store.
Your job is to steer the user's own agent: discuss, interrogate, read minimal context,
mutate through deterministic MCP tools, and let server validation guard the graph.

If the `mfm_spec_*` MCP tools are not available, do not pretend to persist anything. You may
shape the intended change in the conversation, but stop before commit and report that the
MFM Spec connector/tooling is missing.

## Scope

Work at the MFM Spec MVP graph level:

- **Components** — responsibility owners.
- **Features** — observable behavior linked to the components they need.
- **Criteria** — system qualities, constraints, and prohibitions the spec must preserve,
  pursue, or avoid.
- **Evaluations** — feedback or judgment records against a feature, component, revision,
  criterion, variant, or artifact.

Do not choose technologies, UI layouts, data schemas, implementation plans, or code. Park
those as lower-layer details or open questions on the relevant node.

## Read Small

Start every session with `mfm_spec_project` for current project metadata and policy, then
use `mfm_spec_read` with `view=map`. Keep the whole map in context: node id, kind, status,
parent, and edge summary — including criterion statement, scope, and strength. Load full
bodies only for the active blast radius:

- `view=node` for one full node,
- `view=subtree` for a component branch,
- `view=referrers` for everything pointing AT one node — children, dependents, touching
  features, evaluation subjects — the blast radius to query before any identity change,
- named projections such as `authoring-map`, `feature-work`, or `derivation-context` when
  the task has a stable slice shape.

The persisted spec is the memory. The chat is disposable.

## Interrogate First

Let the user dump raw intent before formalizing. Classify it into components, features,
criteria, evaluations, open questions, and lower-layer details. Propose the smallest touched
node set, then surface the one or two boundary questions that would change the graph.

Always name the touched nodes before mutating. A request rarely affects one node; trace the
blast radius across dependencies, feature touches, and evaluation subjects.

## Apply Criteria Actively

Criteria are not passive review checklists. Use the active criteria to improve the spec while
it is being written or changed:

1. Read the compact statement, scope, and strength for every active criterion.
2. Load the full body only for criteria relevant to the current discussion.
3. Before proposing a mutation, state any pressure or conflict those criteria create.
4. Ask for missing decisions that materially affect a criterion.
5. Push back when a proposal violates a required criterion; for a preferred criterion, name
   the trade-off instead of silently overriding it.
6. Record unresolved tensions as open questions and conclusions as decisions on the relevant
   node. Record review findings as evaluations whose subject includes the criterion.

A criterion may create technical pressure — for example, latency can rule out obviously slow
interaction shapes — but do not turn that pressure into a prescribed technology or architecture
inside the spec. Preserve the outcome and constraint; leave the mechanism for derivation.

## Mutate Through Tools

The normal commit path is `mfm_spec_mutate`, not whole-node replacement. Use
`mfm_spec_validate` first when the change is non-trivial or when you expect a repair loop.
Every commit carries the `base_rev` from the last read and a required `change_note`.

A revision is one coherent decision, not one touched node. Once the touched-node set has
settled, batch all of its operations, validate the complete candidate, and commit it once.
The `change_note` is a concise human explanation of what changed overall, why, and any
remaining point worth review. Do not mechanically enumerate files or operations: the service
already stores those as deterministic evidence. Failed validation attempts create no revision,
and the service rejects an unchanged candidate rather than recording an empty checkpoint.

MVP operations are deliberately small and deterministic:

- create node,
- delete node,
- move node,
- set frontmatter field,
- add/remove dependency,
- add/remove feature touch,
- replace or append a named body section,
- record evaluation node.

Use `mfm_spec_write` only for import/bootstrap or as an escape hatch when the user already
intends to replace whole nodes. It is not the normal authoring primitive.

## Reorganize Through Intents, Not Cascades

A node's id is its identity. When the shape of the spec is wrong — a node is misnamed, two
nodes are one, one node is two, a responsibility is gone — do NOT hand-compose the change
from primitive ops, and never end an identity change in `delete_node`: that destroys the
provenance the graph is for. Use the dedicated intents:

- `mfm_spec_rename` — recreates under the new id, repoints every live referrer, supersedes
  the old id. Fully deterministic; you supply nothing but the ids.
- `mfm_spec_merge` — you author the successor (`into`: a create payload, or an existing
  node id to absorb into); the server wires: referrers repoint, each merged node gets
  `status: superseded` and `superseded_by` → successor.
- `mfm_spec_split` — you author the successor payloads and `reassign` each live referrer to
  the successor it now needs; the server refuses to guess an unassigned referrer.
- `mfm_spec_retire` — for a responsibility that is gone, not relocated. Refused while live
  nodes still reference it; the refusal lists them.

The loop is always: `view=referrers` on the affected node → name the blast radius to the
user → issue the intent with the current `base_rev` and a `change_note`. Superseded nodes stay
in the graph as provenance; evaluations keep pointing at them by design.

If a write is rejected because `base_rev` is stale, re-read the map and the changed nodes,
reconcile the user's intent against the new head, and resend a fresh mutation batch. Never
force through a conflict.

## Validation Boundary

`mfm_spec_validate` and `mfm_spec_mutate` both apply the proposed operations to the base
revision, parse the resulting MFM Spec graph, and run the deterministic lint rules. A
failed validation changes nothing. Treat the error report as the source of truth for
structural validity; semantic quality remains your job.

Load-bearing errors:

- exactly one root component,
- all parents, dependencies, feature touches, criterion scope references, and checked
  evaluation subjects resolve,
- component and dependency graphs are acyclic,
- component responsibilities, feature intents, criterion statements, and evaluation summaries
  are one sentence.

## Evaluation Notes

When feedback arrives, record it as an `evaluation` node instead of burying it in chat or
rewriting intent silently. Evaluations may point at a component, feature, criterion, revision,
variant, artifact, or any combination. They record what was learned; a later explicit
mutation promotes that lesson into the spec.
