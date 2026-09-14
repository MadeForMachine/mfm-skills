# Executable mock and feedback loop

## Establish the run

Read the selected spec, Data Model and architecture at exact revisions. Confirm the
user's variant choices, record known gaps and establish the product scenarios to
exercise. A scenario is a flow with setup, interactions and expected outcome; include
important negative, empty, failure and recovery paths. “Complete flow” means end to
end for this stated scope, not all possible paths through the graph.

Retain the actual input tuple in construction records. An unchanged model or
architecture may have older authoring provenance; the agent assesses whether it is
suitable for the selected inputs. That assessment is a judgment, not a certificate.

## First milestone: executable mock product

Build the component boundaries, interfaces and wiring that the architecture declares.
Use lightweight mock behavior behind those boundaries and simulate external systems
through their declared adapters. A screen populated with independent canned responses
does not demonstrate data flowing between components.

Generate synthetic **scenario data** consistent with logical identity, relationships,
invariants and lifecycle. Reuse coherent IDs across interfaces. State changes must
affect subsequent reads and interactions. Record fixture artifacts or a generator
with its version, seed and other required inputs so the same scenario can be replayed.
Keep generated instances with construction evidence, not inside the logical schema.

Execute the agreed scenarios through the actual wiring. Check payload contracts,
expected interactions and final state. Retain an **execution trace** identifying
scenario, run, fixture/generator version, component/interface connections, observations
and outcomes. Tie results to exact code and design revisions. Explain coverage gaps.
The mock milestone is met when required scenarios pass in this scope, with evidence;
the service does not infer it from declarations alone.

## Replace mock behavior

Treat the mock as the initial implementation of the same product. Replace behavior
within a component's boundary while retaining its interface contracts and scenario
checks. Track mocked, partially implemented or implemented behavior separately from
task completion and acceptance. A completed mock task can still describe mocked behavior.

Run component checks and the affected end-to-end scenarios after each replacement.
Parent components own integration within their scope. Include real persistence,
external integrations and operational checks before claiming production completion.
Do not perform actual external transactions simply because a mock scenario covers them;
honor the user's authorization and the environment's test arrangements.

## Correct the design when construction teaches us something

1. Record the finding, affected exact inputs, evidence and resolution responsibility.
2. Correct intent in Spec, meaning in Data Model, or implementation structure/contracts
   in Architecture through MCP. The same authorized agent may perform these roles.
3. Traverse references from changed concepts/components/interfaces to dependent work,
   mappings, scenario data and checks. Document necessary edits and retained choices.
4. Adopt revised inputs explicitly in successor construction work. Reuse code and
   evidence only after assessing their continuing relevance; never rewrite old evidence.
5. Rebuild the affected mock paths or implementation, then rerun checks and record results.

For a removed or replaced component, identify callers, connections, owned files,
persistent data, migration needs and obligations that move or disappear. Retire the
design identity with history intact. Deleting a graph node does not complete the
corresponding code/data removal. Avoid forcing every architecture edit into a new
component identity when its responsibility is unchanged.

On interruption, resume from durable tasks, pinned inputs and last verified results.
An abandoned agent session is not evidence that its task failed or succeeded.
