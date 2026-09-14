# MFM Software Factory — Working Glossary

**Status:** Core naming agreed; remaining working distinctions are listed in section 13.

**Date:** 2026-09-14.

**Scope:** Shared vocabulary for Factory design, construction and evaluation.

This dictionary records what we mean within the software-factory discussion. It does not approve an architecture, define a file schema, or claim that the proposed factory exists. Definitions are grouped by subject; bold terms are the preferred names.

The governing order is **Specification → Data Model → Architecture → Construction**. Users develop the specification, data model, and architecture with the responsible agents. Construction agents implement, integrate, and verify within those decisions. Feedback can trigger explicit upstream revisions; adopting changes requires reassessing affected designs, work, and evidence.

Prompt-level restrictions are sufficient for the first version. Stronger sandboxes, formal capability requests, broad benchmarking, and model comparisons are future possibilities. Their inclusion here does not put them into the MVP.

## 1. Purpose and scope

| Term | Meaning for us |
| --- | --- |
| **MadeForMachine (MFM)** | The platform providing skills, tools, durable memory, and deterministic services around the customer's own agent. |
| **Software factory** | The overall workflow from Specification through Data Model and Architecture to Construction, supported by governed design, recursive supervision, context, and a central ledger. |
| **Construction** | Implementing, integrating, and verifying the system against its approved specification, data model, and architecture. |
| **MFM Data Model** | The product supporting centrally governed data-model authoring, revision, inspection, and validation through skills and deterministic services around the customer's agent. |
| **MFM Architecture** | The product supporting independently versioned project architecture variants that preserve the approved specification and data model, through skills and deterministic services around the customer's agent. |
| **MFM Construction** | The product supporting recursive implementation, integration, verification, and supervision by the customer's construction agents and execution harness. |
| **Constrained construction** | Building within declared component boundaries, permitted technologies, and composition rules, while retaining useful freedom inside each component. |
| **System** | A coherent whole with a purpose, an external contract, and an internal composition of components. |
| **Subsystem** | A system considered as a constituent part of a larger system. |
| **System of systems** | A larger system composed of systems that have their own boundaries, contracts, and internal components. Composition can repeat across levels. |
| **Service** | Software exposing a contract across a running service boundary, such as an API. In the MFM platform, services are independently deployable. A component need not be a service. |
| **Architecture** | How the system will satisfy the specification and data model: component responsibilities, interfaces, technologies, deployment, and concrete data representations. |
| **Architecture Template** | A reusable architectural arrangement across projects, deferred until concrete reuse warrants it. It is not required to author, publish, or construct an architecture variant. |
| **Top-down construction** | Progressing through Specification, Data Model, Architecture, and Construction, with explicit upstream decisions when downstream work exposes a conflict. |
| **MVP** | The smallest working version that demonstrates the construction approach with a small system and toolbox. It does not need to implement every concept in this glossary. |

## 2. Intent, specifications, and durable artifacts

