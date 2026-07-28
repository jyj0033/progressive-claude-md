# Progressive CLAUDE.md

English | [简体中文](README.zh-CN.md)

A focused Claude Code CLI plugin that generates evidence-backed project instructions using Claude Code's real progressive loading boundaries. The public interface is intentionally small: the default command builds the layout, while `check` validates it without writing.

## What it generates

- A concise root `CLAUDE.md` for instructions that apply to the whole repository.
- Path-scoped `.claude/rules/*.md` files for guidance that applies only to matching files.
- Nested `CLAUDE.md` files for package- or subtree-specific instructions.
- Task skills for detailed procedures that should load only when invoked.

It does not treat headings in one large Markdown file as lazy-loaded layers.

## How it works

- Scans repository evidence before proposing instructions.
- Routes only applicable read-only Scanner, Planner, Frontend, Backend, QA/Infra, Auditor, Merger, and Validator subagents.
- Runs independent domain analysis in parallel when the repository is large enough to benefit.
- Keeps the main conversation as the only writer.
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

Build progressive project instructions at the repository root:

```text
/progressive-claude-md:progressive-claude-md
```

Limit generation to a scope:

```text
/progressive-claude-md:progressive-claude-md packages/api
```

Check the existing layout without writing:

```text
/progressive-claude-md:progressive-claude-md check
/progressive-claude-md:progressive-claude-md check packages/api
```

When instruction files do not exist, the default command creates the smallest useful progressive layout. When they already exist, it preserves human-authored content and applies only validated changes needed to keep that layout accurate.

Natural-language requests that explicitly mention generating or checking progressive Claude Code project instructions can also trigger the skill. `check` is always read-only.

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
│   └── validator.md
├── references/
│   ├── claude-loading.md
│   ├── contracts.md
│   ├── workflows.md
│   └── project-types.md
├── templates/layer-template.md
└── scripts/validate_plugin.py
```

All subagents are read-only. Only the main conversation may write validated build output.
