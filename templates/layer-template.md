# Layer Template Reference

多文件渐进结构模板。**禁止**把 L2–L4 写进同一个 CLAUDE.md。

## 落盘布局

```
CLAUDE.md                      # L1 only
docs/ai/architecture.md        # L2
docs/ai/conventions.md         # L3
docs/ai/ops.md                 # L4
```

---

## L1: CLAUDE.md

```markdown
# [Project Name]

[One sentence]

## Tech Stack
- Frontend: [framework]
- Backend: [framework]
- Database: [database]
- Package Manager: [npm/yarn/pnpm]

## Quick Commands
```bash
[install]
[dev]
[build]
```

## Progressive Docs（按需 Read，勿整份粘贴进 CLAUDE.md）

| 何时 | 文件 |
|------|------|
| 理解结构 / 改模块 / 数据流 | `docs/ai/architecture.md` |
| 写代码 / 命名 / API 约定 | `docs/ai/conventions.md` |
| 测试 / 部署 / 环境 / 坑 | `docs/ai/ops.md` |

**指令给 Agent：** 仅在当前任务需要时用 Read 打开上表路径。
```

---

## L2: docs/ai/architecture.md

```markdown
# Architecture (L2)

## Project Structure

```
[directory tree - max 3 levels]
```

## Core Modules

| Module | Purpose |
|--------|---------|
| [path] | [description] |

## Data Flow

[How data flows - one paragraph]
```

---

## L3: docs/ai/conventions.md

```markdown
# Conventions (L3)

## Naming Conventions
- Components: PascalCase
- Utils: camelCase
- Constants: SCREAMING_SNAKE_CASE

## File Organization
- One component per file
- Colocation for tests when present

## API Patterns
- RESTful: GET/POST/PUT/DELETE
- Error: `{ error: string }`
```

---

## L4: docs/ai/ops.md

```markdown
# Ops (L4)

## Testing
- Framework: [Vitest/...]
- Commands: `npm test`

## Run / Deploy
```bash
[build]
[start]
```

## Environment
| Var | Meaning | Default |
|-----|---------|---------|
| ... | ... | ... |

## Constraints & Gotchas ⚠️
- Node version: ...
- Known issues: ...
```

---

## Token Budget

| Layer | File | Target | Hard Limit |
|-------|------|--------|------------|
| L1 | CLAUDE.md | ~100 | 150 |
| L2 | architecture.md | ~300 | 400 |
| L3 | conventions.md | ~400 | 500 |
| L4 | ops.md | ~500+ | 800 |

---

## Placement Guide

| Type | L1 | L2 | L3 | L4 |
|------|----|----|----|----|
| 一句话/栈/命令 | ✓ | | | |
| 目录/模块/数据流 | | ✓ | | |
| 命名/API 约定 | | | ✓ | |
| 测试/部署/环境/坑 | | | | ✓ |
