#!/usr/bin/env python3
"""Validate the plugin's local contracts without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_FIELDS = {
    "name",
    "description",
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "disallowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "background",
    "hooks",
    "paths",
    "shell",
}
AGENT_REQUIRED_FIELDS = {"name", "description"}
WRITE_TOOLS = {"Write", "Edit", "NotebookEdit"}
PLUGIN_AGENT_UNSUPPORTED_FIELDS = {"permissionMode", "hooks", "mcpServers"}
EXPECTED_AGENTS = {
    "scanner",
    "planner",
    "frontend-analyzer",
    "backend-analyzer",
    "qa-analyzer",
    "auditor",
    "merger",
    "validator",
}
CONTRACT_SNIPPETS = (
    "schema_version: 1",
    "status: ok | not_applicable | partial | failed",
    "scope_checked:",
    "destination: root | rule:<relative-path> | nested:<relative-path> | skill:<name> | omit",
    "warnings:",
    "conflicts:",
    "result:",
)


def frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("unterminated YAML frontmatter") from exc

    values: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values, text


def main() -> int:
    errors: list[str] = []

    manifest_path = ROOT / ".claude-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("name") != "progressive-claude-md":
            errors.append("plugin name must be progressive-claude-md")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid plugin manifest: {exc}")

    skill_path = ROOT / "SKILL.md"
    try:
        skill_meta, skill_text = frontmatter(skill_path)
        unknown = set(skill_meta) - SKILL_FIELDS
        if unknown:
            errors.append(f"SKILL.md has unsupported fields: {sorted(unknown)}")
        if not skill_meta.get("description"):
            errors.append("SKILL.md requires a description")
        if "tools" in skill_meta:
            errors.append("SKILL.md must use allowed-tools, not tools")
        if "$ARGUMENTS" not in skill_text:
            errors.append("SKILL.md must consume $ARGUMENTS")
        if "[check] [scope]" not in skill_meta.get("argument-hint", ""):
            errors.append("SKILL.md argument-hint must expose only optional check and scope")
        orchestration_snippets = (
            "./**/.claude/rules/**/*.md",
            "@path",
            "claudeMdExcludes",
            "`check` is the only public read-only command",
            "Fail closed when the first argument is a legacy command word",
        )
        for snippet in orchestration_snippets:
            if snippet not in skill_text:
                errors.append(f"SKILL.md orchestration missing: {snippet}")

        for link in re.findall(r"\[[^]]+\]\(([^)#]+)(?:#[^)]+)?\)", skill_text):
            if "://" in link or link.startswith("#"):
                continue
            target = (ROOT / link).resolve()
            if not target.exists():
                errors.append(f"SKILL.md links to missing resource: {link}")
    except (OSError, ValueError) as exc:
        errors.append(f"invalid SKILL.md: {exc}")

    names: dict[str, Path] = {}
    for path in sorted((ROOT / "agents").glob("*.md")):
        try:
            meta, agent_text = frontmatter(path)
            missing = AGENT_REQUIRED_FIELDS - set(meta)
            if missing:
                errors.append(f"{path.name} missing fields: {sorted(missing)}")
            name = meta.get("name", "")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                errors.append(f"{path.name} has invalid agent name: {name!r}")
            if name != path.stem:
                errors.append(f"{path.name} must match frontmatter name {name!r}")
            if name in names:
                errors.append(f"duplicate agent name {name!r}: {names[name].name}, {path.name}")
            elif name:
                names[name] = path
            tools = set(re.split(r"[\s,]+", meta.get("tools", "")))
            writable = sorted(tools & WRITE_TOOLS)
            if writable:
                errors.append(f"{path.name} must remain read-only; found {writable}")
            if tools != {"Read", "Glob", "Grep"}:
                errors.append(f"{path.name} tools must be exactly Read, Glob, Grep")
            unsupported = sorted(set(meta) & PLUGIN_AGENT_UNSUPPORTED_FIELDS)
            if unsupported:
                errors.append(f"{path.name} has unsupported plugin fields: {unsupported}")
            try:
                max_turns = int(meta.get("maxTurns", "0"))
                if not 1 <= max_turns <= 20:
                    raise ValueError
            except ValueError:
                errors.append(f"{path.name} maxTurns must be an integer from 1 to 20")
            for snippet in (f"agent: {name}", *CONTRACT_SNIPPETS):
                if snippet not in agent_text:
                    errors.append(f"{path.name} contract missing: {snippet}")
        except (OSError, ValueError) as exc:
            errors.append(f"invalid agent {path.name}: {exc}")

    missing_agents = sorted(EXPECTED_AGENTS - set(names))
    extra_agents = sorted(set(names) - EXPECTED_AGENTS)
    if missing_agents:
        errors.append(f"missing expected agents: {missing_agents}")
    if extra_agents:
        errors.append(f"unexpected agents: {extra_agents}")

    try:
        merger_text = (ROOT / "agents" / "merger.md").read_text(encoding="utf-8")
        for snippet in (
            "mode: build | check",
            "operation: create | update | move | remove | unchanged",
            "patches:",
            "preserve_unmatched_content: true",
            "unresolved_questions: []",
        ):
            if snippet not in merger_text:
                errors.append(f"merger patch contract missing: {snippet}")
    except OSError as exc:
        errors.append(f"invalid merger agent: {exc}")

    try:
        validator_text = (ROOT / "agents" / "validator.md").read_text(encoding="utf-8")
        if "mode: build | check" not in validator_text:
            errors.append("validator contract must use build/check mode")
        if "It remains `false` in check mode." not in validator_text:
            errors.append("validator must keep check mode read-only")
    except OSError as exc:
        errors.append(f"invalid validator agent: {exc}")

    project_types_text = (ROOT / "references" / "project-types.md").read_text(encoding="utf-8")
    if "## Scanner Output Contract" in project_types_text or "- key: package_manager" in project_types_text:
        errors.append("project-types.md contains a competing scanner contract")

    try:
        workflows_text = (ROOT / "references" / "workflows.md").read_text(encoding="utf-8")
        for snippet in ("./**/.claude/rules/**/*.md", "@path", "claudeMdExcludes"):
            if snippet not in workflows_text:
                errors.append(f"workflows.md discovery missing: {snippet}")
    except OSError as exc:
        errors.append(f"invalid workflows reference: {exc}")

    secret_policy_files = (
        skill_path,
        ROOT / "agents" / "scanner.md",
        ROOT / "references" / "project-types.md",
        ROOT / "references" / "workflows.md",
    )
    for path in secret_policy_files:
        try:
            text = path.read_text(encoding="utf-8")
            if ".env.example" in text or "tracked example/template may be inspected" in text:
                errors.append(f"{path.relative_to(ROOT)} weakens the no-env-read policy")
        except OSError as exc:
            errors.append(f"invalid secret-policy file {path.relative_to(ROOT)}: {exc}")

    canonical_command = "/progressive-claude-md:progressive-claude-md"
    legacy_command = re.compile(
        rf"(?m)^/?(?:progressive-claude-md:)?progressive-claude-md\s+"
        r"(?:generate|audit|update|analyze)(?:\s|$)"
    )
    for name in ("README.md", "README.zh-CN.md"):
        path = ROOT / name
        try:
            readme_text = path.read_text(encoding="utf-8")
            if not re.search(rf"(?m)^{re.escape(canonical_command)}$", readme_text):
                errors.append(f"{name} is missing the default namespaced invocation")
            if not re.search(rf"(?m)^{re.escape(canonical_command)} check$", readme_text):
                errors.append(f"{name} is missing the namespaced check invocation")
            if legacy_command.search(readme_text):
                errors.append(f"{name} documents a removed legacy command mode")
        except OSError as exc:
            errors.append(f"invalid {name}: {exc}")

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated plugin, skill, and {len(names)} read-only agents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
