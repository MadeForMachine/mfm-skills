"""Experimental logical-model structure; no semantic or publication guarantees."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Annotated, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, ValidationError, model_validator


Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Id = Annotated[str, StringConstraints(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class SpecReference(Record):
    id: Id
    revision: Text
    location: Text


class Relationship(Record):
    id: Id
    target: Id
    cardinality: Literal["one", "zero-or-one", "many", "one-or-more"]
    meaning: Text


class Invariant(Record):
    id: Id
    statement: Text


class Concept(Record):
    id: Id
    definition: Text
    identity: Text
    lifecycle: Text
    spec_refs: list[Id] = Field(min_length=1)
    relationships: list[Relationship]
    invariants: list[Invariant]
    open_questions: list[Text]


class Publication(Record):
    actor: Text
    reason: Text


def require_unique(values: list[str], label: str) -> None:
    seen = set()
    for value in values:
        if value in seen:
            raise ValueError(f"duplicate {label}: {value}")
        seen.add(value)


class DataModel(Record):
    format_version: Literal["0.1"]
    id: Id
    title: Text
    revision: Text
    status: Literal["draft", "published"]
    spec: SpecReference
    scope: list[Id] = Field(min_length=1)
    authority: Text
    concepts: list[Concept] = Field(min_length=1)
    open_questions: list[Text]
    publication: Publication | None = None

    @model_validator(mode="after")
    def check_references(self) -> DataModel:
        for revision in (self.revision, self.spec.revision):
            if revision.lower() in {"latest", "head", "main", "master", "current"}:
                raise ValueError(f"revision must not be a moving alias: {revision}")
        ids = [concept.id for concept in self.concepts]
        require_unique(ids, "concept id")
        require_unique(self.scope, "scope reference")
        require_unique(
            [item.id for concept in self.concepts for item in concept.invariants],
            "invariant id",
        )
        known = set(ids)
        for concept in self.concepts:
            require_unique(concept.spec_refs, f"spec reference in {concept.id}")
            require_unique(
                [relation.id for relation in concept.relationships],
                f"relationship id in {concept.id}",
            )
            for relation in concept.relationships:
                if relation.target not in known:
                    raise ValueError(f"{concept.id}.{relation.id}: unknown target {relation.target}")
        if self.status == "draft" and self.publication is not None:
            raise ValueError("a draft cannot carry a publication record")
        if self.status == "published":
            if self.publication is None:
                raise ValueError("a published model requires a publication record")
            if self.open_questions or any(item.open_questions for item in self.concepts):
                raise ValueError("resolve open questions before publishing this model")
        return self


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject silently overwritten definitions, including YAML merge keys."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        seen = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError("YAML mapping keys must be strings")
            if key in seen:
                raise ValueError(f"duplicate YAML key: {key}")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def load_model(path: Path) -> DataModel:
    return DataModel.model_validate(yaml.load(path.read_text(), Loader=UniqueKeyLoader))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, nargs="?")
    parser.add_argument("--schema", action="store_true", help="emit derived JSON Schema")
    args = parser.parse_args()
    if args.schema:
        print(json.dumps(DataModel.model_json_schema(), indent=2))
        return 0
    if args.model is None:
        parser.error("provide model.yaml or --schema")
    try:
        model = load_model(args.model)
    except (OSError, ValueError, ValidationError, yaml.YAMLError) as error:
        print(f"INVALID: {error}")
        return 1
    print(f"VALID structure: {model.id}@{model.revision} ({model.status}), {len(model.concepts)} concepts")
    print("Spec snapshot, semantic rules, compatibility, and publication authority are not verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