| Term | Meaning for us |
| --- | --- |
| **Intent** | The purpose and desired outcomes that explain why a system or feature should exist. |
| **Specification / Spec** | What the system must do, its constraints, and what counts as success. Spec is the accepted abbreviation. The MFM Spec graph can record required responsibilities and design decisions without replacing the factory's separate Data Model and Architecture artifacts. |
| **Data Model** | The system's concepts, identities, relationships, lifecycle rules, and invariants, defining data meaning independently of storage and transport choices. |
| **Logical data model** | Describes the kind of Data Model we mean. Use Data Model as the preferred name; physical schemas and transport layouts belong to Architecture. |
| **MFM Spec** | Our approach to representing and developing specifications as a typed graph, supported by a format, skills, and a hosted service. Use the qualified names below when the distinction matters. |
| **MFM Spec format** | The portable, versioned representation of a specification and its typed relationships. |
| **MFM Data Model 1** | The selected starting content format for logical concepts, attributes, identity, relationships, lifecycle and invariants. It has no model display name or construction status. |
| **MFM Architecture 1** | The selected starting content format for components, containment, interfaces, contracts, connections, concrete mappings, ownership, checks and product scenarios. |
| **Format version** | Identifies the rules for interpreting an artifact, independently of that artifact's content revision or the Factory skill release. |
| **Service envelope** | Stored project/variant identity, revision and authoring provenance surrounding a design's content. It avoids embedding workflow state in the design schema. |
| **Logical attribute** | A named value belonging to a concept, with domain meaning, type, cardinality and applicable rules; it is not a database column definition. |
| **Payload contract** | The declared shape of data exchanged through an interface. The first architecture format uses JSON Schema Draft 2020-12; behavioral meaning remains explicit alongside it. |
| **MFM Spec service** | The hosted, deterministic service that stores, serves, versions, and validates spec changes for the customer's agent. |
| **Requirement** | A behavior, property, or constraint that the system must satisfy. |
| **Feature** | A coherent piece of intended behavior. A feature can involve several components. |
| **Acceptance criterion** | An explicit condition used to decide whether a requirement or feature has been satisfied. |
| **Design criterion** | A quality or trade-off used to guide design judgment, such as diagnosability or simplicity. It need not be mechanically decidable. |
| **Design decision** | A chosen direction together with its rationale and relevant trade-offs. |
| **Artifact** | An identifiable output or input of the construction process, such as a spec, profile, component declaration, source file, or verification report. |
| **Source of truth** | The authoritative artifact for a particular fact. Other representations should derive from it or be checked against it. |
| **Stable identifier** | A persistent handle for an artifact or graph node, used to reference it independently of its display name or location. |
| **Version / Revision** | An identifier for a particular state of an artifact. Exact numbering and compatibility rules depend on the artifact. |
| **Content revision** | A retained change to a spec, model or architecture. User-facing numbering starts at 1 within its history. Unchanged downstream content does not gain a revision merely because an upstream design changed. An empty layer displays “No version yet”. |
| **Variant** | A named alternative with a stable identity and content history. A project has spec variants; each owns one unnamed logical Data Model and any number of named architecture variants. Alternative logical meanings use separate spec variants. |
| **Architecture revision** | An exact version within one architecture variant's history, identified by owning project, architecture identity, and revision. Two variants may use the same revision label without identifying the same design. |
| **Snapshot** | A fixed selection of artifact revisions used together for a task, construction run, or verification. |
| **Provenance** | The recorded origin and derivation of an artifact or result, including relevant source revisions and decisions. |
| **Decision log** | A chronological record of decisions and their reasons. It preserves why the design changed. |

## 3. Components and reusable construction vocabulary

| Term | Meaning for us |
| --- | --- |
| **Component** | A named part of a particular system with a defined responsibility, boundary, and contract. It may contain other components and need not correspond to one file, process, or deployment. |
| **Component instance** | A particular component defined in a system, such as `orders.place`, as opposed to its reusable archetype. Here, instance means a design instance; it does not mean a running object. |
| **Component boundary** | The line separating a component's internal decisions from the interfaces, effects, dependencies, and obligations visible to others. |
| **Responsibility** | The coherent job owned by a component or system. |
| **Archetype / Component archetype** | A reusable definition of an allowed component shape: inputs, outputs, dependencies, lifecycle, effects, contracts, and implementation conventions. Example: Operation. |
| **Component shape** | The required structure and interaction pattern of a component. An archetype defines a permitted shape. |
| **Component type** | The category assigned to a component, such as Operation or Endpoint. An archetype gives that category its detailed rules. |
| **Brick** | A versioned, reusable construction unit with a contract and an implementation or generation mechanism, accompanied by the material needed to use and verify it. This is our working distinction from an archetype, which defines a shape. |
| **Brick family** | A related group of bricks, such as persistence or messaging bricks. It is an organizational category. |
| **Composition** | Connecting components through declared contracts and relationships to form a larger whole. |
| **Module** | A unit of source-code organization. A component may occupy several modules, and a module boundary alone does not establish a component contract. |
| **Interface** | The visible inputs, outputs, and operations through which a component can be used. Its contract additionally describes meaning and obligations. |
| **Dependency** | Something a component requires to fulfill its responsibility, such as another component's interface. Qualify code, build, runtime, or context dependencies when needed. |
| **Dependency direction** | Which component is allowed to rely on which other component. This describes reliance, not necessarily runtime data flow. |
| **Port** | An interface expressing a capability a component provides or requires, without committing the consumer to a concrete implementation. |
| **Adapter** | An implementation that connects a port to a particular technology or external system. |

## 4. Toolbox, profile, and construction rules

