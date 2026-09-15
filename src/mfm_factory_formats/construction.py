"""Factory /v3 pull construction. /v2 commands retain their earlier meaning."""

from typing import Annotated, Literal

from pydantic import Field, model_validator

from .formats import Id, Record, Text


class SystemPlan(Record):
    system: Id
    instructions: Text
    sibling_order: int = Field(ge=0)
    preparation_required: bool = False


class StartRun(Record):
    type: Literal["start_run"]
    id: Id
    spec_variant: Id
    architecture_variant: Id
    spec_revision: int = Field(ge=1)
    model_revision: int = Field(ge=1)
    architecture_revision: int = Field(ge=1)
    deliverable: Literal["mock", "product"]
    adopted_mock: Id | None = None
    predecessor: Id | None = None
    scenarios: list[Id] = Field(min_length=1)
    plan: list[SystemPlan] = Field(min_length=1)
    assessment: Text


class ClaimWork(Record):
    type: Literal["claim_next_work"]
    run_id: Id
    lease_seconds: int = Field(default=900, ge=10, le=3600)
    recover_expired: bool = False


class Check(Record):
    obligation: Id
    outcome: Literal["passed", "failed", "unavailable"]
    evidence: list[Id] = Field(min_length=1)


class ChildInstruction(Record):
    system: Id
    instructions: Text


class IssueAction(Record):
    issue_id: Id
    version: int = Field(ge=1)
    action: Literal["propose", "escalate"]
    explanation: Text


class ReportSystem(Record):
    type: Literal["report_system"]
    id: Id
    run_id: Id
    system: Id
    claim_id: Id
    token: Text
    generation: int = Field(ge=1)
    transition: Literal["prepared", "delivered", "blocked", "resolved", "interrupted"]
    summary: Text
    evidence: list[Id] = Field(min_length=1)
    artifact: Text | None = None
    checks: list[Check] = Field(default_factory=list)
    child_results: dict[Id, Id] = Field(default_factory=dict)
    child_instructions: list[ChildInstruction] = Field(default_factory=list)
    issue_category: Literal["construction", "spec", "model", "architecture"] = "construction"
    actions: list[IssueAction] = Field(default_factory=list)


class ResolvePause(Record):
    type: Literal["resolve_design_pause"]
    run_id: Id
    decision: Text
    assessment: Text
    evidence: list[Id] = Field(min_length=1)
    successor: Id | None = None


class RouteDesignIssue(Record):
    type: Literal["route_design_issue"]
    issue_id: Id
    system: Id
    explanation: Text
    evidence: list[Id] = Field(min_length=1)


class Exchange(Record):
    connection: Id
    observation: Text


class ScenarioResult(Record):
    type: Literal["record_scenario"]
    id: Id
    run_id: Id
    scenario: Id
    outcome: Literal["passed", "failed"]
    code_evidence: Id
    data_evidence: Id
    trace_evidence: Id
    exchanges: list[Exchange] = Field(min_length=1)
    observations: Text


class AcceptRun(Record):
    type: Literal["accept_run"]
    run_id: Id
    results: list[Id] = Field(min_length=1)
    evidence: list[Id] = Field(min_length=1)
    decision: Text


class LookupContext(Record):
    type: Literal["lookup_context"]
    id: Id
    claim_id: Id
    design_ids: list[Text] = Field(min_length=1, max_length=20)


Command = Annotated[
    StartRun | ClaimWork | ReportSystem | ResolvePause | RouteDesignIssue | ScenarioResult | AcceptRun | LookupContext,
    Field(discriminator="type"),
]


class Envelope(Record):
    project_slug: Id
    idempotency_key: Id
    reason: Text
    expected_version: int = Field(default=0, ge=0)
    causes: list[int] = Field(default_factory=list, max_length=100)
    command: Command

    @model_validator(mode="after")
    def unique_lists(self):
        c = self.command
        for name in ("scenarios", "results", "design_ids"):
            values = getattr(c, name, [])
            if len(values) != len(set(values)):
                raise ValueError(f"duplicate {name}")
        return self
