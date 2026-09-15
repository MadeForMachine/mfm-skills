# mfm-skills

> The public source of truth for [MadeForMachine](https://madeformachine.com) agent
> skills. Every public surface — the madeformachine.com skill pages, the mfm.dev
> machine pages, the install bundles — is **generated from this repo.**

A *skill* is a focused, procedural instruction set your coding agent loads to do
better work: it carries the opinion (how to approach a task), while the work itself
runs through tools — usually a MadeForMachine MCP connector. The skill is the
incision plan; the tools are the instruments; your agent holds the scalpel.

## Layout

Skills live under `skills/`; shared format code lives independently under `src/`.
Each installed skill is self-contained:

```
skills/
  <name>/
    SKILL.md       # manifest frontmatter (see skill.schema.json) + the skill body
    agents/
      openai.yaml  # Codex UI name, invocation policy, and MCP dependencies
    CHANGELOG.md   # notable changes; entries marked MAJOR need a re-read
    …              # any assets the skill bundles (examples, scripts, reference linter)
skill.schema.json  # the frontmatter contract the page generator reads
src/               # canonical Python library; no imports from skills/
formats/spec/      # canonical spec documentation and JSON Schemas
tests/             # format, packaging, and isolated skill checks
scripts/sync_bundles.py  # generates portable copies; --check detects drift
```

The frontmatter is the keystone: `version`, `status`, `public`, `connector`,
`requires` (the MCP tool ids the body calls), and `license`. The generator turns
`frontmatter + body + CHANGELOG` into the public pages and the machine-readable JSON
twin — so the pages can't drift from the skill.

## Skills

| Skill | What it does | Status |
|-------|--------------|--------|
| [`mfm-spec-local`](skills/mfm-spec-local/) | Interrogates a system's architecture out of your head into local MFM Spec files. | mvp |
| [`mfm-data-model-local`](skills/mfm-data-model-local/) | Develops logical data meaning from a specification in local files; experimental, excluded from generated distribution. | alpha |
| [`mfm-spec`](skills/mfm-spec/) | Steers hosted, service-backed MFM Spec authoring through MCP. | alpha |
| [`mfm-factory`](skills/mfm-factory/) | One MCP workflow for design variants, executable mocks and construction feedback; includes starting data/architecture formats. Excluded from generated distribution pending hosted Factory support. | alpha |
| [`atlas`](skills/atlas/) | Steers your agent to query MadeForMachine Atlas (the product/feature discovery-and-comparison engine) — jump to doc evidence instead of crawling provider docs. | beta |

Internal / operator-scoped skills (e.g. the Atlas harvest tooling) are **not** in
this repo — they live in a private repo and are never published.

**MFM Spec Local remains specification-only.** It needs no hosted service or other
skill. **MFM Factory is a separate, complete hosted workflow**, including its own
spec-authoring reference. It needs neither the local spec/model skills nor the
hosted spec skill installed. Local Docker hosting still means hosted authority.

The standalone hosted `mfm-spec` skill remains useful for spec-only MCP projects.
The experimental `mfm-data-model-local` skill remains a separate tool with its
existing format. There is no combined “MFM Local” workflow or automatic migration.

## Install

The primary, version-pinned install is the **mfm.dev page for each skill**
(`mfm.dev/skills/<name>`): hand it to your agent and it fetches the current version
and writes it to the right skills directory for your harness.

Manual install is the fallback — copy a skill folder into your agent's skills
directory:

```sh
git clone https://github.com/MadeForMachine/mfm-skills.git
cp -r mfm-skills/skills/mfm-spec ~/.claude/skills/mfm-spec                 # Claude Code hosted MCP skill
cp -r mfm-skills/skills/mfm-spec ~/.agents/skills/mfm-spec                 # Codex / Cursor hosted MCP skill
cp -r mfm-skills/skills/mfm-spec-local ~/.claude/skills/mfm-spec-local     # Claude Code
cp -r mfm-skills/skills/mfm-spec-local ~/.agents/skills/mfm-spec-local     # Codex / Cursor
```

Hosted skills also need their MCP connector. For MFM Spec Hosted, configure the `mfm`
server at `https://mcp.mfm.dev/mcp` and complete OAuth before expecting the `mfm_spec_*`
tools to appear.

For a development checkout, symlink each desired skill into one discovery root,
such as `~/.codex/skills`, instead of maintaining copied installations. Avoid
duplicate copies in both `~/.agents/skills` and `~/.codex/skills`. Keep unrelated
skills untouched. Existing conversations may retain their original catalog; use
a new conversation to discover changed metadata.

## Format library and validation

The distribution name `mfm-spec-format` and imports `mfm_spec_lint`,
`mfm_data_model`, and `mfm_factory_formats` remain compatible. The package builds
from `src/`; services do not install a local-authoring skill to validate content.
`mfm_data_model` retains the older model format for legacy consumers;
`mfm_factory_formats` contains current Factory document and command schemas.
This cleanup changes packaging, not their semantics.

Edit shared code in `src/` and spec definitions in `formats/spec/`. Run
`python scripts/sync_bundles.py` in the permitted Python environment to generate
portable skill copies and Factory JSON Schemas. Generated copies let an installed
skill run without this repository or sibling skills; do not edit them separately.

Run all checks in Docker:

```sh
docker build -t mfm-skills-check .
docker run --rm mfm-skills-check
```

CI checks bundle drift, format tests, manifest/link validity, and isolated installs
of Local and Factory. Existing published skill names and validator entry points
remain stable.

## License

[MIT](./LICENSE) — applies to every skill in this repo.
