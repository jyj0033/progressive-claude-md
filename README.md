# Progressive CLAUDE.md Generator

生成和维护**多文件渐进式**项目上下文：默认只让 Agent 加载短 `CLAUDE.md`（L1），架构/规范/运维拆到 `docs/ai/`，需要时再 Read。

**跨 CLI：** 同一套 skill 可在 **Claude Code**、**Grok Build**、Codex、Cursor 及其他支持 Agent Skills 的工具中使用。角色与产物可移植；子代理工具名按宿主适配（见 `references/orchestration.md`）。

## 为什么必须多文件？

多数 Agent 会**整份注入** `CLAUDE.md`。若 L2–L4 写在同一文件里，所谓「按需加载」无效。

```
✅ 真渐进          ❌ 伪渐进
CLAUDE.md (L1)     CLAUDE.md
docs/ai/L2.md        ├── L1
docs/ai/L3.md        ├── ## L2
docs/ai/L4.md        ├── ## L3
                     └── ## L4  ← 仍会全部进上下文
```

## 落盘结构

```
project/
├── CLAUDE.md                      # L1：描述 + 栈 + 命令 + 索引表
└── docs/ai/
    ├── architecture.md            # L2
    ├── conventions.md             # L3
    └── ops.md                     # L4
```

## 特性

- **文件级渐进披露**：L1 自动加载；L2–L4 按任务 Read
- **跨宿主调度**：`references/orchestration.md`
  - 语义角色：`read-explore` / `read-plan` / `write-merge`
  - Claude Code → `Agent` 只读 + 主会话写盘  
  - Grok Build → `explore`/`plan` + 主会话写盘  
  - 无子代理 → 主会话串行（产物不变）
- **模型**：默认跟随当前会话；skill 不写死 model id
- **生成 / 审计 / 被动学习**
- **迁移**：单文件伪渐进 → 自动拆成四文件

## 安装

```bash
# skills CLI（若可用）
npx skills add jyj0033/progressive-claude-md -g -y

# 或拷到各工具 skill 目录（按你本机习惯）
# Claude Code:  ~/.claude/skills/progressive-claude-md
# 通用/多工具: ~/.agents/skills/progressive-claude-md
# Grok 等常 symlink 到上述路径
```

本地改过规范时，以本机 skill 目录为准（可能新于 GitHub）。

## 使用（任意支持的 CLI）

```
帮我创建 CLAUDE.md
初始化项目
检查 CLAUDE.md 是否需要更新
分析项目结构
```

## Token 预算

| 层级 | 文件 | 预算 |
|------|------|------|
| L1 | CLAUDE.md | ~100 |
| L2 | docs/ai/architecture.md | ~300 |
| L3 | docs/ai/conventions.md | ~400 |
| L4 | docs/ai/ops.md | ~500+ |

## Skill 包结构

```
progressive-claude-md/
├── SKILL.md
├── agents/                 # 可移植角色提示词
├── templates/layer-template.md
└── references/
    ├── orchestration.md    # 跨 CLI 调度（先读）
    └── project-types.md
```

## 模型与多 CLI

| 做法 | 说明 |
|------|------|
| 默认 | 子任务 = 当前会话模型 |
| Claude Code | 用会话 `/model` 或 Agent 文档支持的参数；用户点名再改 |
| Grok Build | spawn 默认不传 model；可用 persona 等宿主配置 |
| 本 skill | **不**内置具体 model slug，避免过期与绑死厂商 |
