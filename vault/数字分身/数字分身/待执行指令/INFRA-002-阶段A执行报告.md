# INFRA-002 阶段A 执行报告

**执行时间**：2026-03-27  
**执行者**：工程窗口（Cursor Agent）  
**回报对象**：数字真我  
**状态**：阶段A已完成（阶段B：实现方案待设计）

---

## 一、A1 · Cursor MCP 正确配置方式（官方依据）

**依据**：[Cursor MCP 主文档](https://cursor.com/docs/mcp.md)（与 `https://docs.cursor.com/context/model-context-protocol` 同体系）。

| 要点 | 结论 |
|------|------|
| 项目级配置位置 | **是**：在项目根目录使用 `.cursor/mcp.json`（与全局 `~/.cursor/mcp.json` 并存；优先级为项目 → 全局） |
| 格式 | 顶层 `mcpServers`，每项为 `command`+`args` 的 STDIO 服务，或 `url` 的远程服务 |
| STDIO 必填字段 | 文档表格标明 **`type` 为 Required**，取值 `"stdio"` |
| 是否在设置里启用 | **需要**：Settings → Features → **Model Context Protocol** 中可对各 Server **开关**；未启用则不会加载 |
| 修改后 | 通常需 **重启 Cursor** 或重新加载 MCP |

**本仓库已做修正**：`E:/数字/.cursor/mcp.json` 中 `chroma` 条目已补充 **`"type": "stdio"`**（此前缺失，可能导致 Cursor 未按 STDIO 正确连接）。

---

## 二、A2 · chroma MCP 能否被 Cursor 调用（根因与验证）

### 2.1 环境侧（工程已验证）

- `uvx`、`chroma-mcp` 可正常执行（`uvx chroma-mcp --help` 正常）。
- 与 INFRA-001 一致：持久化目录 `E:/数字/knowledge_base_v2/vector_store` 已用于配置。

### 2.2「Cursor 不调 chroma」的可能根因（供数字真我归档）

1. **配置不完整**：缺少 `"type": "stdio"`（已修复，需用户侧重启 Cursor 后再验）。
2. **MCP 未在 UI 中启用**：Features → MCP 中 `chroma` 被关闭。
3. **模型路由行为**：官方写明 Agent「在相关时」自动使用 MCP；若任务可被 **Grep/Read** 完成，模型可能**不选**向量检索——**不等于 MCP 坏了**。
4. **工具审批**：默认需用户批准 MCP 调用；未开 Auto-run 时可能表现为「未调用」。
5. **排障**：Output 面板选择 **MCP Logs** 查看连接/崩溃日志。

### 2.3 仍须用户在新对话中完成的验收（A2 闭环）

1. 重启 Cursor（加载新 `mcp.json`）。
2. 新 Agent 对话中**明确**要求：「请使用 MCP 工具 `chroma_list_collections`（或 chroma 提供的列表接口）」。
3. 观察是否出现工具调用及 MCP Logs 无报错。

**说明**：当前工程窗口无法在无人操作下代替用户点击「批准」或确认 UI 状态，故 A2 的最终签字仍以用户一次对话验证为准。

---

## 三、A3 · MCP 是否具备「启动新 Agent 会话」能力

### 3.1 结论（可行性）

| 能力 | 结论 |
|------|------|
| **标准 MCP 协议** | **不提供**「由工具回调宿主新开一条 Cursor Agent 会话」的通用能力。 |
| **Cursor 文档** | MCP 用于 **Tools / Prompts / Resources** 等；CLI 侧为 `agent mcp list` 等管理命令，**未描述**「MCP 工具 = 新开 IDE Agent 窗口」。 |
| **关窗自动复盘架构** | **不能**指望「写一个 chroma 类 MCP 就自动弹新窗口跑数字真我」。 |

### 3.2 替代方案（阶段B设计输入）

1. **Cursor CLI `agent`**：脚本或外部调度调用 `agent -p "..."`，由本机流程触发「新的一次 agent 运行」（是否等价于 IDE 里新 Composer/Agent 标签，以 Cursor 当前版本文档为准）。
2. **手动/半自动**：关窗指令 → 落盘对话摘要路径 → 用户快捷键新开窗口 + 粘贴路径（规则/SK 约束打开数字真我）。
3. **VS Code/Cursor 扩展**：若存在「打开新 Chat 并注入提示」的 API，可归入扩展或内部脚本（需专项调研与权限）。
4. **完全外部编排**：n8n/计划任务监听文件，调用 CLI 或通知用户执行固定步骤。

**建议**：阶段B将「导出当前对话 → 新上下文消费」拆成 **可落盘产物** + **可重复触发命令**，不依赖 MCP 启动会话。

---

## 四、验收对照（阶段A）

| 检查项 | 阶段A结论 |
|--------|-----------|
| Cursor MCP 配置方式与根因说明 | ✅ 已文档化；并已补 `type: stdio` |
| chroma 能否被调用 | ⚠️ 配置已修正；**须在用户新对话中**按 A2.3 最终确认 |
| MCP 能否启动新会话 | ✅ **明确不可行**（标准能力）；替代方案已列 |

---

## 五、需数字真我决策 / 转述事项

1. 是否在 SK 或交接备忘中写明：**复盘任务应显式要求使用 chroma**，避免模型只用 Grep。
2. 阶段B是否优先 **CLI/脚本 + 落盘**，而非 MCP 扩展职责。

---

## 六、相关文件

- 指令：`vault/数字分身/数字分身/待执行指令/INFRA-002-MCP关窗自动复盘.md`
- MCP 配置：`E:/数字/.cursor/mcp.json`（已更新）
- 前置：`vault/数字分身/数字分身/待执行指令/INFRA-001-阶段B执行报告.md`
