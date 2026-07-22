# Progressive CLAUDE.md Generator

一个 Claude Code Skill，用于生成和维护结构化的渐进式 CLAUDE.md 文件。

## 特性

- **渐进式披露**: 四层结构 (L1-L4)，按需加载上下文
- **多 Agent 协作**: Scanner, Planner, Frontend, Backend, QA, Merger
- **双模式**: 生成模式 + 更新模式
- **被动学习**: 会话中自动识别 CLAUDE.md 更新点

## 安装

```bash
# 复制到项目目录
cp -r progressive-claude-md ~/.claude/skills/

# 或在项目中创建
mkdir -p .claude/skills
cp -r progressive-claude-md .claude/skills/
```

## 使用方法

### 生成 CLAUDE.md

```bash
# 进入项目目录
cd your-project

# 启动 Claude Code
claude

# 输入触发命令
帮我创建 CLAUDE.md
```

### 更新 CLAUDE.md

```bash
# 主动审计
检查 CLAUDE.md 是否需要更新

# 被动学习
这个项目用 pnpm，不是 npm
```

### 分析项目结构

```bash
分析项目结构
```

## 四层结构

| 层级 | Token 预算 | 触发时机 |
|------|------------|----------|
| L1 | ~100 | 每次会话 |
| L2 | ~300 | 理解结构 |
| L3 | ~400 | 编写代码 |
| L4 | ~500+ | 复杂任务 |

## 文件结构

```
progressive-claude-md/
├── SKILL.md                  # 主技能文件
├── agents/                   # Agent 提示词
│   ├── scanner.md           # 扫描器
│   ├── planner.md           # 规划师
│   ├── frontend.md          # 前端
│   ├── backend.md           # 后端
│   ├── qa.md               # 测试
│   ├── merger.md            # 合并器
│   ├── auditor.md          # 审计器
│   └── learner.md           # 被动学习
├── templates/                # 模板
│   └── layer-template.md    # 四层模板
└── references/               # 参考
    └── project-types.md     # 项目类型检测
```

## 更新模式

### 主动审计

```
用户: "检查 CLAUDE.md 是否需要更新"
↓
Scanner 扫描代码库
↓
对比现有内容
↓
输出差异报告
↓
用户确认
↓
选择性更新
```

### 被动学习

```
用户会话中提及新信息
↓
识别 CLAUDE.md 更新点
↓
建议更新
↓
用户确认
↓
自动更新
```

## 更新范围控制

```
[1] 仅更新 L1 (快速开始)
[2] 更新 L1 + L2 (概览)
[3] 更新 L3 (规范)
[4] 更新 L4 (细节)
[5] 全部更新
[6] 选择具体部分
```

## 触发关键词

| 关键词 | 动作 |
|--------|------|
| `创建 CLAUDE.md` | 生成新文件 |
| `优化 CLAUDE.md` | 分析并改进 |
| `更新 CLAUDE.md` | 审计后更新 |
| `检查 CLAUDE.md` | 主动审计 |
| `初始化项目` | 生成初始化 |
| `分析项目结构` | 仅分析 |

## 设计文档

- 设计文档: `docs/superpowers/specs/2026-07-22-progressive-claude-md-design.md`
- 实现计划: `docs/superpowers/plans/2026-07-22-progressive-claude-md-plan.md`
