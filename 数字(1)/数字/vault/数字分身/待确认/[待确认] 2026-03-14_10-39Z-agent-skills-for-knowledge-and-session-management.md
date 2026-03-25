---
type: 待确认
source: SpecStory/Cleaned
date: 2026-03-18
models: [claude-4.6-opus-high]
turns: 1
title: "Agent skills for knowledge and session management"
original_file: "[导出] 2026-03-18-2206-2026-03-14_10-39Z-agent-skills-for-knowledge-and-session-management.md"
status: pending
archive_title: ""
replaced_count: 0
---

# Agent skills for knowledge and session management
_Cleaned from SpecStory on 2026-03-18_


### 👤 用户

你是SK搜索助手。请在以下平台搜索两类技能：

## 搜索目标A：知识库管理
找到支持"Obsidian vault同步、知识图谱、实体关系、PKM"的agent skills。

## 搜索目标B：会话管理/上下文接续
找到支持"跨窗口交接、上下文压缩、长期记忆、session handoff"的agent skills。

## 搜索方法

### 知识库管理 - WebSearch搜索
- "clawhub obsidian knowledge graph skill"
- "clawhub knowledge base management PKM"
- "skills.sh obsidian vault knowledge graph"
- "github SKILL.md obsidian knowledge graph entity"
- "github agent-skills knowledge management PKM"
- "cursor agent skills obsidian ontology 2026"

### 会话管理 - WebSearch搜索
- "clawhub session management context handoff"
- "clawhub long term memory context compression"
- "skills.sh session handoff context"
- "github SKILL.md session context handoff memory"
- "github agent-skills context compression long-term memory"
- "cursor agent skills session management memory 2026"

## 输出要求
对每个类别的每个找到的候选SK，列出：
- 名称
- 来源
- 描述
- 星数/下载量
- 最后更新
- 安装方式
- URL

每类尽量找3个以上候选。明确区分两个类别的结果。

---


### 🤖 Cursor (claude-4.6-opus-high)

我开始在多个平台上并行搜索这两类技能。

**知识库管理类搜索：**

---

**会话管理类搜索：**

---

再补充搜索更多候选：

---

再补充几个关键细节搜索：

---

所有搜索完成，下面整理最终结果。

---

# SK搜索报告：知识库管理 & 会话管理/上下文接续

---

## 类别A：知识库管理（Obsidian / PKM / 知识图谱）

### 1. kepano/obsidian-skills（官方级）

| 项目 | 详情 |
|------|------|
| **名称** | obsidian-skills（含 obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli） |
| **来源** | GitHub / skills.sh / Tessl |
| **描述** | Obsidian 官方开发者 kepano 出品，教 AI agent 操作 Obsidian Flavored Markdown（wikilinks、callouts、properties、embeds）、Bases 文件、JSON Canvas 可视化画布、CLI 交互。是 Agent Skills 生态中 Obsidian 类最权威的仓库 |
| **星数** | **13,163 stars** / 715 forks / 总安装 4,200+ |
| **最后更新** | 2026-03-02 |
| **安装方式** | `npx skills add kepano/obsidian-skills` 或 `npx tessl i github:kepano/obsidian-skills` |
| **URL** | https://github.com/kepano/obsidian-skills |

### 2. obsidian-ontology-sync（已安装）

