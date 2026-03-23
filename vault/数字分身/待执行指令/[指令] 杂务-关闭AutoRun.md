---
type: 待执行指令
from: 大脑-04
to: 杂务
model: Auto
created: 2026-03-15 14:20
status: pending
---

# 指令：关闭 Cursor Auto-run 模式并验证

> 发出方：大脑-04 | 接收方：杂务窗口

## 任务

帮用户关闭 Cursor 的 Auto-run 模式，然后做一次文件修改测试，确认 IDE 会弹出 diff 让用户确认。

## 步骤

### 第1步：引导用户关闭 Auto-run

告诉用户操作：
1. 聊天窗口底部找到小盾牌/闪电图标 → 关掉 Auto-run
2. 或者：`Ctrl + Shift + J` → 左侧 **Agents** → Auto-Run → 选 **Ask Every Time**

### 第2步：测试文件修改弹 diff

用 StrReplace 修改这个文件，在末尾加一行测试文字：
- 文件：`.cursor/skills/工程-操作纪律/SKILL.md`
- 在"测试段落"下方加一行："Auto-run 关闭测试成功"

如果 IDE 弹出了 diff 让用户确认 → 测试成功
如果没弹出 → 告诉用户，汇报给大脑

### 第3步：清理测试内容

测试成功后，删除"测试段落"和"Auto-run 关闭测试成功"这两行。

## 约束

- 只做上面写的事，不多做
- 搞不定就汇报"无法完成，原因是XX"