| Term | Meaning for us |
| --- | --- |
| **Toolbox** | The versioned collection of technologies, tools, archetypes, bricks, definitions, examples, and templates made available for construction. |
| **Construction profile** | The versioned declaration of which toolbox elements are permitted and how they may be used together, including architecture rules and conventions. The profile governs the available materials. |
| **Approved stack** | The selected languages, engines, frameworks, libraries, and infrastructure technologies. This is one part of a construction profile. |
| **Brick registry** | The versioned catalog through which agents discover bricks and retrieve their definitions and usage material. It can begin as ordinary files in a Git repository. |
| **Registry index** | A compact listing of available registry entries, versions, purposes, and retrieval locations. |
| **Construction grammar** | Rules defining valid component declarations and valid ways to compose them. Structural validity alone does not establish correct behavior. |
| **Convention** | An agreed way of expressing or implementing something, such as error representation or file organization. |
| **Constraint / Rule** | An explicit restriction or obligation. A rule may be communicated through instructions, checked mechanically, or prevented by the environment. |
| **Rule set** | A named, versioned collection of guidance and constraints. State whether it governs spec authoring or software construction. |
| **Project policy** | The project's governing configuration. In the existing MFM Spec service, this selects rules and tool profiles for spec authoring; it does not itself enforce customer source code. |
| **Tool profile** | A selection of agent-facing tools or operations exposed for a workflow. This is narrower than a construction profile. |
| **Allowlist** | An explicit list of permitted elements. Its scope must say whether it covers imports, packages, APIs, effects, or something else. |
| **Structural freedom** | How much authority an agent has over decomposition, file organization, and dependency structure. |
| **Technological freedom** | How much authority an agent has to select or replace technologies. |
| **Algorithmic freedom** | Freedom to implement domain logic within an assigned component's contracts and permitted effects. |
| **Capability** | A behavior or facility needed or supplied by a component or toolbox. Here it is a general construction term, not automatically an Atlas taxonomy entry. |
| **Capability gap** | A requirement that the current toolbox or component design cannot adequately support. It prompts reconsideration in the design dialogue. |
| **Capability request** | An optional formal artifact describing a capability gap and a proposed extension. A dedicated request workflow is not required for the first version. |
| **Compatibility** | The conditions under which versions of contracts, bricks, profiles, and implementations can be used together without violating their obligations. |

## 5. Models, representations, and implementation

| Term | Meaning for us |
| --- | --- |
| **Implementation model** | The component-focused, machine-readable description within Architecture: component instances, interfaces, dependencies, effects, and links to requirements and verification. It is not a competing name for the whole Architecture or another workflow level. |
| **Intermediate representation (IR)** | The implementation model in its role between approved design and source code. Earlier references to architecture IR and implementation IR meant this same concept. |
| **Component model** | Our shorter name for the component-focused implementation model. It does not imply an additional separately maintained artifact. |
| **Component graph** | The components and typed relationships represented by the implementation model. It is a graph view of the model, not necessarily a separate store. |
| **Declaration** | Structured data stating what an element is and what relationships or obligations it has. |
| **Schema** | A machine-readable definition of the permitted structure and values of data or declarations. |
| **Interface representation** | The concrete shape and encoding of data crossing a component boundary, defined in Architecture and reviewed for preservation of Data Model meaning. |
| **Persistence mapping** | The architecture-owned mapping from Data Model concepts to stored records, identifiers, and relationships, reviewed by the central data authority for semantic preservation. |
| **Data custody** | A component's responsibility to store, protect, and operate on its data. Custody does not confer authority to redefine its meaning. |
| **JSON Schema** | A schema language for describing and validating data structure. It can validate YAML declarations after they are parsed into a compatible data model. |
| **YAML** | A human-readable data notation we can use to serialize profiles and component declarations. YAML alone does not define their meaning. |
| **Domain-specific language (DSL)** | A language specialized for a domain. Our declarations, vocabulary, and construction rules together can form a DSL even when their syntax is YAML. |
| **Serialization** | A concrete encoding of a model, such as YAML or JSON. A serialization format and a model are different things. |
| **Implementation** | The concrete code and supporting configuration that realize the component model and satisfy its contracts. |
| **Source code** | The programming-language text of an implementation, whether written by an agent, a human, or a generator. |
| **Template** | A reusable pattern used to produce an artifact or source structure. |
| **Scaffolding** | The initial structural code and files produced from templates or archetype definitions. |
| **Generator / Code generation** | A tool or process that produces artifacts or source code from declarations and templates. Distinguish deterministic generation from agent-authored implementation. |
| **Derivation** | Producing an artifact from a spec or model. In the MFM Spec service design, the service assembles context and the customer's agent produces the derived artifact. |
| **Regeneration** | Producing an implementation again from the current authoritative inputs after a design, toolbox, or implementation choice changes. |
| **Replaceable implementation** | An implementation that can be substituted while retaining the declared intent and compatibility obligations. This depends on preserving the knowledge needed to reproduce the required behavior. |
| **Disposable implementation / Fluid implementation** | Earlier phrases for the replaceable-implementation ambition. They do not mean persistent data, compatibility, or undocumented behavior can safely be discarded. |
| **Migration** | A controlled transition of existing data, configuration, or running behavior to a new version. Regenerating source code alone does not perform that transition. |

