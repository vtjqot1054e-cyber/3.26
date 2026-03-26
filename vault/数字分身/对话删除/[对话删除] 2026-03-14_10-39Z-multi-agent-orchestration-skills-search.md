---
type: 对话删除
source: SpecStory/Cleaned
date: 2026-03-18
models: [claude-4.6-opus-high]
turns: 1
title: "Multi-agent orchestration skills search"
original_file: "[导出] 2026-03-18-2206-2026-03-14_10-39Z-multi-agent-orchestration-skills-search.md"
status: deleted
archive_title: ""
replaced_count: 0
---

# Multi-agent orchestration skills search
_Cleaned from SpecStory on 2026-03-18_


### 👤 用户

你是SK搜索助手。请在以下平台搜索"多Agent编排"类技能：

## 搜索目标
找到支持"多窗口/多Agent协作、任务分发、消息传递"的agent skills。

## 搜索方法

### 1. WebSearch搜索ClawHub
用WebSearch搜索以下关键词（分别搜索）：
- "clawhub multi-agent orchestration skill"
- "clawhub agent coordination task dispatch"
- "openclaw multi agent workflow"

### 2. WebSearch搜索skills.sh
- "skills.sh multi-agent orchestration"
- "skills.sh agent coordination"

### 3. WebSearch搜索GitHub
- "github SKILL.md multi-agent orchestration"
- "github agent-skills task dispatch coordination"
- "github SKILL.md agent workflow automation"

### 4. 通用搜索
- "AI agent multi-agent orchestration tool 2026"
- "cursor agent skills multi window coordination"

## 输出要求
对每个找到的候选SK，列出：
- 名称
- 来源（ClawHub/skills.sh/GitHub）
- 描述
- 星数/下载量（如有）
- 最后更新时间（如有）
- 安装方式
- GitHub URL或安装命令

尽量找3个以上候选。如果某个平台没找到，说明。

---


### 🤖 Cursor (claude-4.6-opus-high)

我来按你的要求在各个平台搜索"多Agent编排"类技能。先批量发起搜索。

---

找到不少结果了。继续搜索其余关键词。

---

再搜最后两个通用关键词。

---

现在让我获取几个关键页面的详细信息。

---

最后再查一下 ClawHub 的 agent-orchestration 和 clawctl 详细信息。

---

Fetch timed out while retrieving content

---

信息充足了。下面是完整的搜索结果报告。

---

## 搜索结果：多Agent编排类技能

共找到 **6个高度相关候选SK**，覆盖 ClawHub、skills.sh、GitHub 三大平台。

---

### 候选1: `agent-orchestration` (ClawHub)

| 项目 | 详情 |
|------|------|
| **名称** | agent-orchestration v2.0.0 |
| **来源** | ClawHub (OpenClaw官方注册表) |
| **描述** | 教Agent如何spawn、路由、管理子Agent。包含prompt模板、生命周期控制、实时追踪、结果聚合+重试、自动学习循环 |
| **适用场景** | 多步骤pipeline协调、专业任务分发（研究/摘要/数据提取）、客服升级、分布式实验编排 |
| **星数/下载量** | LobeHub上架（OpenClaw官方出品） |
| **最后更新** | 活跃维护中 |
| **安装命令** | `clawhub install openclaw-skills-agent-orchestration` |
| **URL** | https://clawhub.ai/halthelobster/agent-orchestration |

**亮点**：OpenClaw原生，提供`sessions_list`/`sessions_history`/`sessions_send`/`sessions_spawn`四大Agent间通信工具，支持真正的Agent-to-Agent消息传递。

---

### 候选2: `clawctl` (ClawHub)

| 项目 | 详情 |
|------|------|
| **名称** | clawctl |
| **来源** | ClawHub (OpenClaw) |
| **描述** | Agent舰队协调层：任务编排、Agent间消息路由、活动Feed、集中Dashboard、角色访问控制 |
| **适用场景** | 多Agent任务调度、消息路由、历史审计 |
| **安装方式** | 通过ClawHub安装 |
| **URL** | https://lobehub.com/en/skills/openclaw-skills-clawctl |

**亮点**：偏"管控台"定位，支持任务创建调度+消息路由+RBAC权限+审计日志，适合需要集中管理多个Agent的场景。

---

### 候选3: `multi-agent-orchestration` (skills.sh)

