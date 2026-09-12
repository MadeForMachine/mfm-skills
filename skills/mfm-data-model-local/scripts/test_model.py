"""Structural checks that guard authored definitions without judging semantics."""

from copy import deepcopy

import pytest
import yaml
from pydantic import ValidationError

from .model import DataModel, UniqueKeyLoader


@pytest.fixture
def draft():
    return {
        "format_version": "0.1",
        "id": "allocation-model",
        "title": "Allocation model",
        "revision": "draft-001",
        "status": "draft",
        "spec": {"id": "allocation", "revision": "snapshot-001", "location": "../spec"},
        "scope": ["allocation"],
        "authority": "The data-design role with the project users.",
        "concepts": [{
            "id": "resource",
            "definition": "A resource available for allocation.",
            "identity": "Project and resource identity.",
            "lifecycle": "Registered, available, then retired.",
            "spec_refs": ["allocation"],
            "relationships": [],
            "invariants": [{"id": "capacity-nonnegative", "statement": "Capacity is never negative."}],
            "open_questions": ["Which units measure capacity?"],
        }],
        "open_questions": [],
    }


def test_draft_preserves_unresolved_semantics(draft):
    model = DataModel.model_validate(draft)
    assert model.concepts[0].open_questions == ["Which units measure capacity?"]
    assert model.publication is None


def test_duplicate_concepts_fail(draft):
    draft["concepts"].append(deepcopy(draft["concepts"][0]))
    with pytest.raises(ValidationError, match="duplicate concept id"):
        DataModel.model_validate(draft)


def test_invariant_ids_are_model_wide(draft):
    second = deepcopy(draft["concepts"][0])
    second["id"] = "other-resource"
    draft["concepts"].append(second)
    with pytest.raises(ValidationError, match="duplicate invariant id"):
        DataModel.model_validate(draft)


def test_dangling_relationship_fails_but_recursive_relationship_is_valid(draft):
    relation = {"id": "parent", "target": "missing", "cardinality": "zero-or-one", "meaning": "Containing resource."}
    draft["concepts"][0]["relationships"] = [relation]
    with pytest.raises(ValidationError, match="unknown target missing"):
        DataModel.model_validate(draft)
    relation["target"] = "resource"
    assert DataModel.model_validate(draft).concepts[0].relationships[0].target == "resource"


@pytest.mark.parametrize("field,value", [("identity", " "), ("spec_refs", []), ("table_name", "resources")])
def test_blank_missing_provenance_and_unknown_fields_fail(draft, field, value):
    draft["concepts"][0][field] = value
    with pytest.raises(ValidationError):
        DataModel.model_validate(draft)


@pytest.mark.parametrize("alias", ["latest", "HEAD", "main"])
def test_moving_source_revisions_fail(draft, alias):
    draft["spec"]["revision"] = alias
    with pytest.raises(ValidationError, match="moving alias"):
        DataModel.model_validate(draft)


def test_publication_requires_record_and_resolved_questions(draft):
    draft["status"] = "published"
    with pytest.raises(ValidationError, match="publication record"):
        DataModel.model_validate(draft)
    draft["publication"] = {"actor": "Authorized project user", "reason": "Reviewed the initial model."}
    with pytest.raises(ValidationError, match="resolve open questions"):
        DataModel.model_validate(draft)
    draft["concepts"][0]["open_questions"] = []
    assert DataModel.model_validate(draft).status == "published"
    draft["status"] = "draft"
    with pytest.raises(ValidationError, match="draft cannot carry"):
        DataModel.model_validate(draft)


def test_duplicate_yaml_keys_are_not_silently_overwritten():
    with pytest.raises(ValueError, match="duplicate YAML key"):
        yaml.load("id: first\nid: second\n", Loader=UniqueKeyLoader)


def test_numeric_revisions_are_not_coerced(draft):
    draft["revision"] = 1
    with pytest.raises(ValidationError):
        DataModel.model_validate(draft)
