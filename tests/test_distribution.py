"""Exercise copied skills without sibling skills or repository imports."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd):
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    return subprocess.run(
        [sys.executable, *map(str, args)], cwd=cwd, env=env,
        capture_output=True, text=True, check=True,
    )


def test_local_spec_bundle_works_alone(tmp_path):
    skill = tmp_path / "local"
    shutil.copytree(ROOT / "skills/mfm-spec-local", skill)
    # -S excludes installed site packages. Supply only PyYAML and this bundle:
    # the spec validator itself must come from the copied skill.
    code = (
        "import sys; sys.path[:0] = sys.argv[1:3]; "
        "from mfm_spec_lint import main; sys.argv = ['lint', sys.argv[3]]; "
        "raise SystemExit(main())"
    )
    run("-I", "-S", "-c", code, skill, Path(yaml.__file__).parents[1],
        skill / "examples/relayve", cwd=tmp_path)


def test_factory_bundle_works_alone(tmp_path):
    skill = tmp_path / "factory"
    shutil.copytree(ROOT / "skills/mfm-factory", skill)
    code = """
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from scripts.formats import Architecture, DataModel
from scripts.commands import Envelope
example = json.loads(Path(sys.argv[1], 'references/example.json').read_text())
Architecture.model_validate(example['architecture'])
DataModel.model_validate(example['data_model'])
Envelope.model_validate(dict(project_slug='example', idempotency_key='one',
    reason='Isolated bundle', command=dict(type='create_architecture_variant',
    id='one', name='One', spec_variant='primary')))
assert not any(k.startswith('mfm_spec_lint') for k in sys.modules)
"""
    run("-I", "-c", code, skill, cwd=tmp_path)


def test_installed_library_has_no_skill_path_dependency(tmp_path):
    run("-I", "-c", """
import mfm_spec_lint, mfm_data_model, mfm_factory_formats.commands
for module in (mfm_spec_lint, mfm_data_model, mfm_factory_formats.commands):
    assert '/skills/' not in module.__file__, module.__file__
from mfm_spec_lint import parse_node, render_node
assert parse_node(render_node({'id': 'root', 'kind': 'component'}, '## Why\\nTest')).id == 'root'
""", cwd=tmp_path)


def test_skill_manifests_and_local_links():
    schema = json.loads((ROOT / "skill.schema.json").read_text())
    for entry in (ROOT / "skills").glob("*/SKILL.md"):
        frontmatter = yaml.safe_load(entry.read_text().split("---", 2)[1])
        jsonschema.validate(frontmatter, schema)
        assert frontmatter["name"] == entry.parent.name
    # These are independent installs: relative instruction links must stay inside
    # their bundle and resolve. Public URLs are deliberately not fetched here.
    for name in ("mfm-spec-local", "mfm-factory"):
        skill = ROOT / "skills" / name
        for doc in skill.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", doc.read_text()):
                target = target.split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                path = (doc.parent / target).resolve()
                assert path.is_relative_to(skill), (doc, target)
                assert path.exists(), (doc, target)
