# Progressive CLAUDE.md

English | [简体中文](README.zh-CN.md)

A Claude Code CLI plugin that generates, audits, and safely updates project instructions using repository evidence and Claude Code's actual loading boundaries.

## What changed in v2

- Uses a concise root `CLAUDE.md`, path-scoped `.claude/rules`, nested `CLAUDE.md` files, and task skills instead of four always-loaded headings.
- Registers read-only Scanner, Planner, Frontend, Backend, QA/Infra, Auditor, Merger, Change Detector, and Validator subagents.
- Routes only applicable agents and runs independent domain analysis in parallel.
- Requires source evidence for generated facts and keeps the main conversation as the only writer.
- Preserves existing human-authored content through minimal, validated patches.

## Install for Claude Code CLI

Place this directory at:

```text
~/.claude/skills/progressive-claude-md/
```

Because the directory contains `.claude-plugin/plugin.json`, Claude Code discovers it as `progressive-claude-md@skills-dir` on the next session. No marketplace installation is required.

For local development from another directory:

```bash
claude --plugin-dir /absolute/path/to/progressive-claude-md
```

After changing `agents/` or the plugin manifest, restart Claude Code or run `/reload-plugins`. Changes to `SKILL.md` are detected live.

## Use

Invoke the skill directly:

```text
/progressive-claude-md:progressive-claude-md generate
/progressive-claude-md:progressive-claude-md audit
/progressive-claude-md:progressive-claude-md update
/progressive-claude-md:progressive-claude-md analyze
```

Natural-language requests that explicitly mention creating, auditing, or updating Claude Code project instructions can also trigger it automatically.

Read-only requests stay read-only. Generate and update requests write only after evidence collection, candidate validation, and scope checks.

## Validate

From the plugin root:

```bash
python scripts/validate_plugin.py
claude plugin validate . --strict
```

Use `/memory` in a project session to inspect loaded instructions. Use `/doctor` to find oversized or derivable CLAUDE.md content.

## Runtime layout

```text
progressive-claude-md/
├── .claude-plugin/plugin.json
├── SKILL.md
├── agents/
│   ├── scanner.md
│   ├── planner.md
│   ├── frontend-analyzer.md
│   ├── backend-analyzer.md
│   ├── qa-analyzer.md
│   ├── auditor.md
│   ├── merger.md
│   ├── change-detector.md
│   └── validator.md
├── references/
│   ├── claude-loading.md
│   ├── contracts.md
│   ├── workflows.md
│   └── project-types.md
├── templates/layer-template.md
└── scripts/validate_plugin.py
```

All subagents are read-only. `change-detector.md` is non-persistent; it does not monitor conversations after a skill invocation ends.
