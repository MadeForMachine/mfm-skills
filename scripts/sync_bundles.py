"""Generate self-contained skill resources from neutral format sources.

Run with --check in CI. Consumers can copy one skill directory without installing
the repository or any sibling skill. Edit src/ and formats/, not generated copies.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mfm_factory_formats.commands import Envelope  # noqa: E402
from mfm_factory_formats.construction import Envelope as ConstructionEnvelope  # noqa: E402
from mfm_factory_formats.formats import Architecture, DataModel  # noqa: E402


def resources():
    copies = {
        "skills/mfm-spec-local/mfm_spec_lint.py": "src/mfm_spec_lint.py",
        "skills/mfm-spec-local/SPEC.md": "formats/spec/SPEC.md",
        "skills/mfm-spec-local/mfm-spec.schema.json": "formats/spec/mfm-spec.schema.json",
        "skills/mfm-spec-local/mfm-spec-manifest.schema.json": "formats/spec/mfm-spec-manifest.schema.json",
        "skills/mfm-factory/references/spec-format.md": "formats/spec/SPEC.md",
        "skills/mfm-factory/references/mfm-spec.schema.json": "formats/spec/mfm-spec.schema.json",
        "skills/mfm-factory/references/mfm-spec-manifest.schema.json": "formats/spec/mfm-spec-manifest.schema.json",
        "skills/mfm-data-model-local/scripts/model.py": "src/mfm_data_model/model.py",
        "skills/mfm-data-model-local/scripts/__init__.py": "src/mfm_data_model/__init__.py",
    }
    for name in ("__init__.py", "formats.py", "commands.py", "construction.py"):
        copies[f"skills/mfm-factory/scripts/{name}"] = f"src/mfm_factory_formats/{name}"
    for name in ("mfm-spec.schema.json", "mfm-spec-manifest.schema.json"):
        copies[f"src/mfm_factory_formats/schemas/{name}"] = f"formats/spec/{name}"
    result = {destination: (ROOT / source).read_bytes() for destination, source in copies.items()}
    for name, model in (("data-model", DataModel), ("architecture", Architecture), ("commands", Envelope), ("construction", ConstructionEnvelope)):
        schema = model.model_json_schema(by_alias=True)
        schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        result[f"skills/mfm-factory/references/{name}.schema.json"] = (
            json.dumps(schema, indent=2) + "\n"
        ).encode()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for relative, content in resources().items():
        path = ROOT / relative
        if path.exists() and path.read_bytes() == content:
            continue
        if args.check:
            stale.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            print(f"Updated {relative}")
    if stale:
        raise SystemExit("Stale skill resources:\n" + "\n".join(stale))


if __name__ == "__main__":
    main()
