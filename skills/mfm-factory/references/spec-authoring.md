# Hosted specification authoring

This is the Factory's spec workflow. No local-authoring skill is required.
The Spec service owns working revisions; Factory retains exact synchronized
snapshots. Local Docker hosting does not change that authority.

Read the project binding and discover the actual MCP deployment. Read
`mfm_spec_project` for HEAD and active policy, then `mfm_spec_read(view=map)`.
Read full nodes only for the affected scope; use `view=referrers` before identity
changes. Keep the criterion map visible and assess relevant criteria explicitly.
The bundled [format reference](spec-format.md) explains the portable format;
the deployment's active policy and mutation schema govern admission.

Components own responsibility; features describe observable behavior and link to
needed capabilities; criteria express requirements across the graph; evaluations
record evidence and judgment. Challenge contradictions, missing paths, and excessive
decomposition. Spec describes intent; model and architecture describe meaning and
representation. A request for Factory work may span all three layers.

Name the affected nodes and make one coherent mutation batch. Use
`mfm_spec_validate`, then `mfm_spec_mutate` with the same read `base_rev` and a
meaningful `change_note`. Re-read conflicts and reconcile; do not overwrite a newer
head. Use `mfm_spec_rename`, `merge`, `split`, and `retire` for identity changes,
preserving predecessors and referrers. Discover exact signatures before calls.

Read back the committed revision. Use `sync_spec_variant` with that exact source
revision to publish the Factory snapshot, then verify its record. Assess downstream
model and architecture impact without creating unchanged revisions. If maintaining
a repository export, derive it from the hosted export and verify its content; never
edit it as a substitute for the hosted mutation.

On missing tools or OAuth failure, use the client's supported connection/login flow
for the selected server. Do not assume the server is named `mfm`, switch deployments,
or substitute direct API/database writes. Continue independent authorized work and
state what was not persisted. A construction finding that requires changing a design
must follow the run's user-decision boundary before revising and adopting inputs.
