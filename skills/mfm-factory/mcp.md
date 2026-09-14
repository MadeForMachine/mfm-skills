# MCP operations and capability boundary

Inspect the live tool signatures and schemas; these names are discovery anchors,
not permission to invent parameters or supported command variants.

| Work | Tools |
| --- | --- |
| Hosted spec policy and reading | `mfm_spec_project`, then `mfm_spec_read` (`map`, `node`, `subtree`, `referrers`) |
| Hosted spec changes | `mfm_spec_validate`, then `mfm_spec_mutate`, using the same `base_rev` and coherent operations |
| Spec identity changes | `mfm_spec_rename`, `mfm_spec_merge`, `mfm_spec_split`, `mfm_spec_retire` |
| Spec portability and history | `mfm_spec_import` for explicit bootstrap; `mfm_spec_export` for mirrors; `mfm_spec_history` |
| Factory capability and current state | `mfm_factory_schema`, `mfm_factory_project` |
| Exact records, graph and context | `mfm_factory_read`, `mfm_factory_graph`, `mfm_factory_context` |
| Typed commands and observations | `mfm_factory_mutate`, `mfm_factory_history`, `mfm_factory_changes` |

The Spec tools accept a `params` object; Factory tool parameters are direct.
Tenant identity comes from authentication, never from a caller-invented argument.
The project binding identifies the project, not access authority. Keep exact revision
IDs and returned pagination checkpoints; never resolve separate pages against moving HEADs.

On OAuth failure, trigger the harness's login flow. In Codex, run `codex mcp login`
with the server name from the project's binding (for example, `mfm` or `mfm-local`)
and let the user approve the browser request. Retry after it completes. If transport
state remains stale, report that a refreshed connection/session is needed. Do not
substitute a local development token or inspect unrelated credentials.

For Factory mutations, read the command schema and relevant record version first.
Supply the reason, expected version and causal references supported by that command.
Preserve the exact request and idempotency key when retrying an uncertain response;
a changed decision needs a new key. On a conflict, re-read and assess before retrying.
Read back persisted results. Context reads expand knowledge, not write authority.

## Deployment selection and initial capability limits, 2026-09-14

Service-backed specs can run locally in Docker or on a public deployment. Use the
project's actual service binding. The public `https://mcp.mfm.dev/mcp` connection and
the local `http://localhost:9000/mcp` connection reach different stores and authentication
environments. A missing project in one does not mean it is missing in the other.

The public `mfm` connection exposed Spec tools but no Factory tools at initial inspection;
the local Docker deployment registered both. Workspace identity matters independently
of the endpoint: synthetic development records can exist in a different tenant from
the signed-in user. A missing project is not permission to bypass authentication or
move another workspace's data. Confirm the binding and use an authorized bootstrap
when establishing the user's project in that workspace. Preserve prior history.
The legacy Factory `/v1` schemas still require transitive
spec/model/architecture equality and semantic-review mappings. They do not implement
the selected independent input tuple, named-variant workflow or new portable formats.

Do not claim the complete workflow is operational until live discovery supports:

- Project setup and named spec/architecture variants with one model per spec variant.
- Read, validate, mutate and retain design content in the selected formats.
- Construction from an explicit spec/model/architecture tuple, without a compatibility certificate.
- Mock milestone, scenario data and trace evidence, and implementation progress per component.
- Feedback, successor runs and work to add, replace or retire components.

Use existing compatible commands for supported work. Missing capabilities require
implementation through an explicitly recorded bootstrap task, using available hosted
spec operations first. Do not weaken frozen `/v1` contracts to make the new workflow
look supported; introduce a versioned contract or deliberate migration preserving history.

The skill is version 1.0.0 with alpha maturity and is excluded from public distribution
until its end-to-end MCP workflow has been verified. Recheck live capabilities
each session rather than treating this dated observation as permanent.
