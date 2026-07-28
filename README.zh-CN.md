# Progressive CLAUDE.md

[English](README.md) | 简体中文

一个 Claude Code CLI 插件。它依据仓库中的实际证据和 Claude Code 的真实加载边界，生成、审计并安全更新项目指令。

## v2 的变化

- 使用简洁的根目录 `CLAUDE.md`、限定路径范围的 `.claude/rules`、嵌套的 `CLAUDE.md` 和任务技能，取代四个始终加载的标题层级。
- 注册只读子代理：Scanner、Planner、Frontend、Backend、QA/Infra、Auditor、Merger、Change Detector 和 Validator。
- 仅调用适用的代理，并行执行相互独立的领域分析。
- 要求为生成的事实提供源码证据，并仅允许主会话写入文件。
- 通过最小化且经过验证的补丁，保留已有的人工编写内容。

## 安装到 Claude Code CLI

将此目录放置在：

```text
~/.claude/skills/progressive-claude-md/
```

由于目录中包含 `.claude-plugin/plugin.json`，Claude Code 会在下次会话中将其识别为 `progressive-claude-md@skills-dir`，无需通过 Marketplace 安装。

如需从其他目录进行本地开发，请运行：

```bash
claude --plugin-dir /absolute/path/to/progressive-claude-md
```

修改 `agents/` 或插件清单后，请重启 Claude Code 或运行 `/reload-plugins`。对 `SKILL.md` 的修改会被实时检测。

## 使用方法

直接调用该技能：

```text
/progressive-claude-md:progressive-claude-md generate
/progressive-claude-md:progressive-claude-md audit
/progressive-claude-md:progressive-claude-md update
/progressive-claude-md:progressive-claude-md analyze
```

明确提到创建、审计或更新 Claude Code 项目指令的自然语言请求，也可以自动触发该技能。

只读请求始终保持只读。生成和更新请求仅会在收集证据、验证候选内容并检查作用域之后写入文件。

## 校验

在插件根目录中运行：

```bash
python scripts/validate_plugin.py
claude plugin validate . --strict
```

在项目会话中使用 `/memory` 检查已加载的指令，使用 `/doctor` 查找内容过多或可从仓库推导的 `CLAUDE.md` 内容。

## 运行时目录结构

```text
progressive-claude-md/
├── .claude-plugin/plugin.json
├── SKILL.md
├── agents/
│   ├── scanner.md
│   ├── planner.md
│   ├── frontend-analyzer.md
│   ├── backend-analyzer.md
│   ├── qa-analyzer.md
│   ├── auditor.md
│   ├── merger.md
│   ├── change-detector.md
│   └── validator.md
├── references/
│   ├── claude-loading.md
│   ├── contracts.md
│   ├── workflows.md
│   └── project-types.md
├── templates/layer-template.md
└── scripts/validate_plugin.py
```

所有子代理均为只读。`change-detector.md` 是非持久代理；技能调用结束后，它不会继续监控对话。
