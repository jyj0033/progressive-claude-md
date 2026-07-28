# Agent Output Contract

Use this schema as the canonical maintenance contract for every plugin subagent. Each agent embeds the same envelope because subagents run in independent contexts; only `agent`, claim topics, and `result` are role-specific.

## Canonical Envelope

```yaml
schema_version: 1
agent: scanner | planner | frontend-analyzer | backend-analyzer | qa-analyzer | auditor | merger | change-detector | validator
status: ok | not_applicable | partial | failed
summary: "brief, factual summary"
scope_checked:
  - "repository-relative path or glob"
claims:
  - id: <role-prefix>-001
    topic: <role-specific topic>
    value: "fact, decision, or candidate instruction"
    destination: root | rule:<relative-path> | nested:<relative-path> | skill:<name> | omit
    confidence: high | medium | low
    evidence:
      - kind: file | user_statement
        path: "repository-relative path or <user>"
        lines: "line, range, manifest key, symbol, or turn reference"
        detail: "what the source proves without exposing secrets"
warnings: []
conflicts: []
result: {}
```

## Status Semantics

- `ok`: completed for the full requested scope.
- `not_applicable`: the routed domain is absent or no role-specific work is needed; this is a successful terminal result.
- `partial`: useful results exist, but named paths, evidence, or conflicts remain unresolved.
- `failed`: no trustworthy result can be produced; explain why in `warnings` or `conflicts`.

Never replace missing information with a plausible value just to satisfy the schema.

## Evidence Rules

- Preserve raw evidence locators across every handoff; an upstream summary is not evidence.
- Use `kind: user_statement` only for an explicit current fact, never for a question, quotation, hypothetical, negation, or future plan.
- Do not merge `low` confidence claims into instruction files.
- Report two supported but incompatible values in `conflicts`; do not silently select one.
- Use `destination: omit` for derivable inventory, generic defaults, secrets, or information that does not belong in Claude Code instructions.

## Role-Specific Result

| Agent | Required `result` content |
|---|---|
| scanner | detected domains and key files |
| planner | conditional routes and proposed documents |
| frontend/backend/qa analyzer | domain findings relevant to placement |
| auditor | drift findings and proposed actions |
| change-detector | statement classification and suggested target |
| merger | mode, candidate manifest, create/update/move/remove/unchanged operations, anchored patches, omitted claims, unresolved questions |
| validator | mode, write authorization, checks, failures, and `safe_to_write` |

The validator must receive the original evidence ledger as well as merger output. Validation cannot rely only on synthesized candidate prose.
