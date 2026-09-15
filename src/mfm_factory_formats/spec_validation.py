"""Published v0.5 shape checks, independent of service policy and graph lint."""

import json
from importlib.resources import files

from jsonschema import Draft202012Validator, FormatChecker


def shape_errors(manifest, nodes):
    """Return field-specific errors; older formats retain their existing graph rules."""
    if manifest.get("spec_format") != "0.5":
        return []
    root = files("mfm_factory_formats").joinpath("schemas")
    errors = []
    for name, values in (
        ("mfm-spec-manifest.schema.json", [("manifest", manifest)]),
        ("mfm-spec.schema.json", [(n.id, n.fm) for n in nodes]),
    ):
        schema = json.loads(root.joinpath(name).read_text())
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for label, value in values:
            for error in validator.iter_errors(value):
                path = ".".join(str(part) for part in error.absolute_path)
                errors.append(f"{label}{'.' + path if path else ''}: {error.message}")
    return errors
