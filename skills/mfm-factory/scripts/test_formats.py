"""Checks of construction-relevant graph invariants, not semantic certification."""

import copy
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from formats import Architecture, DataModel


@pytest.fixture
def example():
    return json.loads((Path(__file__).parents[1] / "references/example.json").read_text())


def test_example_and_schema_roundtrip(example):
    for name, model in (("data_model", DataModel), ("architecture", Architecture)):
        parsed = model.model_validate(example[name])
        assert model.model_validate_json(parsed.model_dump_json(by_alias=True)) == parsed


def test_model_rejects_unknown_identity_and_relationship(example):
    model = example["data_model"]
    model["concepts"][0]["identity"] = ["missing"]
    with pytest.raises(ValidationError, match="unknown identity"):
        DataModel.model_validate(model)
    model["concepts"][0]["identity"] = ["id"]
    model["concepts"][0]["relationships"] = [{"id": "customer", "target": "customer", "cardinality": "one", "meaning": "Purchaser"}]
    with pytest.raises(ValidationError, match="unknown relationship"):
        DataModel.model_validate(model)


def test_containment_cycle_rejected_but_runtime_cycle_allowed(example):
    arch = example["architecture"]
    broken = copy.deepcopy(arch)
    broken["components"][1]["parent"] = "orders"
    broken["components"][2]["parent"] = "web"
    with pytest.raises(ValidationError, match="containment cycle"):
        Architecture.model_validate(broken)
    arch["interfaces"] += [
        {"id": "notify", "component": "orders", "role": "required", "kind": "event", "input": "order-payload", "behavior": "Notify UI"},
        {"id": "receive", "component": "web", "role": "provided", "kind": "event", "input": "order-payload", "behavior": "Receive update"},
    ]
    arch["connections"].append({"id": "update", "source": "notify", "target": "receive", "transport": "event", "behavior": "Deliver confirmation"})
    assert len(Architecture.model_validate(arch).connections) == 2


@pytest.mark.parametrize("mutation, error", [
    (lambda a: a["interfaces"][0].update(input="missing"), "unknown interface contract"),
    (lambda a: a["connections"][0].update(target="missing"), "unknown connection endpoint"),
    (lambda a: a["connections"][0].update(source="orders-place"), "required to provided"),
    (lambda a: a["scenarios"][0]["steps"][0].update(connection="missing"), "unknown scenario connection"),
    (lambda a: a["components"].append(copy.deepcopy(a["components"][1])), "duplicate architecture id"),
])
def test_graph_rejects_dangling_and_ambiguous_references(example, mutation, error):
    arch = example["architecture"]
    mutation(arch)
    with pytest.raises(ValidationError, match=error):
        Architecture.model_validate(arch)


def test_questions_and_no_domain_data_are_valid():
    assert DataModel(format="mfm-data-model/1", concepts=[], questions=["Does this product retain domain data?"]).concepts == []


def test_format_cannot_be_implicitly_assigned(example):
    del example["data_model"]["format"]
    with pytest.raises(ValidationError, match="format"):
        DataModel.model_validate(example["data_model"])


def test_model_references_cannot_be_ambiguous(example):
    example["data_model"]["concepts"][0]["invariants"][0]["id"] = "order"
    with pytest.raises(ValidationError, match="duplicate model id"):
        DataModel.model_validate(example["data_model"])
