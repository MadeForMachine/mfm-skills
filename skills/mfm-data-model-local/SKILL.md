---
name: mfm-data-model-local
description: >-
  Develop or revise a logical data model from a specification in local project
  files. Define concepts, identity, relationships, lifecycle, and invariants;
  review architecture mappings for preservation of that meaning. Use before
  physical database or API schema design, or when revisiting shared data meaning.
version: 0.1.0
status: alpha
public: false
connector: null
requires: []
license: MIT
---

# MFM Data Model Local

Develop data meaning with the user from their governing specification. The model
must expose ambiguities that field declarations would hide and give a later
architecture concrete obligations to satisfy. This experimental local workflow
needs files and an agent; it has no hosted service or required agent harness.

## Start from the existing system

Find the specification and any existing data model. Read the spec map, relevant
features and criteria, and existing definitions before introducing concepts.
Reuse established identities and meanings. Do not copy the spec's component tree
into an entity list: responsibility owners and domain concepts are different.

Read [FORMAT.md](FORMAT.md) when creating or changing model files. It defines the
experimental artifact contract; [scripts/model.py](scripts/model.py) is its
executable structural schema. Keep project artifacts outside the skill and outside
the MFM Spec node directory, normally in `data-model/`.

Identify the source spec and an exact revision. Git is one possible revision
mechanism, not a prerequisite. An immutable export identifier also works. Read that
snapshot; if only a changed working copy is available, explicitly identify it as
a new draft snapshot rather than claiming the old revision governs new content.

Keep a compact whole-system concept map in view. Develop one connected behavior
path first; name the unmodeled areas and dependencies in the handoff. A bounded
first pass is a partial model, not proof of whole-system coverage.

## Interrogate meaning

For each concept, establish what it means, what distinguishes one instance from
another, its scope, relationships and cardinalities, lifecycle, and invariants.
Ask about units and time semantics where quantities or time affect behavior.
Give each invariant a stable id so architecture decisions can reference it.

Use concrete counterexamples: can this identity survive a restart? Can the same
thing belong to two scopes? What happens when an upstream revision changes? Does
deletion erase an obligation or its evidence? Record unresolved answers as open
questions, not plausible-looking rules. Explain alternative meanings when they
would change behavior; choose routine representation details using project context.

Keep logical meaning independent of tables, API payloads, storage engines,
frameworks, agent session identifiers, and deployment boundaries. A logical
relationship does not imply a physical foreign key or shared database. Design
authority over meaning does not imply custody of every dataset.

When the spec is contradictory or silent about required behavior, identify the
source nodes and route the question to the spec dialogue. Do not quietly invent
requirements. Semantic judgment belongs to the user's agent; a validator checks
structure, not whether the business rules are right.

## Review and evolve

Persist useful drafts within the user's authorized scope. Distinguish proposed
model choices from approved intent. Publication must name the authorized actor
and reason; a passing validator is not approval. Do not ask again for an approval
already given, and do not equate permission to draft with approval of every rule.

When architecture exists, review its concrete interface and persistence mappings
against invariant ids. Architecture owns representations; this role reviews
their meaning. Record satisfied obligations, conflicts, and missing evidence.
Unsatisfied obligations return to the responsible design role and users; they
are never weakened locally to accommodate a technology choice.

On revision, preserve prior published content and identities. Identify affected
architectures, contracts, work, and evidence, or explicitly say those consumers
do not exist or are unknown. A new publication does not update their pinned inputs.
Incompatible alternative meanings require distinct model identities and explicit
compatibility review. Do not equate structural validity with migration safety.

## Leave resumable work

Validate `model.yaml` with `scripts/model.py` in the project's permitted execution
environment. Dependencies are in `scripts/requirements.txt`. Use `--schema` to
derive JSON Schema from the same Pydantic models; do not maintain a second schema.
Resolve the model's spec references against the actual governing snapshot using
the existing spec reader. The model checker does not fetch or verify that snapshot.

Keep `NOTES.md` beside the model: source location and revision resolution, coverage,
decisions and reasons, concrete review cases, applicable criteria and their status,
open questions, and the next useful action. Reference concept and invariant ids;
do not maintain duplicate authoritative definitions there.

Use the first application to improve this skill and format. Change instructions
when an observed failure warrants it; do not generalize every project decision
into a universal modeling rule.
