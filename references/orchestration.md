# Subagent Orchestration（跨 CLI 调度规范）

本 skill 面向 **多种 Agent CLI / IDE**，不绑定某一家产品。

已知会加载本 skill 的环境包括（不限于）：

| 宿主 | 典型入口 | 子代理机制（名称因版本而异） |
|------|----------|------------------------------|
| **Claude Code**（优先说明） | `claude` | `Agent` 工具 / 子 agent |
| **Grok Build** | `grok` | `spawn_subagent` |
| **Codex / Cursor / 其他** | 各 CLI 或 Agent 模式 | 自带 Task/Subagent，或无则主会话串行 |

`agents/*.md` = **可移植的角色剧本**（与宿主无关）。  
**是否 spawn、工具名、模型参数** = 宿主相关；先看本文 **§2 语义角色**，再映射 **§4 宿主适配**。

---

## 1. 可移植原则（所有宿主相同）

| 原则 | 说明 |
|------|------|
| **角色 ≠ 必须起子进程** | 见规模门控；S 项目主会话串行即可 |
| **语义能力匹配** | 探索只读 / 规划只读 / 合并可写——用宿主最接近的能力表达 |
| **写权限收口** | 分析阶段 **禁止写盘**；仅 Merger（优先主会话）写 `CLAUDE.md` + `docs/ai/*` |
| **模型不写死** | skill **禁止**写死 `claude-opus-*` / `grok-*` 等会过期的 id；默认跟**当前会话** |
| **主会话是编排器** | 门控 → 派活 → 汇总 → Merger → 对用户报告 |
| **无子代理则降级** | 任何宿主关掉 subagent 或工具失败 → **S 串行**，结果仍须多文件落盘 |

### 「合适的模型」在跨 CLI 下的含义

1. **默认**：子任务继承**当前会话模型**（Claude Code / Grok / 其他皆然）。  
2. **「合适」优先指能力画像**，不是品牌：  
   - 扫库 / 分端分析 → 快、短输出、只读  
   - 规划分层 → 结构化、只读  
   - 合并落盘 → 与主会话同模型、可写、遵守多文件规范  
3. **仅当用户明确指定**（如「用 Sonnet 扫、用 Opus 合并」）且宿主支持时，才在子 agent 参数里设 model。  
4. **禁止**在 skill 正文写死具体 model slug。

---

## 2. 语义角色表（宿主无关）

把 PCM 角色映射到**能力标签**；宿主适配时只翻译标签，不改流水线语义。

| PCM 角色 | 能力标签 | 写盘 | 角色文件 | 输出 |
|----------|----------|------|----------|------|
| Scanner | `read-explore` | 否 | `agents/scanner.md` | Scanner Results |
| Planner | `read-plan` | 否 | `agents/planner.md` | Planner Results |
| Frontend | `read-explore` | 否 | `agents/frontend.md` | Frontend Analysis |
| Backend | `read-explore` | 否 | `agents/backend.md` | Backend Analysis |
| QA | `read-explore` | 否 | `agents/qa.md` | QA Analysis |
| Auditor | `read-explore` | 否 | `agents/auditor.md` | 审计报告 |
| Merger | `write-merge` | **是** | `agents/merger.md` | 4 个文件 |

**禁止**：`read-*` 角色写 `CLAUDE.md` / `docs/ai/*`。  
**禁止**：多个 writer 并行写同一路径。  
**Merger 默认在主会话执行**（上下文已齐、少一次交接错误）。

---

## 3. 规模门控（所有宿主相同）

主会话先 list 根目录 + 看是否 monorepo / 前后端分离：

| 规模 | 条件（满足任一条） | 策略 |
|------|-------------------|------|
| **S** | 单包；源码 ≤ ~30 文件；无前后端拆分 | **不 spawn**；主会话按角色文件串行 |
| **M** | 2 包 monorepo 或前后端分离；约 30–150 源文件 | 并行 Frontend + Backend（只读）；Scanner/Planner 可主会话 |
| **L** | 多包 / 多 app；源码 > ~150 | Scanner → Planner → 并行 FE/BE/QA → 主会话 Merger |

- **主动审计**：默认 S；变更面大再升 M/L。  
- **被动学习**：永不 spawn；主会话改对应层文件。

---

## 4. 宿主适配（翻译层）

执行时：**先识别自己在哪个宿主**，再用下表把 §2 能力标签换成该宿主的工具调用。  
若表中工具名与当前版本不一致，用**等价物**（只读子 agent / 通用 agent + 提示禁止写文件）。

### 4.1 Claude Code（常用）

| 能力标签 | 推荐做法 |
|----------|----------|
| `read-explore` | 使用 **`Agent`**（或当前文档中的子 agent 工具）。prompt 贴对应 `agents/*.md`，明确：**只读、禁止 Edit/Write、禁止改 CLAUDE.md**。子 agent 工具集尽量不含写文件；若无法限制工具，用 prompt 硬约束 + 主会话复核。 |
| `read-plan` | 同上 `Agent`，强调输出 Planner 结构、**不落盘**。若有 Explore/Plan 类内置 subagent_type，优先用只读类。 |
| `write-merge` | **主会话**直接 Read/Write（或 Edit）：按 `merger.md` 写 4 文件。一般**不要**再开子 agent 写盘。 |
| 并行 | M/L：可同时开多个 Agent（Frontend / Backend / QA），主会话 `Task`/`Agent` 并行后汇总。 |
| model | 默认跟随会话。用户指定时用 Claude Code 支持的方式（会话 `/model` 或 Agent 参数——**以当前 Claude Code 文档为准**，不在 skill 写死 id）。 |
| 降级 | 无 Agent 工具或失败 → S 串行。 |

