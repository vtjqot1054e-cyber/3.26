---
type: 待确认
source: SpecStory/Cleaned
date: 2026-03-18
models: [composer-1.5]
turns: 1
title: "Agent skill security review"
original_file: "[导出] 2026-03-18-2206-2026-03-14_10-43Z-agent-skill-security-review-1.md"
status: pending
archive_title: ""
replaced_count: 0
---

# Agent skill security review
_Cleaned from SpecStory on 2026-03-18_


### 👤 用户

对以下Agent Skill进行安全审查（skill-vetter协议）：

## 审查对象
**session-handoff** from softaworks/agent-toolkit
URL: https://github.com/softaworks/agent-toolkit

## 审查步骤

### Step 1: 获取仓库信息
用Shell运行：
```
curl -s "https://api.github.com/repos/softaworks/agent-toolkit" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at, license: .license.spdx_id}'
```

### Step 2: 获取SKILL.md内容
用WebFetch获取：https://raw.githubusercontent.com/softaworks/agent-toolkit/main/session-handoff/SKILL.md
如果404，尝试其他路径：
- https://raw.githubusercontent.com/softaworks/agent-toolkit/main/skills/session-handoff/SKILL.md
- https://raw.githubusercontent.com/softaworks/agent-toolkit/master/session-handoff/SKILL.md

### Step 3: 检查红旗
读取SKILL.md内容后检查：
- 是否有curl/wget到未知URL
- 是否发送数据到外部服务器
- 是否请求凭证/token
- 是否使用eval()/exec()
- 权限范围是否最小化
- 是否只操作本地文件

### Step 4: 输出审查报告
格式同skill-vetter标准：
```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: session-handoff
Source: GitHub (softaworks/agent-toolkit)
Author: softaworks
───────────────────────────────────────
METRICS / RED FLAGS / PERMISSIONS / RISK LEVEL / VERDICT
═══════════════════════════════════════
```

---


### 🤖 Cursor (composer-1.5)

---

Error fetching URL, status code: 404 Not Found

---

改用 PowerShell 获取仓库信息并尝试其他路径获取 SKILL.md：

---

获取 SKILL 引用的 Python 脚本以进行完整代码审查：

---

正在获取 skill 下的 scripts 与 references 的完整内容：

---

Cancelled

---