## 6. Contracts and component behavior

| Term | Meaning for us |
| --- | --- |
| **Contract** | The explicit assumptions and obligations governing a component or system. Contracts are developed through design dialogue and guide implementation and verification. |
| **Structural contract** | Obligations about shape, interfaces, permitted dependencies, and architectural boundaries. |
| **Behavioral contract** | Required observable behavior for specified inputs, states, and conditions. |
| **Interaction contract** | Obligations governing interactions with other components, including order, allowed effects, and behavior under failures or retries. |
| **Operational contract** | Obligations under stated operating conditions, such as latency, resource use, availability, and observability. |
| **Verification contract** | The obligations to be checked and the evidence required to assess conformance, including the scope and assumptions of the checks. |
| **Invariant** | A property that must remain true over its stated scope and conditions, such as uniqueness within one tenant. |
| **Precondition / Postcondition** | A condition required before an operation / a condition guaranteed after a specified outcome. |
| **Effect / Side effect** | An interaction with state or the outside world, such as a database write, network call, or event emission. |
| **Domain logic** | The rules and calculations specific to the system's purpose. |
| **Input / Output** | Data accepted or returned at a component boundary. |
| **Data transfer object (DTO)** | A structured value used to carry data across an interface. |
| **Result type** | An explicit representation of an operation's success value or declared failure outcome. |
| **Lifecycle** | The stages and transitions of a component or resource, such as initialization, execution, and shutdown. |
| **Failure mode** | A specified way an operation or component can fail, together with its observable consequences. |
| **Observability** | The ability to understand system behavior from emitted evidence such as logs, metrics, and traces. |
| **Trace context** | Identifiers and related information connecting observations across one execution or request. |
| **Transaction / Atomicity** | A unit of work / the guarantee that its specified changes take effect together or do not take effect. The guarantee has an explicit boundary. |
| **Idempotency** | The property that repeating an operation under its defined identity and conditions does not duplicate its intended effect. |
| **Retry** | Another attempt after an unsuccessful or uncertain attempt. Contracts must define its permitted behavior. |
| **Concurrency** | Overlapping operations whose interactions can affect correctness. |
| **Event delivery semantics** | The promises and limits around event loss, duplication, ordering, and redelivery. |

## 7. Example component vocabulary and technical layers

These are examples from the discussion, not an approved initial archetype catalog.

