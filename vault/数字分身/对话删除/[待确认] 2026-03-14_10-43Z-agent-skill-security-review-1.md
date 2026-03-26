---
type: 待确认
source: SpecStory/Cleaned
date: 2026-03-18
models: [composer-1.5]
turns: 1
title: "Agent skill security review"
original_file: "[导出] 2026-03-18-2206-2026-03-14_10-43Z-agent-skill-security-review-2.md"
status: pending
archive_title: ""
replaced_count: 0
---

# Agent skill security review
_Cleaned from SpecStory on 2026-03-18_


### 👤 用户

对以下两个Agent Skill进行安全审查（skill-vetter协议）：

## 审查对象1
**context-compression** from muratcankoylan/Agent-Skills-for-Context-Engineering
URL: https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering

## 审查对象2
**adr-skill** from skillrecordings
URL: https://github.com/skillrecordings/adr-skill

## 审查步骤（对每个对象）

### Step 1: 获取仓库信息
分别用Shell运行：
```
curl -s "https://api.github.com/repos/muratcankoylan/Agent-Skills-for-Context-Engineering" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'
```
```
curl -s "https://api.github.com/repos/skillrecordings/adr-skill" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'
```

### Step 2: 获取SKILL.md内容
用WebFetch获取：
1. https://raw.githubusercontent.com/muratcankoylan/Agent-Skills-for-Context-Engineering/main/skills/context-compression/SKILL.md
   或 https://raw.githubusercontent.com/muratcankoylan/Agent-Skills-for-Context-Engineering/main/context-compression/SKILL.md
2. https://raw.githubusercontent.com/skillrecordings/adr-skill/main/SKILL.md

### Step 3: 红旗检查
按skill-vetter清单检查每个SK

### Step 4: 输出两份审查报告
每份格式：
```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [name]
Source: GitHub
Author: [author]
───────────────────────────────────────
METRICS / RED FLAGS / PERMISSIONS / RISK LEVEL / VERDICT
═══════════════════════════════════════
```

---


### 🤖 Cursor (composer-1.5)

---

正在执行 skill-vetter 协议的完整安全审查。先读取 skill-vetter 的审查清单，再收集两项 Skill 的仓库与 SKILL.md 信息。

---

Error fetching URL, status code: 404 Not Found

---

Error fetching URL, status code: 404 Not Found

---

Cancelled

---

Cancelled

---