| 项目 | 详情 |
|------|------|
| **名称** | multi-agent-orchestration |
| **来源** | skills.sh (qodex-ai/ai-agent-skills) |
| **描述** | 框架无关的多Agent编排技能，覆盖5种编排模式（顺序/并行/层级/共识/工具中介），附带CrewAI、AutoGen、LangGraph、Swarm框架模板 |
| **周安装量** | **548次**（最高） |
| **GitHub星数** | 3 |
| **首次上架** | 2026-01-22 |
| **已安装平台** | Cursor 423, Codex 478, GitHub Copilot 449 等 |
| **安全审计** | Socket Pass, Snyk Pass |
| **安装命令** | `npx skills add https://github.com/qodex-ai/ai-agent-skills --skill multi-agent-orchestration` |
| **GitHub URL** | https://github.com/qodex-ai/ai-agent-skills |

**亮点**：**安装量最大**，内容最全面——包含完整的编排模式文档、代码示例、通信协议（直接/共享内存/管理器）、评估指标、最佳实践。是纯知识型SK，教Agent如何设计和运行多Agent系统。

---

### 候选4: `subagent-coordination` (skills.sh)

| 项目 | 详情 |
|------|------|
| **名称** | subagent-coordination |
| **来源** | skills.sh (outfitter-dev/agents) |
| **描述** | 面向Cursor/Claude的子Agent协调技能。按角色路由（coding/reviewing/research/debugging/testing/challenging/specialist/patterns），支持顺序交接、并行执行、挑战循环、调查链等工作流模式 |
| **周安装量** | 6 |
| **GitHub星数** | **24**（星数最高） |
| **首次上架** | 2026-01-22 |
| **安装命令** | `npx skills add https://github.com/outfitter-dev/agents --skill subagent-coordination` |
| **GitHub URL** | https://github.com/outfitter-dev/agents |

**亮点**：**与Cursor原生subagent机制最匹配**。定义了8种角色（senior-dev/ranger/analyst/debugger/tester/skeptic/specialist/pattern-analyzer），支持`run_in_background`并行、resume恢复长会话、model选择。有明确的反模式警告和升级机制。

---

### 候选5: `ai-agent-orchestrator` (skills.sh)

| 项目 | 详情 |
|------|------|
| **名称** | ai-agent-orchestrator |
| **来源** | skills.sh (patricio0312rev/skills) |
| **描述** | TypeScript实现的多Agent系统构建SK，包含Agent基类、专业Agent定义（Researcher/Writer/Reviewer/Planner）、三种编排器（Sequential/Supervisor/Parallel）、共享内存（Redis）、事件总线通信 |
| **周安装量** | 48 |
| **GitHub星数** | 16 |
| **首次上架** | 2026-01-24 |
| **安全审计** | Agent Trust Hub Pass, Socket Pass, Snyk Warn |
| **安装命令** | `npx skills add https://github.com/patricio0312rev/skills --skill ai-agent-orchestrator` |
| **GitHub URL** | https://github.com/patricio0312rev/skills |

**亮点**：最接近**可运行代码**的SK，提供了完整的TypeScript实现（Agent基类、Orchestrator、SharedMemory、EventBus、Workflow定义），适合想直接搭建多Agent系统的场景。

---

### 候选6: `orchestrating-swarms` (GitHub Gist)

| 项目 | 详情 |
|------|------|
| **名称** | orchestrating-swarms |
| **来源** | GitHub Gist (kieranklaassen) |
| **描述** | Claude Code Swarm编排技能——基于TeammateTool和Task系统的多Agent协调完整指南。定义了Team/Teammate/Leader/Task/Inbox/Message六大原语 |
| **Fork数** | **87**（社区关注度极高） |
| **创建时间** | 2026-01-25 |
| **最后更新** | 2026-03-13（2天前刚更新） |
| **URL** | https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea |

**亮点**：专为Claude Code的原生多Agent机制设计，支持tmux/iTerm2/进程内三种spawn后端，有完整的Mermaid流程图和生命周期管理。87个Fork说明社区采纳度高。但注意——这是Claude Code特有机制，Cursor环境下需适配。

---

## 平台搜索结果汇总

| 平台 | 找到候选 | 说明 |
|------|---------|------|
| **ClawHub** | 2个 | agent-orchestration + clawctl，OpenClaw原生生态 |
| **skills.sh** | 3个 | multi-agent-orchestration（最热门）+ subagent-coordination（最适配Cursor）+ ai-agent-orchestrator（代码最完整） |
| **GitHub** | 1个 | orchestrating-swarms（Fork最多，Claude Code原生） |

## 推荐优先级（针对你的Cursor多窗口场景）

1. **subagent-coordination** — 与Cursor subagent机制直接对接，角色路由清晰
2. **multi-agent-orchestration** — 编排模式知识最全面，安装量最大
3. **orchestrating-swarms** — 设计理念最完整（Team/Task/Inbox体系），但需从Claude Code适配到Cursor

需要我深入分析某个SK，或者直接安装测试吗？

---