**Claude Code prompt 要点（所有只读 Agent）：**

```
工作目录: {PROJECT_ROOT}
你是 progressive-claude-md 的 {ROLE}。
严格遵循 skill 内 agents/{role}.md 的 Output Format。
允许: Read, Glob, Grep, Bash(只读用途)。
禁止: Write, Edit, 创建/删除文件, 修改 CLAUDE.md 或 docs/ai/*。
只返回规定 Markdown 章节，不要寒暄。
```

### 4.2 Grok Build

| 能力标签 | `subagent_type` | `capability_mode` |
|----------|-----------------|-------------------|
| `read-explore` | `explore` | `read-only` |
| `read-plan` | `plan` | `read-only` |
| `write-merge` | 主会话；或例外 `general-purpose` + `read-write` | — |

- `model`：默认**不传**（继承父会话）；仅用户点名且 slug 合法时传。  
- 子代理关闭（如 `GROK_SUBAGENTS=0`）→ S 串行。

### 4.3 Codex / Cursor / 其他 Agent CLI

| 能力标签 | 做法 |
|----------|------|
| `read-explore` / `read-plan` | 使用该产品的 **Task / Subagent / Delegate**；prompt 同 §4.1；要求只读。 |
| `write-merge` | 主会话写 4 文件。 |
| 无子代理 | S 串行；**产物规范不变**（多文件渐进）。 |

不要假设存在名为 `explore` 的类型——**语义对齐即可**。

---

## 5. 标准流水线（语义层，跨宿主）

### Generation（M/L）

```
[主] 识别宿主 + 规模门控
  ↓
[只读] Scanner
  ↓
[只读] Planner（输入 Scanner）
  ↓
[只读并行] Frontend | Backend | QA
  ↓
[主] 汇总
  ↓
[主·可写] Merger → CLAUDE.md + docs/ai/*.md
  ↓
[主] 报告 4 路径
```

S：同上顺序，全在主会话，不 spawn。

### Audit

```
[主/只读] 读现有 4 文件 + Scanner
[主] 差异报告 + 范围选项
用户确认
[主·可写] 只改选定层文件
```

---

## 6. 派生子任务时 prompt 必含（所有宿主）

1. `{PROJECT_ROOT}`  
2. 角色名 + 遵循 `agents/{role}.md`  
3. **禁止写盘**（read 角色）或 **只写 4 路径**（Merger）  
4. 跳过 `node_modules` / `.git` / `dist` / build  
5. 输出格式与字数上限  
6. 多文件目标路径（给 Planner/Merger）：

```
CLAUDE.md
docs/ai/architecture.md
docs/ai/conventions.md
docs/ai/ops.md
```

### Scanner（语义示例，宿主自行包装成 Agent 调用）

```
角色: Scanner | 只读 | 不写文件
输出: agents/scanner.md 的 Output Format
跳过 node_modules/.git/dist | 最多 ~200 words
```

### Frontend / Backend（并行）

```
Frontend: 仅前端目录 (web/, frontend/, apps/web, ...)
Backend: 仅后端目录 (server/, api/, apps/api, ...)
禁止写文件；返回各自 Analysis 格式
```

### Merger（主会话）

```
合并各 Analysis → 按 agents/merger.md 写 4 文件
禁止 L2–L4 进入 CLAUDE.md
完成后列出路径
```

---

## 7. 模型策略（跨 CLI）

| 场景 | 做法 |
|------|------|
| 默认 | 继承当前会话 / 父 agent |
| 用户指定 | 用**该宿主**支持的方式设置；skill 不写死 id |
| 想省成本扫库 | 短 prompt、限字、只读、少文件；不依赖未配置的「小模型」 |
| 多模型工作流 | 由用户在宿主设置（Claude 订阅档位、Grok persona、自定义 endpoint）；skill 只保证角色与权限 |

---

## 8. 失败与降级

| 情况 | 处理 |
|------|------|
| 无子代理 / 工具失败 | S：主会话串行 |
| 某一路 FE/BE 失败 | 主会话补扫该侧 → 继续 Merger |
| 只读子任务却写了文件 | 主会话审核；违反多文件规范则重写 |
| 结论冲突 | 以源码为准，主会话再读关键文件 |
| 宿主专有参数不认识 | 忽略专有字段，保留语义（只读/可写/并行） |

---

## 9. 结束前检查清单

- [ ] 已识别宿主（Claude Code / Grok / 其他 / 无子代理）  
- [ ] 规模门控 S/M/L  
- [ ] 分析阶段无写盘（或已纠正）  
- [ ] 仅主会话（Merger）写入  
- [ ] `CLAUDE.md` 仅 L1 + 索引  
- [ ] `docs/ai/{architecture,conventions,ops}.md` 存在  
- [ ] 未把 L2–L4 粘回 `CLAUDE.md`  
- [ ] 未写死过期 model id  
