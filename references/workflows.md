# Generation Workflow and Safe Reconciliation

Read this reference for the default generation workflow, the optional read-only check, agent routing, and safe handling of existing instruction files.

## Contents

- [Public interface](#public-interface)
- [Discovery order](#discovery-order)
- [Evidence and privacy boundary](#evidence-and-privacy-boundary)
- [Agent routing](#choose-main-thread-or-subagents)
- [Merge policy](#planner-and-merge-policy)
- [Existing-file reconciliation](#existing-file-reconciliation)
- [Independent validation](#independent-validation)

## Public Interface

| Invocation | Result | Write files |
|---|---|---|
| Default, optionally followed by a scope | Build the smallest evidence-backed progressive instruction layout | Yes, after validation and only within scope |
| `check`, optionally followed by a scope | Validate the existing layout and return findings plus a proposed manifest | No |

An empty argument list builds at the repository root. `check` is the only public read-only command. Generation, inspection, reconciliation of existing files, and validation are internal phases rather than separate user-facing modes. A request that explicitly prohibits writes is treated as `check`.

## Discovery Order

Inspect applicable sources before proposing files:

1. Project entrypoint: `./CLAUDE.md` or `./.claude/CLAUDE.md`.
2. Personal project instructions: `./CLAUDE.local.md`.
3. Root modular rules: `./.claude/rules/**/*.md`.
4. Nested instructions and rules: `./**/CLAUDE.md`, `./**/CLAUDE.local.md`, and `./**/.claude/rules/**/*.md`, excluding dependencies and generated trees.
5. Approved and accessible `@path` imports referenced outside Markdown code spans.
6. `claudeMdExcludes` from applicable Claude Code settings; excluded files are not part of the effective graph.
7. Task skills: `./.claude/skills/*/SKILL.md`.
8. Relevant manifests, source, tests, CI, and maintained documentation.

Managed and user-level instructions may matter for conflict detection but are outside project-edit scope unless explicitly requested. Avoid creating both root `CLAUDE.md` and `.claude/CLAUDE.md`; follow the existing convention or default to root `CLAUDE.md` when neither exists.

## Evidence and Privacy Boundary

- Repository evidence and explicit user statements are acceptable sources. Label user-stated facts when the repository does not corroborate them.
- Never open `.env*`, credentials, tokens, private keys, certificates, password stores, or production configuration, including tracked environment examples.
- Record an environment variable identifier only when a schema, source declaration, or maintained document exposes it; never record assigned values.
- Never copy personal content from `CLAUDE.local.md` into tracked project files.
- Ignore dependency caches, build output, generated code, vendored trees, `.git`, and unrelated fixtures/examples during inference.

## Choose Main Thread or Subagents

Use the main thread for a small repository, one narrow instruction file, or work whose branches would inspect the same files. Use specialized subagents only when scopes are independently useful and the repository is large enough to justify coordination.

```text
Main: resolve build/check, root, scope, exclusions, and existing instructions
  -> Scanner: gather evidence only
  -> Planner/Router: choose artifacts and applicable branches
  -> [Frontend] [Backend] [QA/Infra]  (applicable branches in parallel)
  -> Auditor: compare existing instructions when present or during check
  -> Merger: reconcile claims and prepare a candidate manifest or minimal patch
  -> Independent validator: verify evidence, scope, syntax, and duplication
  -> Main thread only: write in build mode or report in check mode, then read back
```

Scanner precedes routing. Frontend, Backend, and QA/Infra are peers, not mandatory sequential stages. Every subagent, including auditor, merger, and validator, is read-only. Only the main thread may edit files after successful build-mode validation.

## Conditional Routing

| Branch | Run when | Skip when |
|---|---|---|
| Frontend | Evidence shows browser/mobile UI source or a frontend package in scope | CLI, library, backend-only, or unrelated package |
| Backend | Evidence shows server handlers, services, jobs, API, or backend package in scope | Frontend-only or unrelated package |
| QA/Infra | Tests, CI, build, deployment, migration, environment setup, or verification affects generated instructions | None of these are relevant |
| Auditor | Existing instruction artifacts are in scope or command is `check` | A new layout has no existing artifacts |
| Validator | Candidate artifacts, patches, moves, or removals exist | Merger correctly returns no applicable artifact |

For monorepos, route by requested or detected package. Give agents disjoint evidence scopes; do not make each specialist rescan the repository.

## Unified Agent Contract

Every subagent returns structured findings, not prose ready to paste. The complete canonical envelope and status semantics live in [Agent output contract](contracts.md); the abbreviated shape is:

```yaml
schema_version: 1
agent: scanner | planner | frontend-analyzer | backend-analyzer | qa-analyzer | auditor | merger | validator
status: ok | not_applicable | partial | failed
summary: "brief factual summary"
scope_checked: [<repository-relative paths>]
claims:
  - id: <stable identifier>
    topic: <role-specific topic>
    value: <fact or instruction>
    destination: root | rule:<relative-path> | nested:<relative-path> | skill:<name> | omit
    confidence: high | medium | low
    evidence:
      - kind: file | user_statement
        path: <repository-relative path or user>
        lines: <line, manifest key, target, symbol, or turn>
        detail: <what the source proves>
warnings: []
conflicts: []
result: {}
```

`not_applicable` is a successful terminal status. Never invent a value to fill the schema. Keep unresolved information in warnings or conflicts; do not merge low-confidence claims as facts.

## Planner and Merge Policy

The planner/router:

- turns scanner evidence into bounded specialist scopes;
- classifies content as global, path-scoped, subtree-owned, task-specific, or report-only;
- avoids running a specialist with no evidence-backed scope;
- passes relevant existing instructions to each specialist for conflict detection.

The merger produces a candidate file manifest and patch; it never writes files:

1. Groups claims by stable key and destination.
2. Rejects unsupported, low-confidence, placeholder, and secret-bearing claims.
3. Resolves a conflict only with stronger direct evidence; otherwise reports an unknown.
4. Deduplicates ancestor, rule, and nested instructions.
5. Selects the narrowest correct loading boundary without hiding a global constraint.
6. Produces a proposed file manifest before writing.
7. Returns candidate artifacts and unresolved questions to the main thread.

When files already exist, the merger emits create/update/move/remove/unchanged artifact operations and anchored patches. Build mode allows the main thread to apply only the validated operations in scope. Check mode returns the same validated proposal without writing.

## Existing-File Reconciliation

1. Resolve the repository root, build/check mode, and optional scope.
2. Read every existing instruction artifact affected by that scope.
3. Build a claim-to-evidence ledger; mark stale, duplicate, conflicting, unsupported, misplaced, and missing content.
4. Produce a manifest and minimal diff plan. Preserve unrelated prose, comments, ordering, and formatting.
5. In build mode, patch only affected statements or move them to the correct loading boundary.
6. Re-read every changed file and validate syntax, globs, commands, duplication, and placeholders.
7. Report created, changed, moved, and intentionally untouched files.

Do not overwrite an existing file merely to normalize its format. Moving content is a semantic change: preserve meaning, name the destination, and remove the conflicting old copy only when build scope includes both locations.

## Check Status and Report

| Status | Meaning |
|---|---|
| `valid` | Correct, evidenced, and placed at the proper load boundary |
| `stale` | Contradicted by current evidence |
| `unsupported` | No repository evidence or explicit user instruction supports it |
| `misplaced` | Correct content loaded at the wrong scope |
| `duplicate` | Equivalent instruction exists in several loaded artifacts |
| `conflict` | Loaded instructions disagree |
| `missing` | A non-obvious, high-value instruction should be documented |

```markdown
## Instruction check

| File | Status | Finding | Evidence | Proposed action |
|---|---|---|---|---|
| `<path>` | `<status>` | <concise finding> | `<path#locator>` | <keep/update/move/remove/add> |

### Proposed file manifest

<List path, create/update/move action, destination scope, reason, and evidence.>

### Unknowns

- <Only questions whose answers would materially change the result.>
```

In check mode, propose changes but never perform them.

## Independent Validation

The validator receives the original claim ledger and proposed artifacts or patches. Check that:

- every statement maps to evidence or an explicit user statement;
- root content is globally applicable;
- conditional rules have valid `paths` frontmatter and matching targets;
- nested instructions are not duplicated in ancestors;
- task procedures are absent from always-loaded context;
- exact commands include a non-root working directory when required;
- no secret values, placeholders, generic defaults, or stale four-layer terminology remain;
- changed Markdown/frontmatter parses and every changed file was read back.

Return validation failures to the merger once. If evidence remains ambiguous, report it instead of looping or guessing.
