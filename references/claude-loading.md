# Claude Code Instruction Loading

Read this reference when deciding where generated instructions belong. These are loading boundaries, not conceptual document layers.

## Locations and Scope

| Location | Scope | Loading behavior | Typical content |
|---|---|---|---|
| `~/.claude/CLAUDE.md` | User, all projects | Loaded at session start | Personal cross-project preferences |
| `./CLAUDE.md` or `./.claude/CLAUDE.md` | Shared project | Loaded at session start | Concise global commands and constraints |
| `./CLAUDE.local.md` | Personal project | Loaded at session start; normally gitignored | Local URLs or private workflow preferences, never secrets |
| `.claude/rules/*.md` without `paths` | Shared project | Loaded unconditionally | Modular global instructions |
| `.claude/rules/*.md` with `paths` | Matching paths | Loaded when Claude works with matching files | File- or subtree-specific rules |
| `<subtree>/CLAUDE.md` | Package/subtree | Discovered when Claude reads in that subtree | Package-owned commands and conventions |
| `.claude/skills/<name>/SKILL.md` | Task | Loaded when invoked or when Claude deems it relevant | Multi-step workflows and checklists |

At a given project level, use either root `CLAUDE.md` or `.claude/CLAUDE.md`; avoid creating duplicate project entrypoints. `./.claude.local.md` is not the standard local filename.

## Resolution Semantics

- Claude Code loads applicable ancestor `CLAUDE.md` and `CLAUDE.local.md` files from broad to specific; files are concatenated, not automatically overridden.
- `CLAUDE.local.md` is appended after `CLAUDE.md` at the same directory level.
- Nested instruction files under the launch directory are discovered on demand when Claude reads within their subtrees.
- `.claude/rules` files are discovered recursively. A rule without `paths` is global.
- `paths` values are repository-relative glob patterns. Scope them as narrowly as the instruction permits.
- `@path` imports improve organization but are expanded into the containing instruction context; they are not lazy loading.
- Root instructions survive compaction. Nested instructions reload when Claude next reads in their subtree.

## Placement Algorithm

For each evidence-backed instruction, choose exactly one primary destination:

1. Is it needed for nearly every project task? Put it in the project `CLAUDE.md`.
2. Does it apply only when matching certain files? Put it in a path-scoped `.claude/rules/<topic>.md`.
3. Is it owned by one cohesive package or subtree, including local commands? Put it in that subtree's `CLAUDE.md`.
4. Is it a multi-step procedure that should run only for a task such as deploy, release, or migration? Propose or create a project skill.
5. Is it personal rather than team-shared? Put it in `CLAUDE.local.md`, only when the user explicitly requests this.
6. Is it readily discoverable from code and not an instruction? Omit it.

Do not duplicate content across boundaries to make it more visible. If an instruction genuinely applies at several disjoint paths, one multi-pattern path rule is preferable to repeated copies.

## What Belongs in Always-Loaded Context

Keep the root file concise, specific, and verifiable. Favor:

- exact commands with non-obvious working-directory requirements;
- project-wide safety or architectural constraints;
- required verification that applies to most changes;
- high-impact Gotchas that cannot be inferred cheaply;
- pointers about where a common category of change belongs when structure alone is ambiguous.

Usually omit:

- dependency inventories and generated directory trees;
- generic advice already known to a coding agent;
- architecture narration that merely repeats source layout;
- framework defaults not customized by the repository;
- speculative known issues or conventions;
- procedures relevant only to one occasional task.

Target under 200 lines for each `CLAUDE.md`; shorter is normally better. This is a quality guideline, not a license to split global text into unconditional rule files, which would still load at startup.

## Path Rule Example

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "tests/api/**/*.test.ts"
---

# API changes

- <repository-specific rule supported by evidence>
- Run `<exact targeted command>` after changing matching files.
```

Omit the rule instead of leaving placeholder text. Validate that every glob matches intended repository paths.

## Progressive Disclosure Check

A generated layout is genuinely progressive only if:

- the root file contains only global, frequently useful instructions;
- conditional rules use `paths` frontmatter;
- nested files contain only subtree-owned guidance;
- task procedures live in skills rather than startup context;
- no import is described as deferred loading;
- equivalent instructions are not repeated in ancestor and descendant files.
