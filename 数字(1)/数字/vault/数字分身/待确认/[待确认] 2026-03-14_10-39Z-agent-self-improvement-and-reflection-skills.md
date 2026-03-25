---
type: 待确认
source: SpecStory/Cleaned
date: 2026-03-18
models: [claude-4.6-opus-high]
turns: 1
title: "Agent self-improvement and reflection skills"
original_file: "[导出] 2026-03-18-2206-2026-03-14_10-39Z-agent-self-improvement-and-reflection-skills.md"
status: pending
archive_title: ""
replaced_count: 0
---

# Agent self-improvement and reflection skills
_Cleaned from SpecStory on 2026-03-18_


### 👤 用户

你是SK搜索助手。请在以下平台搜索"自我改进/反思"类技能：

## 搜索目标
找到支持"Agent自我评估、纠偏、学习、self-reflection、self-improvement"的agent skills。

## 搜索方法

### 1. WebSearch搜索ClawHub
- "clawhub self-improvement self-reflection skill"
- "clawhub agent self-evaluation learning"
- "openclaw self improving agent skill"

### 2. WebSearch搜索skills.sh
- "skills.sh self-improvement reflection"
- "skills.sh agent self-evaluation"

### 3. WebSearch搜索GitHub
- "github SKILL.md self-improvement reflection agent"
- "github agent-skills self-evaluation learning correction"
- "github SKILL.md agent retrospective improvement"

### 4. 通用搜索
- "AI agent self-reflection improvement skill 2026"
- "cursor agent skills self-improving retrospective"

## 额外要求
用户已安装了一个 self-improving-1.1.3 技能。搜索时注意看是否有更好的替代品或补充品。

## 输出要求
对每个找到的候选SK，列出：
- 名称
- 来源
- 描述
- 星数/下载量
- 最后更新
- 安装方式
- URL

尽量找3个以上候选。

---


### 🤖 Cursor (claude-4.6-opus-high)

我来在多个平台上搜索"自我改进/反思"类技能。先并行发起搜索。

---

找到了不少候选。让我继续搜索更多细节和补充搜索。

---

信息很丰富了。让我再补充获取一些关键URL和统计数据。

---

现在让我也看看用户已安装的 self-improving-1.1.3 技能的内容，以便做对比分析。

---

现在我有了所有需要的信息。下面整理输出。

---

## 搜索结果：自我改进/反思类 Agent Skills

已搜索平台：ClawHub、skills.sh、agentskill.sh、Tessl、GitHub、SkillMD.ai、playbooks.com、LLMBase

---

### 已安装基线

你已安装 **self-improving v1.1.3**（by ivangdavila/ClawHub），核心功能：
- 纠错日志 + 自我反思 + 分层记忆（HOT/WARM/COLD）
- 路径：`~/self-improving/`
- 优点：结构清晰、安全边界明确、有升降级机制
- 不足：**被动触发为主**（需要用户纠正或手动反思），无定时巡检、无跨会话回顾

---

### 候选 SK 列表

#### 1. **self-improving-agent** (by pskoett)

