---
type: 待确认
source: SpecStory/Cleaned
date: 2026-03-18
models: [composer-1.5]
turns: 1
title: "Agent skill security review"
original_file: "[导出] 2026-03-18-2206-2026-03-14_10-43Z-agent-skill-security-review.md"
status: pending
archive_title: ""
replaced_count: 0
---

# Agent skill security review
_Cleaned from SpecStory on 2026-03-18_


### 👤 用户

对以下Agent Skill进行安全审查（skill-vetter协议）：

## 审查对象
**subagent-coordination** from outfitter-dev/agents (GitHub/skills.sh)
URL: https://github.com/outfitter-dev/agents

## 审查步骤

### Step 1: 获取仓库信息
用Shell运行：
```
curl -s "https://api.github.com/repos/outfitter-dev/agents" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at, license: .license.spdx_id, open_issues: .open_issues_count}'
```

### Step 2: 获取SKILL.md内容
用WebFetch获取：https://raw.githubusercontent.com/outfitter-dev/agents/main/skills/subagent-coordination/SKILL.md
如果404，试试：https://raw.githubusercontent.com/outfitter-dev/agents/main/subagent-coordination/SKILL.md

### Step 3: 检查红旗
读取SKILL.md内容后，按以下清单检查：
- 是否有curl/wget到未知URL
- 是否发送数据到外部服务器
- 是否请求凭证/token/API key
- 是否读取~/.ssh、~/.aws、~/.config
- 是否使用base64 decode
- 是否使用eval()/exec()
- 是否修改系统文件
- 是否安装未列出的包
- 是否有混淆代码
- 权限范围是否最小化

### Step 4: 输出审查报告
格式：
```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: subagent-coordination
Source: GitHub (outfitter-dev/agents)
Author: outfitter-dev
───────────────────────────────────────
METRICS:
• Stars: [count]
• Last Updated: [date]
• Files Reviewed: [count]
───────────────────────────────────────
RED FLAGS: [None / List them]

PERMISSIONS NEEDED:
• Files: [list or "None"]
• Network: [list or "None"]
• Commands: [list or "None"]
───────────────────────────────────────
RISK LEVEL: [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME]
VERDICT: [✅ SAFE TO INSTALL / ⚠️ INSTALL WITH CAUTION / ❌ DO NOT INSTALL]
NOTES: [observations]
═══════════════════════════════════════
```

---


### 🤖 Cursor (composer-1.5)

---

Error fetching URL, status code: 404 Not Found

---

改用 PowerShell 解析 JSON，并尝试备选 SKILL.md 路径：

---

Error fetching URL, status code: 404 Not Found

---

查看 `.agents` 目录结构以定位 subagent-coordination：

---

正在从 GitHub 获取源文件以比对：

---

检查 `subagents` 目录下的相关文件是否有可执行内容：

---

Cancelled

---

Cancelled

---