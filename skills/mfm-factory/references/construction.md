# Pull construction and evidence

Discover the deployed schema first. Current construction uses `/v3/factory` and
separate mock and product runs. `/v2` retains earlier combined-phase runs as history;
never use `complete_mock` to claim the new separate mock acceptance.

## Exact inputs and assignments

Select the user's spec and architecture variants. Read the exact spec/model/architecture
and assess contradictions, incomplete contracts and scenario coverage. No semantic
certificate is required. `start_run` pins those revisions and `deliverable: mock` or
`product`. Product construction must explicitly adopt an accepted mock. A paused
predecessor keeps its successor paused until user resolution explicitly adopts it.

The initial plan names every architecture component exactly once with bounded instructions,
explicit sibling order and whether permitted child-contract preparation is needed.
The current trial architecture requires every direct child for integration. Designs that
need different dependency semantics must state and implement that choice before construction.
Every trial system has a declared verification obligation. Starting a run does not authorize
changing settled contracts, the ownership tree or logical meaning.

## One fresh invocation per claim

Call `claim_next_work` for the run. It atomically returns one eligible assignment with
an opaque token, generation, expiry and bounded context. It may instead return an explicit
no-work reason: paused/accepted, active claims, waiting children, recovery required or blocked.
Do not infer completion from no eligible work. The client chooses its parallelism and starts
workers; Factory never launches agents, requires a broker or keeps a server supervisor.

Each invocation owns exactly one system. Use its exact state version, assignment,
pinned inputs, boundaries, permitted changes, obligations, scenario data and complete
direct-child state/result/issue snapshot. Do not copy a parent conversation or all
descendant history. Additional `lookup_context` calls record exact revision provenance;
reading newer material does not adopt it or expand writable scope.

A preparation worker only supplies bounded direct-child instructions within the architecture's
explicit freedoms and reports `prepared`. Sufficient designs skip preparation and enable
eligible leaves immediately. Preparation does not accept the parent. Leaf workers construct
their own executable behavior. Fresh parent workers integrate exact required child result IDs.
Parents do not change child internals or progress.

Submit `report_system` with the claim ID, token, generation, `expected_version` from its
context, stable report/retry IDs, requested transition and concise reasoning summary/evidence.
Reports can deliver results with exact artifact identities, child results and passing declared
checks; report a blocker; propose/escalate a named issue; or record interruption. Report,
admitted state, results/issues, ledger, audit and retry receipt commit together.

**End the invocation after reporting.** Delegation, blockers and repairs needing child action
always lead to a fresh worker. A parent never remains waiting with its prior context. Claim
expiry marks execution uncertain, not failed or successful. Set `recover_expired: true` only
when deliberately recovering that uncertainty; a fresh generation fences the old attempt.
No exactly-once external execution is promised; inspect filesystem/side effects on recovery.

## Feedback and design pauses

Every issue keeps its origin, route, decisions and evidence. Parent resolution sees all
unresolved direct-child issues, including several blocked siblings. It may resolve actionable
feedback while other siblings work. Each action names the issue version in the claim snapshot;
newly arriving feedback stays pending. Proposed repair is not resolution: fresh affected-system
workers verify it, then fresh parent workers verify required composition.

Construction-local issues escalate one parent edge per report. A spec/model/architecture flaw
immediately pauses the whole run. `route_design_issue` records one explanation/escalation edge
while paused, without a construction claim or progress. New claims cannot execute; late reports
can retain evidence without advancing progress. The harness stops active workers safely and
records interruption; Factory cannot halt external processes.

Surface the actionable issue, evidence and required decision to the user. Only their explicit
resolution with a design agent permits `resolve_design_pause`. Explain every direct-parent
step before root resolution. Resume unchanged inputs only after reassessment; changed inputs
use an explicit successor. Publishing a design revision alone never resumes work.

## Executable mock and separate acceptance

Build executable components and actual wiring, with external systems replaced at their
explicit adapter boundaries. Generate coherent synthetic instances and retain generator/seed,
code identity and actual input/output traces. Static screens or independent canned responses
are insufficient. Validate payloads and important success, failure, empty and recovery paths.

`record_scenario` records exact run scope, ordered connection observations and retained code,
data and trace evidence. `accept_run` requires all selected scenarios to pass, current verified
component compositions, no unresolved issues and no active/unrecovered attempts. It accepts
only that run's deliverable and scope. Reported evidence remains caller-reported judgment,
not a service-issued correctness certificate or production readiness claim.

The present Factory experiment stops at an executable mock. Future actual-product work is a
separate user-initiated run explicitly adopting the accepted mock, then replacing behavior
and rerunning applicable component, integration, persistence and operational checks.

## Corrections and resume

Record findings through MCP. Correct spec intent, model meaning or architecture mappings in
their owning hosted layer. Assess downstream impact and explicitly adopt successor inputs.
Preserve old work/evidence. Source retirement requires explicit code/data/caller migration;
removing a graph node alone does not perform it. Resume from recorded assignments, claims,
issues and exact inputs rather than conversation memory. Keep unobserved harness actions
and the difference between simulated and actual agent execution explicit.
