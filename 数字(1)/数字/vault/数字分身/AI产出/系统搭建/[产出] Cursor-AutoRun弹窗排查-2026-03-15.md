# Cursor Auto-Run 弹窗排查报告

> 产出日期：2026-03-15 | 问题：设 Ask Every Time 后文件修改仍不弹确认窗

## 官方定义（cursor.com/docs 终端文档）

**路径**：Settings → Cursor Settings (`Ctrl+Shift+J`) → **Agents** → **Auto-Run**

| 模式 | 行为 |
|------|------|
| **Run in Sandbox** | 工具和命令在沙盒内自动执行（默认） |
| **Ask Every Time** | **所有工具和命令**（含文件写入、命令、MCP）需用户批准后才执行 |
| Run Everything | 全部自动执行，跳过确认 |

即：Ask Every Time 理论上应对 **Write/StrReplace 等文件写入** 也生效。

## 已排除项

- `.cursor/sandbox.json`：只管网络/路径权限，与 Auto-Run 无关
- 工作区规则 / Skills：无相关配置

## 可能原因（按优先级）

### 1. 设置路径或标签不一致

- 文档：**Agents** → Auto-Run
- 常见误点：Features → Chat（含 Agent 相关，但可能不是同一入口）
- **建议**：`Ctrl+Shift+J` 打开后，左侧逐项点「Agents」「Features」「Chat」，确认 Auto-Run Mode 所在位置及当前值

### 2. 会话在改设置前就已创建

- 部分版本可能只对新会话应用新设置
- **操作**：关掉当前 Agent 对话 → 开新对话 → 再让 Agent 做一次文件修改测试

### 3. 工作区/会话被记成「已授权」

- 若之前选过“始终信任此工作区”或类似选项，可能跳过确认
- **操作**：重启 Cursor，换一个空项目或新文件夹开 Agent 测试

### 4. Cursor 版本差异

- 论坛有反馈：0.49.5 时 Auto-Run 与 Command allowlist 行为不符合预期
- **操作**：检查 `Help → About` 中的版本，必要时更新到最新

### 5. 文件写入与命令的差异化处理（待验证）

- Agent Security 文档：常规工作区文件写入默认「直接保存」，只有配置类文件需 approval
- Terminal 文档：Auto-Run 含「file writes」
- **矛盾点**：两处描述不完全一致，需实测或向 Cursor 确认

## 建议测试流程

1. `Ctrl+Shift+J` → 左侧点 **Agents** → 确认 Auto-Run Mode = **Ask Every Time**
2. 关闭当前 Agent 对话
3. 新建 Agent 对话，输入：「在项目根目录创建一个空文件 `_test_confirm.txt`」
4. 观察是否有确认弹窗
5. 若仍无弹窗：新开一个空文件夹作为工作区，重复 2–4

## 反馈建议

若按上述流程仍无法弹窗，可向 Cursor 反馈：

- 现象：Ask Every Time 下，StrReplace/Write 类文件修改不弹确认
- 环境：Cursor 版本、操作系统、是否使用 WSL
- 复现：设置路径、是否新建会话、是否新建工作区

Forum: https://forum.cursor.com  
或：Help → Report Issue

## 关联文件

- 待执行指令：`数字分身/数字分身/待执行指令/[指令] 杂务-关闭AutoRun.md`
- Cursor 文档：https://cursor.com/docs/agent/tools/terminal.md（Editor configuration 段）