| Term | Meaning for us |
| --- | --- |
| **Endpoint / HTTP endpoint** | A component boundary that receives an HTTP request and returns an HTTP response, translating between transport and application contracts. |
| **Handler** | The callable invoked to handle a request, event, or other trigger. Its role depends on the surrounding archetype. |
| **Operation / Application operation** | A component that executes one application use case by applying domain logic and calling declared ports. |
| **Application service** | A component that coordinates application behavior. Its exact granularity relative to an Operation remains to be settled. |
| **Domain function** | A bounded unit of domain calculation or decision logic. Whether it must be pure is an archetype decision still to be made. |
| **Repository port** | The interface through which a component accesses the persistence capabilities it needs. |
| **Repository adapter** | The concrete implementation of a repository port using a storage technology. Qualify repository to avoid confusion with a source-code repository. |
| **Command / Query** | An operation requesting a state change / an operation requesting information. Their detailed allowed effects belong in their contracts. |
| **Workflow** | A coordinated sequence of steps and state transitions, potentially spanning time and component boundaries. |
| **Event** | A named representation of something that happened, with a defined payload and meaning. |
| **Event publisher / Consumer** | A component that emits events / a component that handles delivered events. |
| **Worker** | A component that performs background work in response to jobs or events. |
| **Scheduler / Scheduled job** | A mechanism that triggers work according to time rules / the work it triggers. |
| **Webhook receiver / Sender** | An endpoint accepting event notifications over HTTP / a component delivering them to an external endpoint. |
| **Projection** | A derived view of authoritative information, shaped for a particular read purpose. Specify data projection or graph projection when needed. |
| **Tool** | A callable capability used to perform work, such as reading a contract, generating files, or running validation. |
| **Library** | Reusable code called by an implementation. |
| **Framework** | A software foundation that supplies application structure and execution conventions. |
| **Wrapper** | An API layer around another implementation that exposes a selected interface or adds behavior. |
| **MFM SDK** | A possible agent-facing set of construction APIs and supporting tools. It is a proposal, not a prerequisite for the first version. |
| **MFM runtime** | Possible shared code that implements MFM construction abstractions while the generated application runs. |
| **Runtime engine** | The program that executes application code, such as Node or a Python interpreter. Distinct from an MFM runtime library. |
| **Infrastructure** | Operating facilities used by the software, such as databases, networks, and deployment environments. |

## 8. Agents and units of work

| Term | Meaning for us |
| --- | --- |
| **Model / LLM** | The inference engine supplying language understanding and generative judgment. Qualify model to distinguish an LLM, Data Model, or implementation model. |
| **Agent** | A model operating through instructions, tools, and a work loop to carry out tasks. |
| **Agent harness** | The surrounding software that supplies instructions and tools, manages execution and context, and records results. |
| **Skill** | Reusable instructions and supporting material that teach an agent how to perform a workflow. |
| **Factory skill** | One user-facing workflow covering project setup, variants, design changes, construction and feedback through MCP. Supporting references contain format detail. It steers the customer's agent and does not run one. |
| **MCP-governed work** | Authoritative design and construction records are read and changed through MCP. The customer's harness still edits code, generates fixtures and executes tests, recording their inputs and evidence through MCP. |
| **Agent role** | The scope and kind of work assigned to an agent. A role does not necessarily require a different model or agent process. |
| **Spec agent** | The role that develops and revises the Specification with participating users through MFM Spec, retaining authority over requirements and business intent. |
| **Data model agent** | The central role that develops and revises the whole-system Data Model with participating users and reviews whether architecture representations preserve its meaning. |
| **Architecture agent** | The role that develops and revises alternative project Architectures with participating users, preserving the governing Specification and Data Model and routing conflicts upstream. |
| **Construction agent** | A reusable task-oriented role instantiated for one system's preparation, implementation, investigation, integration, repair, or recovery. Invocations can end between tasks; system ownership persists independently of harness communication routes. |
| **Implementation agent** | A construction agent performing an implementation task. It does not name an additional design authority or factory level. |
| **Data model authority** | The centrally designated role governing data meaning for the whole system with participating users. Component workers may report defects and recommend changes but cannot publish competing meanings. |
| **Test agent / Repair agent** | An agent working on verification material / an agent addressing specific findings. These are roles, not mandatory separate services. |
| **Specialized agent** | An agent configured for a bounded domain or role through its instructions, tools, and context. Specialization does not necessarily require model training. |
| **Task** | A bounded assignment with an objective, target, permitted changes, inputs, and completion conditions. Here it means a factory work item, not necessarily a Codex conversation. |
| **Task target** | The artifact or set of artifacts the task concerns, such as `orders.place`. It identifies what the work addresses, not what action to perform. |
| **Task kind** | The action being performed, such as design, implementation, testing, repair, or investigation. |
| **Authority boundary** | The decisions and artifacts an agent may change in its current role. Implementation authority does not automatically include redesigning the toolbox. |
| **Construction realization** | The exact design and verification inputs retained for construction, including the spec variant's Specification and Data Model snapshots, its selected Architecture variant and revision, and required profile and bricks. It is internal provenance that can be used by multiple runs, not a compatibility certificate or a separate user selection workflow. |
| **Construction run** | One recorded attempt to produce software from a construction realization under a particular harness configuration. Progress and evidence identify both the realization and run. |

## 9. Graphs and context

