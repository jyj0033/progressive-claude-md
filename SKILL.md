---
name: progressive-claude-md
description: Use when user asks to create, generate, update, audit, or maintain CLAUDE.md files. Also triggers when user says "初始化项目", "分析项目结构", or needs to understand project context. Activates Scanner, Planner, Frontend, Backend, QA agents to analyze codebase.
tools: Read, Edit, Glob, Grep, Bash, Agent
---

# Progressive CLAUDE.md Generator

## Overview

生成和更新结构化的**四层渐进式** CLAUDE.md 文件。

### 渐进式披露的核心原则

**不是把全部内容写在一起，而是分层组织：**

| 层级 | 作用 | 什么时候看 |
|------|------|-----------|
| **L1** | 核心概要，让 AI 5 秒理解项目 | 每次会话开始 |
| **L2** | 架构详情，理解项目结构 | 需要理解结构时 |
| **L3** | 代码规范，知道怎么写代码 | 编写代码时 |
| **L4** | 深入细节，测试/部署/约束 | 复杂任务时 |

**关键**：L1 要简洁（约 100 tokens），详细规范放在 L2-L4。

### 渐进式 vs 非渐进式

```
❌ 非渐进式（错误）：
# Project
[所有内容都堆在一起，没有层次]

✅ 渐进式（正确）：
# Project
[简洁的一两句话 + Tech Stack + 关键命令]

## L2: 架构
[目录结构 + 核心模块]

## L3: 规范
[代码规范]

## L4: 细节
[测试 + 部署 + 约束]
```

## Two Modes

### 1. Generation Mode (生成模式)

**触发条件：** 新项目或缺失 CLAUDE.md

```
┌─────────────────────────────────────────────────────────────┐
│  Generation Mode                                             │
├─────────────────────────────────────────────────────────────┤
│  1. Scanner   → 文件结构、技术栈                             │
│  2. Planner  → 架构分析、模块关系                           │
│  3. Frontend → 前端模式分析                                 │
│  4. Backend  → 后端模式分析                                 │
│  5. QA       → 测试规范、代码约定                           │
│  6. Merger   → 合并生成四层 CLAUDE.md                      │
└─────────────────────────────────────────────────────────────┘
```

### 2. Update Mode (更新模式)

**触发条件：** 已有 CLAUDE.md 需要维护

#### Mode A: Proactive Audit (主动审计)

```
用户: "检查 CLAUDE.md 是否需要更新"

    ↓
Scanner 扫描代码库变化
    ↓
对比现有 CLAUDE.md 内容
    ↓
输出差异报告 → 用户确认 → 选择性更新
```

#### Mode B: Passive Learning (被动学习)

```
用户会话中提及新信息 (如 "这个项目用 pnpm")

    ↓
识别 CLAUDE.md 更新点
    ↓
建议更新 → 用户确认 → 自动更新
```

## Trigger Keywords

| 关键词 | 触发动作 |
|--------|----------|
| `创建 CLAUDE.md` | 生成新文件 |
| `帮我创建` | 生成新文件 |
| `优化 CLAUDE.md` | 分析并改进 |
| `更新 CLAUDE.md` | 审计后更新 |
| `检查 CLAUDE.md` | 主动审计 |
| `审计 CLAUDE.md` | 主动审计 |
| `初始化项目` | 生成作为初始化的一部分 |
| `分析项目结构` | 仅分析，不写入 |
| `CLAUDE.md 维护` | 同检查/更新 |

## Agent Responsibilities

| Agent | 职责 | 关键输出 |
|-------|------|----------|
| **Scanner** | 扫描项目文件结构 | 文件树、技术栈列表、依赖文件 |
| **Planner** | 架构分析 | 项目类型、模块关系、四层内容规划 |
| **Frontend** | 前端代码分析 | 组件结构、路由、状态管理、前端规范 |
| **Backend** | 后端代码分析 | API 结构、数据模型、服务层、后端规范 |
| **QA** | 测试与约定 | 测试模式、代码规范、Gotchas、约束 |
| **Merger** | 合并生成 | 最终的四层 CLAUDE.md |

## Four-Layer Structure

### ⚠️ 重要：渐进式披露的含义

**渐进式披露 = 不是把所有内容堆在一起！**

- **L1** 是核心概要，约 100 tokens，给 AI 快速理解项目
- **L2-L4** 是详细参考，按需加载
- **文件结构**：L1 在开头，L2-L4 在后面，用 `## L2:`, `## L3:`, `## L4:` 区分

### 错误的输出方式 ❌

```markdown
# Project Name

[所有内容都写在这里，没有分层...]
```

### 正确的输出方式 ✅

```markdown
# Project Name

一句话描述项目是做什么的。

## Tech Stack
- Frontend: [框架]
- Backend: [框架]
- Database: [数据库]

## Quick Commands
```bash
npm install && npm run dev
```

<!-- L2+: 详细参考，按需加载 -->

## L2: 技术栈与架构

[详细的目录结构、模块说明]

## L3: 代码规范

[命名规范、代码约定]

## L4: 深入细节

[测试、部署、约束]
```

### L1: Quick Start (~100 tokens)

**触发时机：** 每次会话开始
**目的：** 立即了解项目是什么
**位置：** 必须放在文件最开头

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
```

### L2: Architecture (~300 tokens)

**触发时机：** 理解项目结构时
**目的：** 项目是如何组织的

```markdown
## Project Structure

src/
├── components/     # UI 组件
├── pages/          # 页面/路由
├── api/            # API 调用
└── ...

## Core Modules

| Module | Purpose |
|--------|---------|
| auth/ | 认证相关 |
| api/ | API 接口 |
| store/ | 状态管理 |

## Data Flow

