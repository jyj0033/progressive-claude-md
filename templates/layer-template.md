# Layer Template Reference

四层结构的模板参考。生成 CLAUDE.md 时按需使用。

## ⚠️ 重要：渐进式披露原则

**L1 = 简洁概要 | L2-L4 = 详细参考**

```
# Project Name
[L1: 一句话描述 + Tech Stack + 关键命令]

## L2: 架构
[L2: 详细目录结构]

## L3: 规范
[L3: 详细代码规范]

## L4: 细节
[L4: 测试 + 部署 + 约束]
```

**不是**把所有内容都放在文件开头！

---

## L1: Quick Start Template

```markdown
# [Project Name]

[One sentence describing what this project does]

## Tech Stack
- Frontend: [framework]
- Backend: [framework]
- Database: [database]
- Package Manager: [npm/yarn/pnpm]

## Quick Commands
```bash
[install command]
[dev command]
[build command]
```
```

**使用场景：** 项目初始化、会话开始、快速了解

---

## L2: Architecture Template

```markdown
## Project Structure

```
[directory tree - max 3 levels]
```

## Core Modules

| Module | Purpose |
|--------|---------|
| [path] | [description] |
| [path] | [description] |

## Data Flow

[How data flows through the system - one paragraph]
```

**使用场景：** 理解项目结构、理解模块关系

---

## L3: Code Conventions Template

```markdown
## Coding Standards

### Naming Conventions
- Components: PascalCase
- Utils/Helpers: camelCase
- Constants: SCREAMING_SNAKE_CASE
- Types/Interfaces: PascalCase with I prefix (optional)

### File Organization
- One component per file
- Colocation: test files beside source (e.g., Button.tsx + Button.test.tsx)
- Barrel files (index.ts) for re-exports

### API Patterns
- RESTful conventions: GET/POST/PUT/DELETE
- Error response format: `{ error: string, code: string }`
- Request validation with [library]
```

**使用场景：** 编写代码、代码审查

---

## L4: Deep Details Template

```markdown
## Testing

### Framework
- Unit: [Jest/Vitest/Mocha/etc.]
- E2E: [Playwright/Cypress/Selenium]
- Integration: [library]

### Patterns
- [testing patterns used]
- Mocking strategy: [approach]

### Commands
```bash
[unit test command]
[e2e test command]
[coverage command]
```

## Deployment

### Build
```bash
[build command]
```

### Deploy
```bash
[deploy command]
```

### Environment Setup
1. [step 1]
2. [step 2]
3. [step 3]

## Constraints & Gotchas ⚠️

### Environment
- Node version: [version]
- Required env vars:
  - `DATABASE_URL`: [description]
  - `API_KEY`: [description]
- Required tools: [tools]

### Known Issues
- [issue 1]
- [issue 2]

### Limitations
- [limitation 1]
- [limitation 2]
```

**使用场景：** 复杂任务、测试、部署、问题排查

---

## Layer Token Budget

| Layer | Target | Hard Limit | Content |
|-------|--------|------------|---------|
| L1 | ~100 | 150 | 一句话描述 + 技术栈 + 命令 |
| L2 | ~300 | 400 | 目录结构 + 核心模块 + 数据流 |
| L3 | ~400 | 500 | 命名规范 + 代码约定 + API 模式 |
| L4 | ~500+ | 800 | 测试 + 部署 + 约束 |

---

## Constraints Placement Guide

| Type | L1 | L2 | L3 | L4 |
|------|----|----|----|----|
| 环境要求 | ✓ | | | ✓ |
| 配置依赖 | | | | ✓ |
| 命名规范 | | | ✓ | |
| 代码约定 | | | ✓ | |
| API 模式 | | | ✓ | |
| 测试命令 | | | | ✓ |
| 部署命令 | | | | ✓ |
| 已知问题 | | | | ✓ |
| 限制说明 | | | | ✓ |