| Term | Meaning for us |
| --- | --- |
| **System knowledge** | The available specs, models, contracts, policies, implementations, and evidence relevant to the system. It is the information pool from which task context is selected. |
| **Knowledge graph** | A representation of relevant artifacts and concepts as nodes connected by typed relationships. It does not require a graph database. |
| **Node / Edge** | An identifiable entity in a graph / a relationship between entities. |
| **Typed relationship** | A relationship with an explicit meaning, such as `depends-on`, `implements`, `constrained-by`, or `verified-by`. |
| **Dependency graph** | The graph view showing what depends on what. It is one view of system knowledge, not necessarily a separate maintained model. |
| **Architecture graph** | Components and declared interfaces connected by explicit relationships, authored once and projected for visualization, construction context and impact analysis. It does not require a graph database. |
| **Containment tree** | A single-root, acyclic ownership hierarchy. It identifies enclosing integration scopes and is separate from runtime interaction. |
| **Interface connection** | An explicit link from a required interface to a provided interface, identifying transport and behavior. Runtime connections can form cycles. |
| **Required / Provided interface** | A capability a component needs / offers. For events, a publisher requires delivery and a receiving handler provides the receiving capability. |
| **Impact assessment** | Following design references to identify affected models, architectures, components, scenarios, data and construction work after a change. It is agent judgment, not a compatibility certificate. |
| **Graph traversal** | Following relationships from selected nodes according to explicit rules. |
| **Context** | The information available to an agent while performing a task. |
| **Context window** | The model's bounded capacity to process context during inference. It is a model limit, not a declaration of what a task needs. |
| **Context boundary** | The declared knowledge needed to work on a component for a particular kind of task, and what can remain encapsulated elsewhere. |
| **Context declaration** | Explicit references and selection rules that help determine an artifact's task context. Derive references from existing model relationships where possible. |
| **Context resolver** | A deterministic mechanism that selects and assembles context using the task target, task kind, graph relationships, policies, and artifact revisions. |
| **Context bundle** | The concrete package of information assembled for one task. Context package means the same thing. |
| **Minimal sufficient context** | Context containing what the task needs while excluding unnecessary material. Small token count alone does not establish sufficiency. |
| **Context expansion** | Retrieving additional information when a task needs more than its initial bundle. |
| **Context miss** | Necessary information absent from the context supplied for a task. A request for more information is a possible signal, not proof of a miss. |
| **System noise** | Information present in a task's context that does not help perform the task and makes relevant material harder to identify. |
| **Coupling / Hidden coupling** | Reliance between parts of a system / reliance missing from the declared boundaries or relationships. |
| **Semantic compression** | Reusing known, versioned definitions so that shared meaning need not be explained repeatedly. A brick identifier helps only when its definition is available to the agent. |
| **Implementation entropy / Context entropy** | Informal phrases for uncontrolled variation in construction choices / uncertainty about what knowledge matters. We have not defined them as mathematical metrics. |

## 10. Verification, feedback, and enforcement

