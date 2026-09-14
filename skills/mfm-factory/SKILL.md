---
name: mfm-factory
description: >-
  Use for MadeForMachine Factory projects, including development of the Factory
  itself: maintain hosted specs, logical data models and architecture variants,
  then construct an executable mock and replace it with verified implementation
  through MCP-recorded work. Use for construction feedback and resuming these projects.
version: 1.0.0
status: alpha
public: false
connector: mfm
requires: [mfm_spec_project, mfm_spec_read, mfm_spec_validate, mfm_spec_mutate, mfm_spec_rename, mfm_spec_merge, mfm_spec_split, mfm_spec_retire, mfm_spec_history, mfm_spec_import, mfm_spec_export, mfm_factory_project, mfm_factory_schema, mfm_factory_read, mfm_factory_graph, mfm_factory_mutate, mfm_factory_context, mfm_factory_history, mfm_factory_changes]
license: MIT
---

# MFM Factory

Guide the user's own agent through **Specification → Data Model → Architecture →
Construction**, returning upstream when implementation exposes missing or incorrect
design. MFM stores and validates records; it does not run an inference service or
launch construction agents. These design responsibilities can belong to one agent.
Do not introduce extra sessions, approval handoffs or delegation automatically.
Use the [glossary](references/glossary.md) when a term or role boundary is ambiguous.
All reusable schemas, conventions, examples and agent instructions belong in this
skill's mfm-skills repository; project-specific intent and artifacts belong to the project.

## Start or resume through MCP

Read the project's binding and discover the actual tool capabilities. A service-backed
spec may run in local Docker; do not assume it belongs to the public MFM deployment.
Use MCP records as the working source of truth for design and construction. Repository
exports are mirrors; do not edit them as a substitute for hosted mutations.
Use the customer's ordinary development tools for code, fixtures and tests, and
record their exact inputs, work and evidence through MCP. This workflow also applies
when the project being constructed is the Factory itself.

Read [MCP operations and current limitations](mcp.md) before making a tool call.
If required tools or commands are absent, report the specific missing capability.
Continue independent supported work, but do not simulate success, edit the database,
call HTTP endpoints instead of MCP, or silently use a local design as authority.
This skill's selected formats and workflow do not imply that a deployment supports them.

For an existing project, read project policy, the current spec map and Factory
project/run records. Resume recorded tasks and exact inputs before creating work.
For a new project, use the advertised MCP creation operation with the user's chosen
name. If none exists, report that creation needs MCP support; do not invent a command.
An explicitly authorized first spec import is a bootstrap, never an overwrite of
an existing hosted project. Read its policy and HEAD before subsequent authoring.
When the user explicitly authorizes reconciling local authoring into an existing
service project, compare the complete local and service versions, preserve service-only
work unless its removal is explicitly intended, validate the result and write against
the current service revision. Read back/export and verify the result before treating
repository files as mirrors. This transition is not ongoing bidirectional authoring.

## Develop variants and designs

A project has named **spec variants**. Each owns exactly one unnamed **Data Model**
once modeling has begun and any number of named **architecture variants**. A model
can be absent before construction. Explore different logical meanings in separate
spec variants. Preserve stable IDs across name changes. Content revisions start at 1;
empty layers display “No version yet”. A change creates a revision; review alone does
not. There is no separate draft choice, and completeness is visible independently.

Use the existing MFM Spec format for intent, responsibilities, features and criteria.
The authoritative project policy and actual mutation schema govern how to edit it.
Read the map, then the affected nodes; validate one coherent mutation batch before
committing it with the read revision and a meaningful change note. Re-read conflicts.
Use dedicated rename/merge/split/retire operations after reading referrers, preserving
prior identities rather than composing delete-and-create replacements.

For modeling or architecture work, read [starting formats](references/formats.md).
Data Model defines meaning; Architecture defines a component/interface graph,
concrete representations and scenario expectations. Preserve the distinction between
the containment tree, runtime interactions and construction work scheduling.

After a spec change, inspect the existing model and affected architectures. After a
model change, inspect affected architectures. Change only necessary content; record
the assessment and explain retained choices. Identify alternatives not reassessed.
Do not bump downstream revisions solely to change provenance, and do not create a
semantic-validity certificate or imply a schema check proves compatibility.

## Construct and learn

Before starting construction, establish the user's selected spec variant and
architecture variant. An unambiguous earlier instruction is sufficient; ask only
when the choice is missing or ambiguous. A browser default is not that instruction.
Read the selected spec, its model and architecture. Check their consistency,
completeness and known logical faults; surface gaps and decide how to proceed within
the user's authority. Preserve the exact tuple actually chosen for the run.

Read [construction and feedback](references/construction.md). Build an **executable
mock product first**, using coherent agent-generated scenario data to exercise the
agreed complete product flows through actual declared interfaces. Record results,
then replace mocked behavior component by component and repeat relevant scenarios.
Passing the mock milestone does not mean the product is production-complete.

When a finding changes intent, data meaning or architecture, correct the responsible
hosted design through MCP within existing authority. Ask the user about unresolved
product decisions, not routine implementation details already authorized. Assess
downstream impact and explicitly adopt changed inputs into successor work; preserve
old runs and evidence. Components can be introduced, split, replaced or retired.
Their code, data, callers and ownership need explicit migration/removal work.

Conclude with the actual hosted revisions, construction state, evidence and remaining
gaps. Distinguish records that were persisted from proposed work and local artifacts.
