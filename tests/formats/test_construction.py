import pytest
from pydantic import ValidationError

from mfm_factory_formats.construction import Envelope
from mfm_factory_formats.spec_validation import shape_errors
from mfm_spec_lint import parse_node


def test_claim_bounds_and_typed_versioned_command():
    body = {"project_slug": "demo", "idempotency_key": "claim-one", "reason": "Claim a bounded task", "command": {"type": "claim_next_work", "run_id": "trial"}}
    claim = Envelope.model_validate(body)
    assert claim.command.recover_expired is False
    assert claim.command.lease_seconds == 900
    body["command"]["lease_seconds"] = 100000
    with pytest.raises(ValidationError):
        Envelope.model_validate(body)


def test_published_shape_rejects_unknown_tier_and_mapping_evidence():
    manifest = {"spec_format": "0.5", "name": "Demo", "root": "root"}
    node = parse_node("---\nid: root\nkind: component\ntitle: Demo\nparent: null\nresponsibility: Own demo.\ntier: core\nstatus: open\nopen_questions: []\n---\n")
    assert shape_errors(manifest, [node]) == []
    node.fm["tier"] = "foundation"
    assert any("tier" in error for error in shape_errors(manifest, [node]))
    evaluation = parse_node("---\nid: evaluation\nkind: evaluation\ntitle: Review\nsubject:\n  component: root\nverdict: mixed\nsummary: Review findings.\nevidence:\n  - location: accidentally-a-mapping\n---\n")
    assert any("evidence" in error for error in shape_errors(manifest, [evaluation]))
    assert shape_errors({"spec_format": "0.4"}, [node]) == []