| Term | Meaning for us |
| --- | --- |
| **Verification** | Checking an artifact or running system against stated obligations and recording the result within an explicit scope. |
| **Validation** | In our tooling vocabulary, evaluating an artifact against declared schemas, rules, or checks. Use a qualifier such as schema validation or behavior validation. |
| **Validator** | A tool that evaluates a defined set of checks and produces findings. |
| **Verification model** | The organization of obligations, checks, and evidence and their links to requirements and components. It need not be a separate database or artifact. |
| **Finding** | A structured observation from verification, identifying the affected artifact, relevant rule, observed condition, and expected condition. |
| **Violation** | A finding that a stated obligation has been broken. |
| **Verification evidence** | Recorded results tied to the artifacts, checks, versions, and conditions evaluated. |
| **Spec conformance** | The extent to which a model or implementation satisfies the specification. Different obligations require different kinds of evidence. |
| **Independent component verification** | Checking a component against its contract while representing external dependencies through controlled interfaces and stated assumptions. |
| **Composition verification** | Checking that connected components satisfy their joint obligations, including interactions that isolated checks cannot establish. |
| **Independent acceptance checks** | Evaluation checks whose authority and expected outcomes are not controlled by the implementation being evaluated. |
| **Static analysis** | Examining declarations or code without executing the application to detect particular properties or violations. |
| **Test** | An executable check of specified behavior or properties under selected conditions. |
| **Formal proof** | A mathematical demonstration of a stated property under explicit assumptions. Passing ordinary tests is not a general proof of correctness. |
| **Repair loop** | Repeating implementation changes and relevant verification in response to specific findings. |
| **Design feedback loop** | A construction finding leads to an explicit Spec, Data Model or Architecture correction, reassessment of downstream work, adoption of revised inputs and renewed construction/verification. |
| **Executable mock product** | The first construction milestone: a runnable product whose declared component interfaces and wiring carry coherent data through the agreed end-to-end scenarios, while behavior and external dependencies may be mocked. |
| **Mock behavior** | A controlled substitute behind a declared interface. It must preserve the scenario's state changes and observable contract; unrelated canned screen responses do not demonstrate a complete flow. |
| **Product scenario** | A repeatable flow defined by setup, exchanges between interfaces, expected observations and final outcome. Complete flow means end to end for the declared scenario scope, including selected failure paths. |
| **Scenario data** | Agent-generated synthetic instances that satisfy the relevant logical model and remain coherent across the scenario's components and state changes. |
| **Fixture** | Retained scenario data and setup that can be replayed. A generator can replace a stored fixture when its exact version, seed and other required inputs are retained. |
| **Execution trace** | Evidence of a scenario's observed component/interface exchanges and outcomes, tied to exact design, code and scenario-data inputs. |
| **Implementation state** | Whether a component's behavior is mocked, partially implemented or implemented. This is distinct from task completion, verification results and acceptance. |
| **Mock replacement** | Implementing real behavior behind a previously mocked boundary and rerunning affected contract and product-scenario checks. |
| **Component retirement** | Ending a component's current responsibility while retaining its historical identity. Callers, ownership, code and persistent data require explicit reassignment, migration or removal work. |
| **Successor run** | New construction work that explicitly adopts changed design inputs and records its predecessor. Reused implementation and evidence are reassessed; earlier results keep their original meaning. |
| **Architectural drift** | Implementation or model changes that depart from the governing architecture without corresponding design revision. |
| **Sandbox** | An execution environment that restricts accessible resources or permitted actions. It is distinct from the construction profile describing design rules. |
| **Prompt restriction** | Communicating rules through agent instructions. This is sufficient as the initial restriction mechanism for our factory. |
| **Mechanical enforcement** | Using tools or environmental controls to detect or prevent violations. Always distinguish detected violations from actions that are actually prevented. |
| **Enforcement levels 0–4** | The earlier experiment labels: instructions; supplied repository materials; restricted dependencies; restricted construction APIs; declarative structural construction. They are not a required rollout sequence. |

## 11. Evaluation vocabulary

These terms describe future measurements. Exact units, scopes, and thresholds remain to be defined for each experiment.

| Term | Meaning for us |
| --- | --- |
| **Benchmark / Benchmark suite** | A repeatable evaluation task / a collection of such tasks with fixed inputs and acceptance checks. |
| **Experiment variant** | One configuration being compared, such as a stack with instructions versus the same stack with validators. |
| **Ablation** | A comparison that removes or changes one mechanism to help identify its contribution. |
| **Expressiveness** | The range of required systems and behaviors a construction profile can represent and support. |
| **Implementation variance** | Differences between implementations produced from the same intended inputs. Distinguish meaningful differences from generated scaffolding. |
| **Cross-run similarity** | The measured resemblance between results of repeated construction runs. Similarity alone does not establish correctness. |
| **Change amplification** | The amount of implementation and design work caused by a requirement change, relative to its intended scope. |
| **Regression** | Previously satisfied behavior broken by a change. |
| **Repair cost** | The effort, time, tokens, and human intervention needed to resolve failures. |
| **Contextual surface area** | The amount and spread of knowledge needed to modify a component safely for a specified task kind. |
| **Context footprint** | The size of the context supplied for a task, usually measured in tokens. |
| **Context fan-in** | The number of external concepts or artifacts the task requires. |
| **Context fan-out** | The number of components potentially affected by a change to the target. This measures change impact, not output tokens. |
| **Context locality** | The share of required knowledge contained within the target component's declared boundary. |
| **Context stability** | How often required contextual artifacts change independently of the target component. |
| **Context completeness** | Whether the assembled bundle contains the information necessary to complete the specified task correctly. |
| **Context retrieval / Repository exploration** | Additional information fetched during work / searching and reading beyond the supplied bundle in the source repository. |
| **Token consumption** | Tokens used during a task or run. Supplied, retrieved, and generated tokens should be distinguished where the harness supports it. |
| **Construction time / Build time** | Elapsed time to produce an accepted result / time spent compiling or packaging software. Qualify the earlier ambiguous phrase build time. |
| **Code volume / Dependency count** | Amount of code / number of dependencies, with generated versus authored code and direct versus transitive dependencies reported separately. |
| **Test coverage** | The behavior or code exercised by tests according to a specified coverage measure. It does not establish correctness by itself. |
| **Mutation survival** | The share or count of valid, deliberately introduced changes that the tests fail to detect. |
| **Unsupported invention** | Introducing an undeclared dependency or capability, or relying on an interface that does not exist. |
| **Adversarial requirement / Capability probe** | A deliberate test of how the construction process handles pressure on its boundaries or a potentially unsupported requirement. |

