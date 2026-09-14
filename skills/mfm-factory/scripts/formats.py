"""Factory starting formats. Pydantic is authoritative; JSON Schema is generated.

These portable content formats are not the legacy Factory /v1 command payloads.
Service envelopes own variant identity, revision, provenance and construction state.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Id = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_.-]*$")]
Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Cardinality = Literal["one", "zero-or-one", "many", "one-or-more"]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Attribute(Record):
    id: Id
    meaning: Text
    type: Literal["text", "identifier", "integer", "decimal", "boolean", "date", "datetime", "bytes"]
    cardinality: Cardinality = "one"
    rules: list[Text] = Field(default_factory=list)


class Relationship(Record):
    id: Id
    target: Id
    cardinality: Cardinality
    meaning: Text


class Invariant(Record):
    id: Id
    statement: Text


class Concept(Record):
    id: Id
    definition: Text
    spec_refs: list[Id]
    attributes: list[Attribute]
    identity: list[Id] = Field(min_length=1)
    relationships: list[Relationship] = Field(default_factory=list)
    lifecycle: Text
    invariants: list[Invariant] = Field(default_factory=list)


def unique(values, label):
    values = list(values)
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {label}")
    return set(values)


class DataModel(Record):
    format: Literal["mfm-data-model/1"]
    concepts: list[Concept]
    questions: list[Text] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_references(self):
        ids = unique((c.id for c in self.concepts), "concept id")
        unique([*ids, *(i.id for c in self.concepts for i in c.invariants)], "model id")
        for c in self.concepts:
            attrs = unique((a.id for a in c.attributes), f"attribute in {c.id}")
            unique(c.identity, f"identity attribute in {c.id}")
            if not set(c.identity) <= attrs:
                raise ValueError(f"unknown identity attribute in {c.id}")
            unique((r.id for r in c.relationships), f"relationship in {c.id}")
            if any(r.target not in ids for r in c.relationships):
                raise ValueError(f"unknown relationship target in {c.id}")
        return self


class Component(Record):
    id: Id
    parent: Id | None
    responsibility: Text
    spec_refs: list[Id]
    model_refs: list[Id]
    technology: Text | None = None
    deployment: Text | None = None
    allowed_effects: list[Text] = Field(default_factory=list)


class Contract(Record):
    id: Id
    description: Text
    schema_body: dict = Field(alias="schema", description="JSON Schema Draft 2020-12 payload contract")


class Interface(Record):
    id: Id
    component: Id
    role: Literal["provided", "required"]
    kind: Literal["request-response", "event", "data-access"]
    input: Id
    output: Id | None = None
    errors: list[Id] = Field(default_factory=list)
    behavior: Text


class Connection(Record):
    id: Id
    source: Id = Field(description="Required interface id; event source is the publishing requirement")
    target: Id = Field(description="Provided interface id; event target is the receiving handler")
    transport: Literal["in-process", "http", "event", "sql"]
    behavior: Text


class Mapping(Record):
    id: Id
    model_ref: Id = Field(description="Concept or invariant id in the selected Data Model")
    targets: list[Id] = Field(min_length=1, description="Component, interface or contract ids")
    representation: Text


class Ownership(Record):
    component: Id
    repository: Text
    path: Text


class Obligation(Record):
    id: Id
    component: Id
    kind: Literal["contract", "component", "composition", "operational"]
    check: Text


class Step(Record):
    connection: Id
    action: Text
    expect: Text


class Scenario(Record):
    id: Id
    spec_refs: list[Id]
    setup: Text
    steps: list[Step] = Field(min_length=1)
    outcome: Text


class Architecture(Record):
    format: Literal["mfm-architecture/1"]
    stack: dict[str, Text] = Field(description="Chosen technologies and pinned versions; no universal profile registry")
    components: list[Component] = Field(min_length=1)
    contracts: list[Contract]
    interfaces: list[Interface]
    connections: list[Connection]
    mappings: list[Mapping]
    ownership: list[Ownership]
    obligations: list[Obligation]
    scenarios: list[Scenario]
    questions: list[Text] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_graph(self):
        collections = (self.components, self.contracts, self.interfaces, self.connections,
                       self.mappings, self.obligations, self.scenarios)
        unique((n.id for collection in collections for n in collection), "architecture id")
        components = {c.id: c for c in self.components}
        contracts = {c.id for c in self.contracts}
        interfaces = {i.id: i for i in self.interfaces}
        connections = {c.id for c in self.connections}
        if sum(c.parent is None for c in self.components) != 1:
            raise ValueError("containment requires one root")
        for c in self.components:
            visited = set()
            current = c
            while current.parent is not None:
                if current.id in visited:
                    raise ValueError("containment cycle")
                visited.add(current.id)
                if current.parent not in components:
                    raise ValueError("unknown parent component")
                current = components[current.parent]
        for i in self.interfaces:
            if i.component not in components:
                raise ValueError("unknown interface component")
            refs = [i.input, *i.errors, *([i.output] if i.output else [])]
            if not set(refs) <= contracts:
                raise ValueError("unknown interface contract")
        for c in self.connections:
            if c.source not in interfaces or c.target not in interfaces:
                raise ValueError("unknown connection endpoint")
            if interfaces[c.source].role != "required" or interfaces[c.target].role != "provided":
                raise ValueError("connection must link required to provided interface")
            if interfaces[c.source].kind != interfaces[c.target].kind:
                raise ValueError("connection interface kinds must agree")
        targets = set(components) | contracts | set(interfaces)
        if any(not set(m.targets) <= targets for m in self.mappings):
            raise ValueError("unknown mapping target")
        if any(o.component not in components for o in [*self.ownership, *self.obligations]):
            raise ValueError("unknown ownership or obligation component")
        if any(s.connection not in connections for scenario in self.scenarios for s in scenario.steps):
            raise ValueError("unknown scenario connection")
        return self


if __name__ == "__main__":
    destination = Path(__file__).resolve().parents[1] / "references"
    for name, model in (("data-model", DataModel), ("architecture", Architecture)):
        schema = model.model_json_schema(by_alias=True)
        schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        (destination / f"{name}.schema.json").write_text(json.dumps(schema, indent=2) + "\n")