[数据流向说明]
```

### L3: Code Conventions (~400 tokens)

**触发时机：** 编写代码时
**目的：** 如何正确编写代码

```markdown
## Coding Standards

### Naming Conventions
- Components: PascalCase
- Utils: camelCase
- Constants: SCREAMING_SNAKE_CASE

### File Organization
- One component per file
- Colocation: test files beside source

### API Patterns
- RESTful conventions
- Error response format
```

### L4: Deep Details (~500+ tokens)

**触发时机：** 复杂任务时
**目的：** 需要时的详细指导

```markdown
## Testing

### Framework
- Unit: Vitest
- E2E: Playwright

### Patterns
- [测试模式说明]

## Deployment

### Commands
```bash
npm run build
npm run deploy
```

## Constraints & Gotchas ⚠️

### Environment
- Requires Node 18+
- 需要配置 .env 文件（见 .env.example）

### Known Issues
- [已知问题]

### Limitations
- 不支持 IE 浏览器
- 移动端暂未优化
```

## Token Budget

### ⚠️ 严格遵守 Token 预算

| Layer | Target | Hard Limit | 内容范围 |
|-------|--------|------------|----------|
| **L1** | ~100 | 150 | 一句话描述 + 技术栈 + 关键命令 |
| **L2** | ~300 | 400 | 目录结构 + 核心模块 + 数据流 |
| **L3** | ~400 | 500 | 命名规范 + 代码约定 + API 模式 |
| **L4** | ~500+ | 800 | 测试 + 部署 + 约束 |

### Token 预算的含义

- **L1 ~100 tokens**：不是 100 行，是 ~100 个英文单词的中文翻译量
- **L2 ~300 tokens**：中等详细程度的架构说明
- **L3 ~400 tokens**：完整的代码规范
- **L4 ~500+ tokens**：详细但不冗余的补充信息

### ⚠️ 常见错误：把所有内容放在 L1

错误示例：
```markdown
# Project Name

## 项目说明
这是一个使用 React + Node.js 构建的 Web 应用...

## 技术栈
- 前端: React 18, TypeScript, Vite
- 后端: Node.js, Express, MongoDB
...

## 代码规范
[所有详细规范都放在这里]
```

正确做法：
```markdown
# Project Name

一句话描述项目。

## Tech Stack
- Frontend: React
- Backend: Node.js

## Quick Commands
npm install && npm run dev

<!-- 详细规范见下方，按需加载 -->

## L2: 技术栈与架构

[详细目录结构和模块说明]

## L3: 代码规范

[详细命名规范和约定]

## L4: 深入细节

[测试、部署、约束]
```

## Update Mode Details

### Update Triggers

| 触发方式 | 模式 | 说明 |
|----------|------|------|
| `检查 CLAUDE.md` | Audit | 主动审计完整性 |
| `更新 CLAUDE.md` | Audit | 基于最新代码库更新 |
| 会话中学到新信息 | Passive | 建议性更新 |
| `#` 快捷键 | Passive | 官方快捷键，功能类似 |
| `CLAUDE.md 维护` | Audit | 同检查/更新 |

### Update Scope Control

```
## 更新选项

[1] 仅更新 L1 (快速开始) - 新增技术栈、命令变更
[2] 更新 L1 + L2 (概览) - 新增模块、重构
[3] 更新 L3 (规范) - 代码约定变化
[4] 更新 L4 (细节) - 测试、部署、约束变化
[5] 全部更新 - 完整刷新
[6] 选择具体部分 - 手动选择
```

### Audit Mode Flow

```
1. 读取现有 CLAUDE.md
2. Scanner 扫描代码库最新状态
3. 对比并输出差异报告:

## CLAUDE.md 审计报告

| 层级 | 状态 | 变化 |
|------|------|------|
| L1 | ✓/⚠️/✗ | [变化描述] |
| L2 | ✓/⚠️/✗ | [变化描述] |
| L3 | ✓/⚠️/✗ | [变化描述] |
| L4 | ✓/⚠️/✗ | [变化描述] |

4. 用户选择更新范围
5. Merger 生成更新后的内容
6. 使用 Edit 工具更新文件
```

### Passive Learning Flow

```
1. 监听用户会话中的关键信息
2. 识别 CLAUDE.md 更新点:
   - 技术栈变更 (npm → pnpm)
   - 新增模块或目录
   - 代码规范变化
   - 测试命令变更
   - 环境配置变更

3. 建议更新:

## 💡 建议更新 CLAUDE.md

**层级:** L1
**当前内容:**
npm install && npm run dev

**建议内容:**
pnpm install && pnpm dev

是否更新？ [是] [否] [查看上下文]
```

## File Discovery Priority

```
./CLAUDE.md                    # Primary (git-tracked)
./.claude.local.md            # Local overrides
~/.claude/CLAUDE.md           # Global defaults
./packages/*/CLAUDE.md        # Monorepo packages
```

## Project Type Detection

| Indicators | Project Type |
|------------|--------------|
| package.json, tsconfig.json | TypeScript Project |
| package.json, vite.config.ts | Vite + TS |
| package.json, next.config.js | Next.js |
| package.json, nuxt.config.ts | Nuxt.js |
| requirements.txt, manage.py | Python/Django |
| requirements.txt, app.py | Python/Flask |
| go.mod | Go Project |
| Cargo.toml | Rust Project |
| pom.xml | Java/Maven |
| build.gradle | Kotlin/Gradle |
| composer.json | PHP/Composer |

## Constraints Placement

| Type | Location |
|------|----------|
| Environment requirements | L1 or L4 |
| Config dependencies (.env) | L4 Constraints section |
| Known bugs/limitations | L4 Constraints section |
| Code conventions | L3 |
| Business rules | L2 or L4 (by complexity) |