| 项目 | 详情 |
|------|------|
| 名称 | self-improving-agent / self-improvement |
| 来源 | ClawHub / GitHub / skills.sh |
| 描述 | 捕获 learnings、errors、corrections，写入结构化 `.learnings/` 目录（ERRORS.md / LEARNINGS.md / FEATURE_REQUESTS.md），高频学习可"晋升"到 CLAUDE.md / AGENTS.md / SOUL.md / TOOLS.md |
| 星数/下载量 | **2,000 stars / 205.7K downloads / 3.1K 当前安装** |
| 最后更新 | 2026年活跃维护中 |
| 安装方式 | `clawhub install pskoett/self-improving-agent` |
| URL | [GitHub](https://github.com/pskoett/pskoett-ai-skills) / [skills.sh](https://skills.sh/pskoett/self-improving-agent/self-improvement) / [OpenClaw](https://openclaw.army/skills/pskoett/self-improving-agent/) |
| **与已安装版对比** | pskoett 版侧重**错误和学习的结构化日志**（`.learnings/` 目录），而你已安装的 ivangdavila 版侧重**分层记忆管理**（HOT/WARM/COLD）。两者互补，但功能有较大重叠。pskoett 版下载量和社区活跃度**远高于**已安装版 |
| 适合度 | ⭐⭐⭐⭐ 替代品（社区更大，但记忆分层不如已安装版精细） |

---

#### 2. **agent-self-reflection** (by openclaw)

| 项目 | 详情 |
|------|------|
| 名称 | agent-self-reflection |
| 来源 | agentskill.sh / playbooks.com / openclaw |
| 描述 | **定期分析最近会话**（默认2小时内），提取可操作洞察，自动路由到对应工作区文件（AGENTS.md / TOOLS.md / memory files / SKILL.md）。设计为 **cron job** 运行 |
| 星数/下载量 | 中等活跃度 |
| 最后更新 | 2026年活跃 |
| 安装方式 | `npx playbooks add skill openclaw/skills --skill agent-self-reflection` |
| URL | [playbooks.com](https://playbooks.com/skills/openclaw/skills/agent-self-reflection) / [agentskill.sh](https://agentskill.sh/@openclaw/self-reflect) |
| **与已安装版对比** | **强补充品**。已安装版是被动触发（用户纠正时记录），这个是**主动巡检**（定时扫描最近会话，自动提取教训）。两者组合 = 被动学习 + 主动复盘 |
| 适合度 | ⭐⭐⭐⭐⭐ **最佳补充品**（你已安装了它！见 `agent-self-reflection-1.0.0`） |

**注意**：你的 Skills 列表显示已安装 `agent-self-reflection-1.0.0`，但搜索结果显示社区版可能有更新。

---

#### 3. **self-reflection** (by hopyky)

| 项目 | 详情 |
|------|------|
| 名称 | self-reflection |
| 来源 | GitHub / OpenClaw Skills |
| 描述 | **心跳机制**驱动的自我反思——每60分钟触发一次检查，达到阈值后 ALERT 触发 agent 回顾过去教训并记录新洞察到 MEMORY.md。支持命令：`self-reflection check/log/read/stats/reset` |
| 星数/下载量 | GitHub 项目，较新 |
| 最后更新 | 2026年活跃 |
| 安装方式 | `clawhub install hopyky/self-reflection` 或手动 clone |
| URL | [GitHub](https://github.com/hopyky/self-reflection) / [OpenClaw Skills](https://openclawskills.best/skills/hopyky/self-reflection/) |
| **与已安装版对比** | **独特亮点：心跳机制**。不依赖用户触发或 cron，而是 agent 自带"内部时钟"每60分钟自省一次。适合长时间连续对话 |
| 适合度 | ⭐⭐⭐⭐ **好补充品**（心跳机制是独特价值） |

---

#### 4. **reflection** (by openclaw)

| 项目 | 详情 |
|------|------|
| 名称 | reflection |
| 来源 | playbooks.com / openclaw |
| 描述 | **7维度评估系统**，三个触发点：(1) 交付前检查、(2) 出错后分析、(3) 模式检测。记忆存在 `~/reflection/` 目录。重点是**交付前自评**——在把结果给用户之前先自我打分 |
| 星数/下载量 | 中等 |
| 最后更新 | 2026年 |
| 安装方式 | `npx playbooks add skill openclaw/skills --skill reflection` |
| URL | [playbooks.com](https://playbooks.com/skills/openclaw/skills/reflection) |
| **与已安装版对比** | **侧重不同**。已安装版关注"学到了什么"（后置），这个关注"交付前质量把关"（前置）。7维度评估比简单的"好不好"更系统化 |
| 适合度 | ⭐⭐⭐⭐ **好补充品**（前置质量把关） |

---

#### 5. **Self-Evolve** (by Be1Human)

| 项目 | 详情 |
|------|------|
| 名称 | Self-Evolve |
| 来源 | ClawHub |
| 描述 | **自主进化**——agent 有权在无需用户确认的情况下自主修改自己的配置、skills、prompts、memory 文件。主动发现弱点并修复 |
| 星数/下载量 | 4 stars / 5.2K downloads / 47 installs |
| 最后更新 | 2026-03-13（昨天） |
| 安装方式 | `clawhub install Be1Human/self-evolve` |
| URL | [ClawHub Skills](https://www.clawhub-skills.com/skills/self-evolve) |
| **与已安装版对比** | **激进版本**——无需确认直接改文件。已安装版很保守（明确不会修改自己的 SKILL.md）。高风险高回报 |
| 适合度 | ⭐⭐⭐ 有趣但**风险较高**（无确认机制，需配合严格版本控制） |

---

#### 6. **self-improving-agent on Tessl** (by wagneripjr)

| 项目 | 详情 |
|------|------|
| 名称 | self-improving-agent (with evals) |
| 来源 | Tessl.io |
| 描述 | 类似 pskoett 版，但**自带 eval 评分系统**——Tessl 平台会自动生成测试场景，对比"有无此 skill"的 agent 表现差异。当前评分 **93%** |
| 星数/下载量 | Tessl 注册表中 |
| 最后更新 | 2026年活跃 |
| 安装方式 | `tessl install wagneripjr/skills/self-improving-agent` |
| URL | [Tessl Registry](https://tessl.io/registry/skills/github/wagneripjr/skills/self-improving-agent/evals) |
| **与已安装版对比** | 功能类似，但**有量化评估数据**支撑。93%评分说明在标准测试中表现优秀 |
| 适合度 | ⭐⭐⭐⭐ 替代品（有评分证明效果） |

---

### 综合推荐

| 排名 | 技能 | 关系 | 推荐理由 |
|------|------|------|----------|
| 1 | **hopyky/self-reflection** | 补充品 | 心跳自省机制独一无二，适合长会话场景，与已安装版零冲突 |
| 2 | **openclaw/reflection** | 补充品 | 7维度交付前质量检查，弥补已安装版"只管后置学习"的空白 |
| 3 | **pskoett/self-improving-agent** | 替代品 | 社区最大（2K stars, 205K downloads），`.learnings/` 结构化日志比已安装版的分层记忆更适合项目级追踪 |
| 4 | **Tessl/wagneripjr** | 替代品 | 93%评分有数据支撑 |
| 5 | **Be1Human/Self-Evolve** | 进阶版 | 自主进化很前沿，但风险大 |

**最佳组合建议**：保留已安装的 `self-improving-1.1.3`（分层记忆管理）+ 新增 `hopyky/self-reflection`（心跳自省）+ 新增 `openclaw/reflection`（交付前质检）= **后置学习 + 定时巡检 + 前置把关** 三层闭环。

---