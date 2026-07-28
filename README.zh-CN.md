# Progressive CLAUDE.md

[English](README.md) | 简体中文

一个专注于生成渐进式项目指令的 Claude Code CLI 插件。它依据仓库证据和 Claude Code 的真实加载边界组织文件。对外入口保持简单：默认命令负责生成，`check` 只读检查现有布局。

## 生成内容

- 简洁的根目录 `CLAUDE.md`，用于整个仓库都适用的指令。
- 带路径范围的 `.claude/rules/*.md`，用于只对匹配文件生效的指令。
- 嵌套的 `CLAUDE.md`，用于特定包或子目录的指令。
- 任务技能，用于仅在调用时加载的详细流程。

它不会把一个大型 Markdown 文件中的标题误当成懒加载层级。

## 工作方式

- 先扫描仓库证据，再提出项目指令。
- 只调用适用的只读子代理：Scanner、Planner、Frontend、Backend、QA/Infra、Auditor、Merger 和 Validator。
- 当仓库规模值得并行处理时，并行运行相互独立的领域分析。
- 仅允许主会话写入文件。
- 通过最小化且经过验证的补丁保留已有人工内容。

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

在仓库根目录生成渐进式项目指令：

```text
/progressive-claude-md:progressive-claude-md
```

将生成范围限制到指定目录：

```text
/progressive-claude-md:progressive-claude-md packages/api
```

只读检查现有布局：

```text
/progressive-claude-md:progressive-claude-md check
/progressive-claude-md:progressive-claude-md check packages/api
```

如果项目尚无指令文件，默认命令会创建满足需要的最小渐进式布局；如果已有指令文件，则保留人工编写内容，只应用维持布局准确性所需且经过验证的变更。

明确提到生成或检查渐进式 Claude Code 项目指令的自然语言请求，也可以触发该技能。`check` 始终只读。

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
│   └── validator.md
├── references/
│   ├── claude-loading.md
│   ├── contracts.md
│   ├── workflows.md
│   └── project-types.md
├── templates/layer-template.md
└── scripts/validate_plugin.py
```

所有子代理均为只读，只有主会话可以写入经过验证的生成结果。
