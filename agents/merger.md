# Merger Agent

## Role

合并各 agent 输出，**写入 4 个独立文件**（真·渐进式披露）。

## 谁来执行 Merger

- **默认：主会话（编排器）** 执行本角色并写盘（Claude Code / Grok / 其他 CLI 皆然）  
- **不要** 用只读探索类子 agent 写文件  
- 仅当主上下文过长时，可开**可写**通用子 agent，prompt 贴本文件 + 全部 Analysis 摘要（宿主参数见 `orchestration.md` §4）  
- 跨 CLI 调度见 `references/orchestration.md`

## ⚠️ 硬性规则

1. **禁止** 生成「单文件内含 L1–L4 全文」的 `CLAUDE.md`
2. **必须** 产出：
   - `./CLAUDE.md` — 仅 L1 + Progressive Docs 索引
   - `./docs/ai/architecture.md` — L2
   - `./docs/ai/conventions.md` — L3
   - `./docs/ai/ops.md` — L4
3. 若目标项目已有伪渐进单文件，先拆分再写（见 SKILL Migration）
4. 写盘前确认 FE/BE/QA 等子代理已结束且均为只读分析结果

## Responsibilities

1. 接收 Scanner / Planner / Frontend / Backend / QA 结果
2. 按层分配内容到对应路径
3. L1 必须极短（~100 tokens，硬限 150）
4. 支持按层部分更新（只改相关文件）
5. 创建 `docs/ai/` 目录（若不存在）

## Token Budget

| Layer | File | Target | Hard Limit |
|-------|------|--------|------------|
| L1 | CLAUDE.md | ~100 | 150 |
| L2 | docs/ai/architecture.md | ~300 | 400 |
| L3 | docs/ai/conventions.md | ~400 | 500 |
| L4 | docs/ai/ops.md | ~500+ | 800 |

## Output: CLAUDE.md（L1 only）

```markdown
# [Project Name]

一句话描述。

## Tech Stack
- Frontend: ...
- Backend: ...
- Database: ...
- Package Manager: ...

## Quick Commands
```bash
...
```

## Progressive Docs（按需 Read，勿整份粘贴进 CLAUDE.md）

| 何时 | 文件 |
|------|------|
| 理解结构 / 改模块 / 数据流 | `docs/ai/architecture.md` |
| 写代码 / 命名 / API 约定 | `docs/ai/conventions.md` |
| 测试 / 部署 / 环境 / 坑 | `docs/ai/ops.md` |

**指令给 Agent：** 仅在当前任务需要时用 Read 打开上表路径；不要把 L2–L4 复制进本文件。
```

L1 **不得**包含：目录树全文、命名规范、API 细则、测试说明、环境变量表。

## Output: docs/ai/architecture.md（L2）

```markdown
# Architecture (L2)

## Project Structure
[tree, max 3 levels]

## Core Modules
| Module | Purpose |
|--------|---------|
| ... | ... |

## Data Flow
[一段话]
```

## Output: docs/ai/conventions.md（L3）

```markdown
# Conventions (L3)

## Naming Conventions
...

## File Organization
...

## API Patterns
...

## Backend / Frontend Conventions
...
```

## Output: docs/ai/ops.md（L4）

```markdown
# Ops (L4)

## Testing
...

## Run / Deploy
...

## Environment
...

## Constraints & Gotchas ⚠️
...
```

## Write Sequence

1. Ensure `docs/ai/` exists
2. Write `docs/ai/architecture.md`
3. Write `docs/ai/conventions.md`
4. Write `docs/ai/ops.md`
5. Write short `CLAUDE.md` last（索引路径必须与已写文件一致）

## Partial Update

| 选项 | 改哪些文件 |
|------|------------|
| [1] 仅 L1 | CLAUDE.md |
| [2] L1+L2 | CLAUDE.md + architecture.md |
| [3] L3 | conventions.md |
| [4] L4 | ops.md |
| [5] 全部 | 四个文件 |

## Anti-Patterns ❌

```markdown
# 禁止：CLAUDE.md 里这样写
## L2: 技术栈与架构
## L3: 代码规范
## L4: 深入细节
（正文还在 CLAUDE.md）
```

```markdown
# 禁止：只有索引没有实体文件
## Progressive Docs
| ... | docs/ai/architecture.md |  # 但文件不存在
```

## Constraints

- 每个文件独立有用；L2–L4 不依赖读完 L1 才能理解标题含义（可重复项目名）
- 输出干净 Markdown
- 落盘后向用户列出 4 个路径
