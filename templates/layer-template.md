# Progressive Claude Code Layout Templates

Use these templates only after evidence collection. They model Claude Code's actual loading boundaries; they are not four headings in one always-loaded file.

## Contents

- [Placement decision](#placement-decision)
- [Root CLAUDE.md](#root-claudemd)
- [Path-scoped rule](#path-scoped-rule)
- [Nested CLAUDE.md](#nested-claudemd)
- [Task skill proposal](#task-skill-proposal)
- [Candidate manifest](#proposed-file-manifest)
- [Final quality gate](#final-quality-gate)

## Placement Decision

| Content | Destination | Loading behavior |
|---|---|---|
| Commands and constraints needed for nearly every task | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Loaded at session start |
| Instructions for matching files or directories | `.claude/rules/<topic>.md` with `paths` | Loaded when Claude works with matching files |
| Instructions owned by one package/subtree | `<subtree>/CLAUDE.md` | Discovered when Claude reads in that subtree |
| A multi-step task or checklist | `.claude/skills/<task>/SKILL.md` | Loaded when invoked or relevant |
| Personal, project-local preferences | `./CLAUDE.local.md` | Loaded at session start; keep out of version control |

Do not use `@import` to claim deferred loading: imports are expanded into context with their containing `CLAUDE.md`.

Create only files supported by repository evidence. Omit empty headings, placeholders, generic advice, dependency inventories, and directory trees that Claude can discover directly.

## Root `CLAUDE.md`

Target a concise file, normally well below 200 lines. Include only globally applicable, non-obvious instructions.

```markdown
# <project name>

<One evidence-backed sentence only when it helps orient work.>

## Commands

- `<exact command>` — <purpose and required working directory if non-root>

## Project rules

- <non-obvious global constraint with repository evidence>
- <where to make a common category of change, if not discoverable>

## Verification

- <minimum exact verification command for a typical change>

## Gotchas

- <confirmed failure mode or invariant; omit this section when none is evidenced>
```

Never emit example facts such as a framework, Node version, naming convention, API shape, browser limitation, or command unless the repository or user explicitly establishes it.

## Path-Scoped Rule

Use a narrow, repository-relative glob. A rule without `paths` loads unconditionally and is therefore not progressive.

```markdown
---
paths:
  - "<verified/subtree/**/*.{ext1,ext2}>"
---

# <Topic> rules

- <specific, evidence-backed instruction>
- Run `<exact targeted check>` after changing matching files.
```

Prefer one coherent topic per file, for example `frontend-components.md`, `api-handlers.md`, or `database-migrations.md`. Do not create a path rule when the same instruction applies globally.

## Nested `CLAUDE.md`

Use this for a cohesive package or subtree with its own commands, architecture, or constraints. The nested file supplements ancestor instructions; it does not override them automatically.

```markdown
# <package or subtree name>

## Scope

- Applies to `<repository-relative subtree>/`.

## Commands

- From `<working directory>`, run `<exact command>` to <purpose>.

## Local conventions

- <confirmed package-specific convention>

## Verification

- `<exact targeted command>`
```

Do not duplicate root instructions. If several unrelated path patterns share a rule, prefer a path-scoped rule over multiple nested files.

## Task Skill Proposal

Procedures such as releases, deployments, migrations, incident response, or complex test setup belong in a task skill when they should not consume every session's context. Generate a skill only when explicitly requested; otherwise propose it in the plan.

```text
.claude/skills/<task-name>/
├── SKILL.md
└── references/        # only when the procedure needs supporting detail
```

```markdown
---
name: <task-name>
description: <what the procedure does and concrete situations that should trigger it>
---

# <Task title>

1. <verified step>
2. <verified step>
3. Run `<exact validation command>`.

Stop and ask the user when <confirmed irreversible or production-impacting boundary>.
```

## Proposed File Manifest

Before writing, present an explicit manifest. An empty category is omitted.

```yaml
files:
  - path: CLAUDE.md
    action: create | update
    reason: globally applicable commands and constraints
    evidence: [<repository-relative paths>]
  - path: .claude/rules/<topic>.md
    action: create | update
    paths: [<globs>]
    reason: instructions apply only to matching files
    evidence: [<repository-relative paths>]
  - path: <subtree>/CLAUDE.md
    action: create | update
    reason: package-owned instructions
    evidence: [<repository-relative paths>]
proposals:
  - path: .claude/skills/<task>/SKILL.md
    reason: task procedure should load only on demand
```

## Final Quality Gate

- Every statement is supported by evidence or an explicit user instruction.
- Root content is globally applicable and concise.
- Every `.claude/rules` file that is intended to be conditional has valid `paths` frontmatter.
- Nested files contain only subtree-specific guidance.
- No `@import` is described as lazy loading.
- No placeholders, empty headings, example defaults, secrets, or duplicated instructions remain.
- Commands preserve exact spelling and working directory.