| 项目 | 详情 |
|------|------|
| **名称** | obsidian-ontology-sync v1.0.1 |
| **来源** | ClawHub / 本地已安装 |
| **描述** | 双向同步 Obsidian PKM（人类友好笔记）与结构化本体（机器可查询图谱）。自动从 Markdown 中提取实体和关系，维护本体图，并反馈改善笔记结构。支持 cron 定时同步 |
| **星数** | ClawHub 来源，openclaw/skills 仓库 1,086 stars |
| **最后更新** | 已安装版本 1.0.1 |
| **安装方式** | 已安装于 `C:\Users\乐迪\.agents\skills\obsidian-ontology-sync-1.0.1\` |
| **URL** | https://clawhub.ai/parthpandya1729/obsidian-ontology-sync |

### 3. obsidian-graph-query

| 项目 | 详情 |
|------|------|
| **名称** | obsidian-graph-query |
| **来源** | GitHub / skills.sh |
| **描述** | 让 AI agent 直接查询 Obsidian vault 的知识图谱，使用图算法（BFS、最短路径、桥接检测、度分析）回答"哪些笔记链接最多？""哪些笔记是孤岛？"等问题 |
| **星数** | skills.sh 收录（88,000+ 技能生态） |
| **最后更新** | 活跃 |
| **安装方式** | `npx skills add azuma520/obsidian-graph-query` |
| **URL** | https://github.com/azuma520/obsidian-graph-query |

### 4. ontology（openclaw 通用本体管理）

| 项目 | 详情 |
|------|------|
| **名称** | ontology |
| **来源** | ClawHub / playbooks.com |
| **描述** | 管理类型化知识图谱，支持创建、查询、链接实体和关系，用于 agent 规划。通用本体 skill，不限于 Obsidian |
| **星数** | openclaw/skills 仓库 1,086 stars |
| **最后更新** | 活跃 |
| **安装方式** | `npx playbooks add skill openclaw/skills --skill ontology` 或 `npx clawhub@latest install ontology` |
| **URL** | https://playbooks.com/skills/openclaw/skills/ontology |

### 5. knowledge-management（ClawHub PKM）

| 项目 | 详情 |
|------|------|
| **名称** | knowledge-management |
| **来源** | ClawHub / playbooks.com |
| **描述** | 将 agent 的知识条目自动分类（Research/Decision/Insight/Lesson/Pattern/Project/Reference/Tutorial），存为带时间戳的 Markdown 文件。支持 `km sync`/`km classify`/`km summarize`/`km cleanup` 命令。纯本地运行，无需 API |
| **星数** | ClawHub 生态（3,286 skills 平台） |
| **最后更新** | 活跃 |
| **安装方式** | `npx playbooks add skill openclaw/skills --skill knowledge-management` |
| **URL** | https://playbooks.com/skills/openclaw/skills/knowledge-management |

### 6. ClawVault（Agent 记忆图谱）

| 项目 | 详情 |
|------|------|
| **名称** | ClawVault |
| **来源** | ClawHub / playbooks.com |
| **描述** | Agent 结构化记忆系统：记忆图谱索引+语义搜索、上下文死亡恢复（checkpoint/recovery）、Obsidian Canvas 集成+任务追踪、会话转录修复、可选 Tailscale 跨 vault 搜索 |
| **星数** | ClawHub 生态 |
| **最后更新** | v1.5.1（2026-02-10） |
| **安装方式** | `npx clawhub@latest install clawvault` |
| **URL** | https://playbooks.com/skills/openclaw/skills/clawvault |

---

## 类别B：会话管理 / 上下文接续

### 1. session-handoff（softaworks）

| 项目 | 详情 |
|------|------|
| **名称** | session-handoff |
| **来源** | GitHub / skills.sh / Tessl / agentskills.me |
| **描述** | 解决上下文耗尽问题的核心 skill。创建全面的交接文档让新 agent 无缝继续工作。支持 CREATE（生成交接脚手架→填写状态/上下文/决策/下一步→验证检测密钥+质量评分）和 RESUME（列出交接→检测过期→加载→验证）两个流程。支持 `--continues-from` 链式交接。5+ 文件编辑或复杂调试后主动建议交接 |
| **星数** | skills.sh + 多平台收录 |
| **最后更新** | 活跃 |
| **安装方式** | `npx skills add softaworks/agent-toolkit/session-handoff` 或 `npx tessl i github:softaworks/agent-toolkit --skill session-handoff` |
| **URL** | https://github.com/softaworks/agent-toolkit (session-handoff) / https://agentskills.me/skill/session-handoff |

### 2. Agent-Skills-for-Context-Engineering（上下文工程全套）

| 项目 | 详情 |
|------|------|
| **名称** | context-compression + context-fundamentals + 更多 |
| **来源** | GitHub (muratcankoylan) |
| **描述** | **13.5k stars 的重量级仓库**。包含：**context-compression**（锚定迭代摘要/不透明压缩/再生全量摘要三种策略）、**context-fundamentals**（上下文退化模式）、多 agent 架构模式、记忆系统设计、工具设计。被北大引用为静态 skill 架构基础性工作 |
| **星数** | **13,500 stars** / 1,055 forks |
| **最后更新** | v1.1.0（2025-12-24），仓库活跃 |
| **安装方式** | `npx skills add muratcankoylan/Agent-Skills-for-Context-Engineering` |
| **URL** | https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering |

### 3. Context Compressor（SkillKit）

| 项目 | 详情 |
|------|------|
| **名称** | context-compressor |
| **来源** | SkillKit / ClawHub |
| **描述** | 自动上下文管理。检测上下文限制临近→压缩旧对话历史→无缝转移到新会话。智能摘要保留关键细节（决策、代码变更、文件状态），删除填充内容 |
| **星数** | SkillKit 平台收录 |
| **最后更新** | 活跃 |
| **安装方式** | 通过 SkillKit 安装 |
| **URL** | https://skillkit.io/skills/openclaw/context-compressor-skill |

### 4. better-memory（语义记忆）

| 项目 | 详情 |
|------|------|
| **名称** | better-memory |
| **来源** | ClawHub / playbooks.com / LobeHub |
| **描述** | 语义记忆 + 智能压缩 + 上下文管理。本地向量嵌入存储、余弦相似度语义搜索、自动去重、**优先级压缩**（接近上下文限制时压缩低优先条目）、跨会话身份持久化 |
| **星数** | openclaw/skills 仓库 1,086 stars |
| **最后更新** | 活跃 |
| **安装方式** | `npx playbooks add skill openclaw/skills --skill better-memory` 或 `npx clawhub@latest install better-memory` |
| **URL** | https://playbooks.com/skills/openclaw/skills/better-memory |

### 5. neural-memory（神经关联记忆）

| 项目 | 详情 |
|------|------|
| **名称** | neural-memory |
| **来源** | ClawHub |
| **描述** | 关联记忆+扩散激活。Hebbian 学习、记忆衰减、矛盾检测、时序推理。零 LLM 依赖的神经图架构。适合跨会话事实/决策/错误持久化和因果链追溯 |
| **星数** | 3,100 下载 / 2 stars |
| **最后更新** | 活跃 |
| **安装方式** | `clawdbot install nhadaututtheky/neural-memory` |
| **URL** | https://clawhub-skills.com/skills/neural-memory |

### 6. agent-context（项目上下文持久化）

| 项目 | 详情 |
|------|------|
| **名称** | agent-context |
| **来源** | ClawHub / playbooks.com |
| **描述** | 双文件系统持久化项目上下文：**AGENTS.md**（共享项目知识，≤120行）+ **.agents.local.md**（个人会话笔记，gitignored）。让 agent 跨会话无缝访问共享知识和个人学习记录 |
| **星数** | openclaw/skills 仓库 1,086 stars |
| **最后更新** | 活跃 |
| **安装方式** | `npx playbooks add skill openclaw/skills --skill agent-context` |
| **URL** | https://playbooks.com/skills/openclaw/skills/agent-context |

### 7. memory v1.0.2（已安装）

| 项目 | 详情 |
|------|------|
| **名称** | memory |
| **来源** | 本地已安装 |
| **描述** | 无限分类记忆，补充 agent 内置记忆，提供无限量分类存储 |
| **星数** | — |
| **最后更新** | v1.0.2 |
| **安装方式** | 已安装于 `C:\Users\乐迪\.agents\skills\memory-1.0.2\` |
| **URL** | — |

---

## 汇总与推荐优先级

| 类别 | 最推荐 | 理由 |
|------|--------|------|
| **知识库管理** | **kepano/obsidian-skills** + 已装的 **obsidian-ontology-sync** | 前者 13k stars、官方出品、覆盖 Markdown/Canvas/CLI；后者已安装且直接支持实体关系提取 |
| **知识库管理**（补充） | **obsidian-graph-query** | 图算法查询能力独特，补充本体同步的不足 |
| **会话管理** | **session-handoff** + **context-compression** | session-handoff 是标准交接方案；context-compression 来自 13.5k stars 仓库，学术级质量 |
| **会话管理**（补充） | **better-memory** | 语义搜索+优先级压缩+身份持久化，适合长期运行场景 |

已安装的 `obsidian-ontology-sync` 和 `memory` 已覆盖部分需求，建议重点评估 **session-handoff** 和 **context-compression** 填补跨窗口交接的空白。

---