## 12. One example connecting the terms

- The **Specification** says a customer can place an order and describes the required behavior and success conditions.
- The **Data Model** defines order identity, line items, monetary meaning, relationships, and permitted lifecycle transitions.
- An **Architecture variant** defines components, interfaces, technologies, deployment, and concrete data representations that preserve the Data Model. Another variant may choose a different arrangement from the same governing inputs; each has its own revision history.
- Within Architecture, the **toolbox** supplies construction materials and the **construction profile** selects permitted technologies and composition rules.
- The **Operation archetype** defines the allowed shape of an application operation.
- A reusable **brick** may supply a transaction mechanism needed by several operations.
- The **implementation model** declares `orders.place` as a **component instance**, with its contracts and dependencies.
- The **task** is to implement that component; the **task target** is `orders.place`; the **task kind** is implementation.
- The **context resolver** follows relevant references and assembles the **context bundle** at selected revisions.
- The first **executable mock product** passes a coherent order through the declared interfaces using generated **scenario data**, recording the observed exchanges in an **execution trace**.
- **Mock replacement** introduces real behavior one component at a time, retaining scenario checks. A discovered missing cancellation rule can trigger a **design feedback loop** and a **successor run**.
- The **construction agent** writes the component's domain logic within its declared boundary; its parent owns integration and acceptance of the immediate children.
- **Validators** and **tests** produce **findings** and **verification evidence** for the component and its composition.

## 13. Naming conventions and remaining alignment

Use **Specification → Data Model → Architecture → Construction** for the four levels, and **MFM Spec**, **MFM Data Model**, **MFM Architecture**, and **MFM Construction** for the products. These names identify responsibilities without prescribing a deployment topology or claiming all four products are implemented.

Use **Data Model** as the name and “logical data model” only to explain its scope. Use **Architecture** in place of the earlier **Architecture Realization**. Use **variant** as a qualifier for alternatives and **revision** for a version within an alternative's history. **Architecture Template** names deferred reuse across projects, not a required workflow step. The operational term **construction realization** means the pinned input set, not an alternative name for Architecture. Earlier journal entries and evaluations retain their historical wording.

Use **implementation model** as the primary name; **IR** and **component model** refer to that same concept here. Use **context bundle** rather than alternating with context package. Use **component instance** when contrasting a particular system part with an archetype or brick. Qualify **model**, **repository**, **runtime**, and **profile** when their meaning could be ambiguous.

Three definitions remain deliberate working proposals:

1. **Archetype versus brick:** archetype means reusable shape; brick means a reusable implementation or generation unit. Earlier discussion sometimes used brick for both.
2. **Toolbox versus construction profile:** toolbox means available materials; profile means their permitted selection and use. They can be packaged together without being synonyms.
3. **Application service versus operation:** both appeared in examples, but their exact relationship has not been chosen. This glossary does not introduce an extra layer between them.

Historical names such as **Specifold** appear in the source discussion. Use **MFM Spec** for the current specification work; the historical names do not introduce additional factory stages.

## Authority and use

This glossary is the reusable vocabulary shipped with Factory skill v1. Its terms
describe the selected workflow and explicitly marked future possibilities; they do
not assert that every deployment implements those capabilities. Read the skill's
[capability notes](../mcp.md) before acting and [starting formats](formats.md) when
authoring model or architecture content. The owning project's spec defines its intent.
