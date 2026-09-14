"""Factory /v2 commands. Stable identities and content revisions are separate."""

from typing import Annotated, Literal

from pydantic import Field, StringConstraints

from .formats import Architecture, DataModel, Id, Record, Text

Label = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
Revision = Annotated[int, Field(ge=1)]


class CreateSpecVariant(Record):
    type: Literal["create_spec_variant"]
    id: Id
    name: Label
    spec_project_slug: Id
    copied_from: Id | None = None


class CreateArchitectureVariant(Record):
    type: Literal["create_architecture_variant"]
    id: Id
    name: Label
    spec_variant: Id
    copied_from: Id | None = None


class RenameVariant(Record):
    type: Literal["rename_variant"]
    layer: Literal["spec", "architecture"]
    id: Id
    name: Label


class SyncSpec(Record):
    type: Literal["sync_spec_variant"]
    id: Id
    source_revision: Annotated[str, StringConstraints(min_length=1, max_length=200)]


class SaveModel(Record):
    type: Literal["save_model"]
    spec_variant: Id
    spec_revision: Revision
    content: DataModel


class SaveArchitecture(Record):
    type: Literal["save_architecture"]
    architecture_variant: Id
    spec_revision: Revision
    model_revision: Revision
    content: Architecture


class StartConstruction(Record):
    type: Literal["start_construction"]
    id: Id
    spec_variant: Id
    architecture_variant: Id
    spec_revision: Revision
    model_revision: Revision
    architecture_revision: Revision
    scenarios: list[Id] = Field(min_length=1)
    predecessor: Id | None = None
    assessment: Text


class Exchange(Record):
    connection: Id
    observation: Text


class ScenarioResult(Record):
    type: Literal["record_scenario"]
    id: Id
    run_id: Id
    scenario: Id
    phase: Literal["mock", "implementation"]
    outcome: Literal["passed", "failed"]
    code_evidence: Id
    data_evidence: Id
    trace_evidence: Id
    exchanges: list[Exchange] = Field(min_length=1)
    observations: Text


class CompleteMock(Record):
    type: Literal["complete_mock"]
    id: Id
    results: list[Id] = Field(min_length=1)


class ComponentProgress(Record):
    type: Literal["record_component_progress"]
    run_id: Id
    component: Id
    implementation: Literal["mocked", "partial", "implemented"]
    evidence: list[Id] = Field(min_length=1)


class CreateWork(Record):
    type: Literal["create_work"]
    id: Id
    run_id: Id
    component: Id
    task_kind: Literal["prepare", "implement", "integrate", "refactor", "retire", "investigate"]
    instructions: Text
    allowed_changes: list[Text]
    obligations: list[Id] = Field(min_length=1)
    origin_work: Id | None = None


class FinishWork(Record):
    type: Literal["finish_work"]
    id: Id
    outcome: Literal["succeeded", "blocked", "cancelled"]
    evidence: list[Id] = Field(min_length=1)


class Finding(Record):
    type: Literal["report_finding"]
    id: Id
    run_id: Id
    component: Id
    layer: Literal["spec", "model", "architecture", "implementation"]
    description: Text
    requested_change: Text
    evidence: list[Id] = Field(min_length=1)


class ResolveFinding(Record):
    type: Literal["resolve_finding"]
    id: Id
    resolution: Text
    evidence: list[Id] = Field(min_length=1)
    successor: Id | None = None


class FinishConstruction(Record):
    type: Literal["finish_construction"]
    id: Id
    outcome: Literal["accepted", "abandoned"]
    results: list[Id]
    decision: Text
    evidence: list[Id] = Field(min_length=1)


Command = Annotated[
    CreateSpecVariant | CreateArchitectureVariant | RenameVariant | SyncSpec | SaveModel
    | SaveArchitecture | StartConstruction | ScenarioResult | CompleteMock | ComponentProgress
    | CreateWork | FinishWork | Finding | ResolveFinding | FinishConstruction,
    Field(discriminator="type"),
]


class Envelope(Record):
    project_slug: Id
    idempotency_key: Id
    expected_version: int = Field(default=0, ge=0)
    reason: Text
    causes: list[int] = Field(default_factory=list, max_length=100)
    command: Command
