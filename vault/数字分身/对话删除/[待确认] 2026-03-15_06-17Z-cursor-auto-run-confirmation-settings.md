---
type: 待确认
source: SpecStory/Cleaned
date: 2026-03-18
models: [composer-1.5]
turns: 2
title: "Cursor auto-run confirmation settings"
original_file: "[导出] 2026-03-18-2206-2026-03-15_06-17Z-cursor-auto-run-confirmation-settings.md"
status: pending
archive_title: ""
replaced_count: 0
---

# Cursor auto-run confirmation settings
_Cleaned from SpecStory on 2026-03-18_


### 👤 用户

在 Cursor 里让「每次执行都弹窗」：

Ctrl + Shift + J 打开 Cursor Settings
左侧点 Agents
在 Auto-Run 里把 Auto-Run Mode 选成 Ask Every Time
这样工具执行（改文件、跑命令等）都会先弹确认，不会自动跑。

如果改完仍不弹窗：关掉当前 Agent 对话、新开一个再试，或重启 Cursor。仍不行就可能是当前会话/工作区被记成「已授权」，需反馈给 Cursor 或大脑排查。我要测试自动弹窗确认修改内容的功能

---


### 🤖 Cursor (composer-1.5)

进行小修改以触发弹窗。若已把 Auto-Run Mode 设为 Ask Every Time，执行写入操作时应先出现确认弹窗。正在创建测试文件：

---

已经写入测试文件 `_test_agent_confirm.md`。

**接下来请你确认：**

1. **如果出现了确认弹窗**：说明 Ask Every Time 已生效，功能正常。
2. **如果没有出现弹窗**：可能原因：
   - 设置未正确应用：用 Ctrl + Shift + J 再检查一次 Auto-Run Mode 是否为 Ask Every Time
   - 当前 Agent 会话在改设置前就存在：关掉本对话，开一个新 Agent 再试
   - 工作区/会话被记成「已授权」：尝试重启 Cursor
   - Cursor 版本或行为限制：需要向 Cursor 反馈或由大脑排查

---

**建议操作流程**：
1. 先确认设置：Ctrl + Shift + J → Agents → Auto-Run Mode = **Ask Every Time**
2. 关掉本 Agent 对话，开一个新的
3. 在新对话里说：「随便改一个文件，测试弹窗」
4. 若仍不弹窗，可在 `数字分身/数字分身/待执行指令/` 里加一条指令，让大脑后续排查

测试结束后，直接删除 `_test_agent_confirm.md` 即可。

---


### 👤 用户

没实现在排查

---


### 🤖 Cursor (composer-1.5)

排查中：查看工作区配置并搜索 Cursor 的 Auto-Run/Ask Every Time 相关文档与已知问题。

---