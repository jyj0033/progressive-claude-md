---
name: progressive-claude-md
description: Use when user asks to create, generate, update, audit, or maintain CLAUDE.md files. Also triggers when user says "初始化项目", "分析项目结构", or needs to understand project context. Multi-file progressive docs (CLAUDE.md L1 + docs/ai/*). Works across Claude Code, Grok Build, Codex, and other agent CLIs — see references/orchestration.md for host-agnostic roles and host adapters. Read-only analysis agents; main session Merger writes. Never dump L2-L4 into CLAUDE.md.
tools: Read, Edit, Glob, Grep, Bash, Agent
---

# Progressive CLAUDE.md Generator

## Overview

生成和维护**多文件渐进式**项目上下文：

| 文件 | 层级 | 何时进入上下文 |
|------|------|----------------|
| `./CLAUDE.md` | L1 | **每次会话自动加载**（必须极短） |
| `./docs/ai/architecture.md` | L2 | 理解结构 / 改模块时 **主动 Read** |
| `./docs/ai/conventions.md` | L3 | 编写代码时 **主动 Read** |
| `./docs/ai/ops.md` | L4 | 测试 / 部署 / 排错时 **主动 Read** |

### ⚠️ 核心原则：文件级按需加载

**渐进式披露 ≠ 在一个 md 里用 `## L2` 分段。**

| 做法 | 是否正确 |
|------|----------|
| L1–L4 全写在 `CLAUDE.md` | ❌ 错误（整文件总会进上下文） |
| `CLAUDE.md` 仅 L1 + 路径索引；L2–L4 独立文件 | ✅ 正确 |

注释 `<!-- 按需加载 -->` **没有执行力**。只有**拆文件 + 在 L1 写明「何时 Read 哪个路径」**，模型才会少带上下文。

### 正确 vs 错误

```
❌ 单文件伪渐进：
CLAUDE.md
  ├── 一句话 + Tech Stack
  ├── ## L2: 架构（仍在同一文件）
  ├── ## L3: 规范
  └── ## L4: 细节
→ Agent 加载 CLAUDE.md 时 L2–L4 一并注入

✅ 多文件真渐进：
CLAUDE.md                      # 仅 L1 + 索引表
docs/ai/architecture.md        # L2
docs/ai/conventions.md         # L3
docs/ai/ops.md                 # L4
→ 默认只注入 L1；任务需要时再 Read 对应文件
```

## Subagent Orchestration（跨 CLI，必须先读）

**详细规范：** 执行前 Read  
`references/orchestration.md`（语义角色 + **Claude Code / Grok / 其他** 宿主适配）。

本 skill **不绑定** Grok Build；在 **Claude Code**、Codex、Cursor 等只要加载了本 skill 即可用。

### 一句话

| 层 | 内容 |
|----|------|
| **可移植** | `agents/*.md` 角色、多文件产物、规模门控、分析只读 / Merger 可写 |
| **随宿主** | 工具名（`Agent` vs `spawn_subagent`）、能否限权、model 参数 |

默认 **继承当前会话模型**；禁止在 skill 流程里写死具体 model id。

### 规模门控（摘要）

| 规模 | 策略 |
|------|------|
| **S** | 主会话串行全角色，**不**开子 agent |
| **M** | 并行只读：Frontend + Backend（Claude Code 用 `Agent`；Grok 用 `explore`） |
| **L** | Scanner → Planner → 并行 FE/BE/QA → **主会话** Merger |

### 语义角色 → 行为（摘要）

| 角色 | 能力 | 写盘 | 典型宿主映射 |
|------|------|------|----------------|
| Scanner / FE / BE / QA / Auditor | 只读探索 | 否 | Claude `Agent`（禁写）/ Grok `explore`+read-only |
| Planner | 只读规划 | 否 | Claude `Agent` / Grok `plan`+read-only |
| Merger | 合并落盘 | **是** | **始终优先主会话** Write/Edit |

- 子 agent **禁止** 写 `CLAUDE.md` / `docs/ai/*`  
- 无子 agent 或失败 → **降级 S 串行**（产物规范不变）  
- 宿主专有参数见 `orchestration.md` §4，勿把 Grok 字段套到 Claude 上（反之亦然）

### Generation 流水线（M/L）

```
主: 识别宿主 + 门控
  → 只读 Scanner → 只读 Planner
  → 并行只读 Frontend | Backend | QA
  → 主会话 Merger 写 4 文件 → 报告路径
```

## Two Modes

### 1. Generation Mode（生成模式）

**触发：** 新项目、缺失 CLAUDE.md、或「初始化项目」

```
0. Read references/orchestration.md + 识别宿主 + 规模门控
1. Scanner   → 文件结构、技术栈（只读子 agent 或主会话）
2. Planner   → 架构与分层落盘计划（只读）
3. Frontend  → 前端模式（可与 Backend 并行，只读）
4. Backend   → 后端模式
5. QA        → 测试、约束
6. Merger    → 主会话写入 4 个文件（禁止合成单文件）
```

### 2. Update Mode（更新模式）

#### Mode A: 主动审计

```
用户: 检查 CLAUDE.md 是否需要更新
  → 读取 CLAUDE.md + docs/ai/*.md
  → Scanner（只读）扫描代码库
  → 差异报告 → 用户确认 → 主 Agent 按层改对应文件
```

#### Mode B: 被动学习

```
会话中新信息（如 "用 pnpm"）
  → 识别落在哪一层 / 哪个文件
  → 建议更新 → 用户确认 → 主 Agent 只改该文件（不 spawn）
```

## Trigger Keywords

| 关键词 | 动作 |
|--------|------|
| `创建 CLAUDE.md` / `帮我创建` | 生成四文件套件 |
| `优化 CLAUDE.md` | 分析并改进（仍保持多文件） |
| `更新 CLAUDE.md` | 审计后更新对应层文件 |
| `检查 CLAUDE.md` / `审计` | 主动审计 |
| `初始化项目` | 生成作为初始化的一部分 |
| `分析项目结构` | 仅分析，不写入 |

## Agent Responsibilities

| Agent | 职责 | 关键输出 | 执行方（默认，跨 CLI） |
|-------|------|----------|------------------------|
| **Scanner** | 扫描结构 | 文件树、技术栈 | 只读子 agent 或主会话 |
| **Planner** | 架构与落盘计划 | 每层内容 + **目标路径** | 只读子 agent 或主会话 |
| **Frontend** | 前端分析 | 组件/路由/状态素材 | 只读（可与 Backend 并行） |
| **Backend** | 后端分析 | API/数据素材 | 只读（可与 Frontend 并行） |
| **QA** | 测试与约束 | L3/L4 素材 | 只读 |
| **Merger** | 落盘 | **4 个文件** | **主会话**（禁止多 writer 抢写） |

## Output Layout（强制）

### 目录

```
project-root/
├── CLAUDE.md                 # L1 only
└── docs/
    └── ai/
        ├── architecture.md   # L2
        ├── conventions.md    # L3
        └── ops.md            # L4
```

若项目已有 `docs/`，仍使用 `docs/ai/` 子目录，避免污染业务文档。

### CLAUDE.md（L1 only，~100 tokens，硬限 150）

```markdown
# Project Name

一句话描述项目是做什么的。

## Tech Stack
- Frontend: [框架]
- Backend: [框架]
- Database: [数据库]
- Package Manager: [npm/yarn/pnpm]

## Quick Commands
```bash
npm install
npm run dev
```

## Progressive Docs（按需 Read，勿整份粘贴进 CLAUDE.md）

| 何时 | 文件 |
|------|------|
| 理解结构 / 改模块 / 数据流 | `docs/ai/architecture.md` |
| 写代码 / 命名 / API 约定 | `docs/ai/conventions.md` |
| 测试 / 部署 / 环境 / 坑 | `docs/ai/ops.md` |

**指令给 Agent：** 仅在当前任务需要时用 Read 工具打开上表路径；不要把 L2–L4 内容复制进本文件。
```

### docs/ai/architecture.md（L2，~300 tokens）

目录结构、核心模块表、数据流。开头可写：`# Architecture (L2)`。

### docs/ai/conventions.md（L3，~400 tokens）

命名、文件组织、API 模式、前后端约定。开头：`# Conventions (L3)`。

### docs/ai/ops.md（L4，~500–800 tokens）

测试、部署/运行、环境变量、Constraints & Gotchas。开头：`# Ops (L4)`。

## Token Budget

| Layer | File | Target | Hard Limit |
|-------|------|--------|------------|
| L1 | `CLAUDE.md` | ~100 | 150 |
| L2 | `docs/ai/architecture.md` | ~300 | 400 |
| L3 | `docs/ai/conventions.md` | ~400 | 500 |
| L4 | `docs/ai/ops.md` | ~500+ | 800 |

## Migration：已有单文件 CLAUDE.md

若发现 `CLAUDE.md` 内含 `## L2` / `## L3` / `## L4` 或大段架构/规范：

1. 抽取 L1 重写为短 `CLAUDE.md` + 索引表
2. 将其余内容拆到 `docs/ai/*.md`
3. **删除** 原 `CLAUDE.md` 中的 L2–L4 正文
4. 向用户说明：已从「单文件伪渐进」迁移到「多文件真渐进」

## Update Scope

```
[1] 仅 L1 → 编辑 CLAUDE.md
[2] L1 + L2 → CLAUDE.md + architecture.md
[3] L3 → conventions.md
[4] L4 → ops.md
[5] 全部 → 四个文件
[6] 自选
```

## File Discovery Priority

```
./CLAUDE.md                 # L1（会话默认加载）
./docs/ai/architecture.md   # L2
./docs/ai/conventions.md    # L3
./docs/ai/ops.md            # L4
./.claude.local.md          # 本地覆盖（可选）
./packages/*/CLAUDE.md      # monorepo 包级 L1（可选，仍应短）
```

## Project Type Detection

| Indicators | Project Type |
|------------|--------------|
| package.json, tsconfig.json | TypeScript |
| package.json, vite.config.ts | Vite + TS |
| package.json, next.config.js | Next.js |
| requirements.txt, manage.py | Django |
| go.mod | Go |
| Cargo.toml | Rust |

## Constraints Placement

| Type | File |
|------|------|
| 一句话 / 栈 / 命令 | CLAUDE.md (L1) |
| 目录与模块 / 数据流 | architecture.md (L2) |
| 命名与 API 约定 | conventions.md (L3) |
| 环境变量 / 测试 / 部署 / 坑 | ops.md (L4) |

## Hard Rules（Agent 必须遵守）

1. **禁止** 把 L2–L4 正文写入 `CLAUDE.md`
2. **禁止** 只靠 `## L2` 标题冒充渐进
3. **必须** 创建 `docs/ai/` 下三个文件（除非用户明确要求其他路径）
4. **必须** 在 L1 提供路径索引表与「何时 Read」说明
5. 更新时只改相关文件，保持 L1 始终可独立理解
6. 每个文件开头标明层级，便于审计
7. **必须** 按 `references/orchestration.md` 做规模门控与权限分离（分析只读、合并可写）
8. **禁止** 写死过期/臆造的 model id；默认继承**当前会话**；仅用户明确指定且宿主支持时设 model
9. **禁止** 多个 writer 并行写同一路径
10. **禁止** 把单一宿主 API（如仅 Grok 的字段）当成唯一实现；按 §4 宿主适配翻译
