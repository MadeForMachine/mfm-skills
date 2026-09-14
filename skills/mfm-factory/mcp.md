# MCP operations and deployment boundaries

Discover live signatures with `mfm_factory_schema`. The portable envelope is defined
in [commands.schema.json](references/commands.schema.json), generated from
[commands.py](scripts/commands.py). The deployed schema decides what is supported.

| Work | Tools |
| --- | --- |
| Hosted spec policy and reading | `mfm_spec_project`, then `mfm_spec_read` (`map`, `node`, `subtree`, `referrers`) |
| Hosted spec changes | `mfm_spec_validate`, then `mfm_spec_mutate`, using the same `base_rev` |
| Spec identity changes | `mfm_spec_rename`, `mfm_spec_merge`, `mfm_spec_split`, `mfm_spec_retire` |
| Spec bootstrap, mirrors and history | `mfm_spec_import`, `mfm_spec_export`, `mfm_spec_history` |
| Variant heads and construction state | `mfm_factory_v2_project` |
| Exact designs and construction graph | `mfm_factory_read`, `mfm_factory_v2_graph` |
| Variant workflow commands | `mfm_factory_v2_mutate` |
| Shared project binding and retained evidence | `mfm_factory_mutate` with `bind_project` or `register_evidence` |
| Shared ledger and audit | `mfm_factory_history`, `mfm_factory_changes` |

Spec tools accept a `params` object; Factory tool parameters are direct. Read the
binding and project policy before writes. Tenant identity comes from authentication.
Bindings identify a project; they confer no access authority.

Every Factory mutation needs `project_slug`, a stable `idempotency_key`, a `reason`,
`expected_version` and a typed `command`. New records expect 0. Updates expect the
current mutable record version, which is distinct from its content revision number.
Preserve the complete payload and key when retrying an uncertain response. A changed
decision needs a new key. Re-read and assess conflicts; never overwrite blindly.
Read back results before reporting persistence. Keep pagination checkpoints fixed.

## Set up and explore

1. Read the existing hosted spec project or use `mfm_spec_import` for an explicitly
   authorized initial import. Never overwrite an existing hosted project to bootstrap.
2. If the Factory project is absent, use shared `bind_project` with `mode: hosted`
   and the chosen display name. This does not create Spec content.
3. `create_spec_variant` takes a stable ID, human name and existing `spec_project_slug`.
   Each spec variant binds its own independently editable hosted Spec project.
4. `sync_spec_variant` takes the variant ID and exact hosted `source_revision`.
   The Factory fetches that export through its configured authenticated Spec adapter.
5. `save_model` takes `spec_variant`, `spec_revision` and Data Model content. The
   `v2_model` record, keyed by spec variant, holds its head and expected version.
6. `create_architecture_variant` takes ID, name and spec variant. `save_architecture`
   takes its ID, selected spec/model revisions and Architecture content; use the
   architecture variant record version as `expected_version`.

Variant heads begin at 0 (no content). Content revisions start at 1 and advance only
when content changes. `rename_variant` updates metadata, not content. `no_change`
means reuse the existing revision. Review alone must not create revisions. A new
spec snapshot does not publish a new model or architecture.

To copy a spec variation, export its exact hosted revision, explicitly import it into
another hosted project, and create a variant with `copied_from` naming the original.
Then sync it and deliberately save model/architecture content retained after assessment.
To copy architecture, create another variant under the same spec variant with
`copied_from`, then explicitly save the selected content. `copied_from` records origin;
it does not silently copy content or construction results.

`v2_design` IDs are `spec:<variant>:<revision>`, `model:<variant>:<revision>` and
`architecture:<architecture-variant>:<revision>`. Read full content using
`mfm_factory_read`; project summaries omit content. Other record kinds are
`v2_spec_variant`, `v2_architecture_variant`, `v2_model`, `v2_run`, `v2_component`,
`v2_work`, `v2_finding` and `v2_scenario`. Graph reads take an exact `design_id` or
`run_id`; page with the returned checkpoint as `as_of`. Runtime edges retain interface
IDs alongside component endpoints. Containment and runtime graphs are distinct.

## Construct through the graph

1. Establish the user's spec and architecture variant choices. Read and assess the
   exact spec/model/architecture tuple. Older authoring provenance on unchanged
   downstream content is allowed; compatibility remains an agent/user judgment.
2. `start_construction` records the three revision numbers, both variant IDs,
   selected scenario IDs and the assessment. Give it a new stable run ID. An explicit
   `predecessor` links successor work within the same spec variant; it never copies
   progress or acceptance. Every new run starts in the mock phase.
3. `create_work` records component responsibility, task kind, instructions, ownership
   entries and obligation IDs from the pinned architecture. Paths use canonical
   `repository:path` entries: relative paths without trailing slash or `..`.
4. Build the executable mock and generated scenario data in the customer's harness.
   Retain code identity, data/generator and actual traces with shared `register_evidence`:
   each record includes its ID, body and SHA-256 `content_hash`. External locators alone
   do not satisfy scenario evidence; retained bodies are limited to 1 MiB each.
5. `record_scenario` names run, scenario, phase, outcome, three evidence IDs and ordered
   exchanges (`connection`, `observation`). Passing results must cover the declared
   scenario steps. Report actual observations and limitations; the service validates
   references and order, not whether execution or semantic correctness occurred.
6. `complete_mock` names passing mock results for every selected scenario. This moves
   the run to implementation; it is not product acceptance.
7. Replace mock behavior, use `record_component_progress` (`mocked`, `partial`,
   `implemented`) with evidence, rerun scenarios in the implementation phase, and
   `finish_work` with its observed outcome. Work completion does not set component state.
8. `finish_construction` records acceptance or abandonment, decision and evidence.
   Acceptance requires implementation results for the selected scenarios, implemented
   component reports, no open work/findings and root acceptance authority. These are
   workflow checks, not a semantic-validity certificate or production guarantee.

## Feedback and resume

Use `report_finding` with the run, component, affected layer, description, requested
change and evidence. Fix the responsible design through MCP, assess dependents, then
start a successor with the newly chosen tuple when inputs change. `origin_work` can
reference work in that predecessor; obligations, scope and evidence need reassessment.
Use `resolve_finding` with the actual resolution, evidence and optional direct successor.
Record additions, refactoring and retirement as explicit work; deleting a component
from a new graph does not remove its old code, callers or data.

Resume open work and exact inputs from records. Do not infer success from an absent
session. Earlier workflow records remain readable through shared read/history tools
and legacy project/context tools. Do not mix their command schemas with v2.

## Deployment boundary

The local Docker deployment at `http://localhost:9000/mcp` supports this v2 workflow.
The public `https://mcp.mfm.dev/mcp` is a different deployment and was not upgraded
by local dogfooding. Verify capabilities each session. Skill 1.1.0 remains alpha and
`public: false` until its public dependencies are deployed and verified.

OAuth uses the harness login flow and server name from the binding. Reuse an existing
session; if authorization is required, let the user complete it. Do not inspect
unrelated credentials or substitute a development token. A missing project can reflect
a different tenant; it is not permission to move workspace data. If a capability is
absent, record the boundary and continue independent supported work. Implementation
bootstraps must be explicit; never substitute direct HTTP/database mutations or local
design files for MCP authority.
