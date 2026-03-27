# INFRA-002 · MCP关窗自动复盘

**创建时间**：2026-03-27
**创建者**：数字真我-V18
**执行者**：工程窗口（Cursor Agent）
**状态**：阶段A已完成（见 `INFRA-002-阶段A执行报告.md`）；阶段B未启动

---

## 任务目标

实现"用户说关窗 → 自动MCP启动新数字真我窗口 → 执行流程一+流程二"。

**业务价值**：
- 同上下文复盘会被污染（V17已确认）
- 用户不应该手动开窗口、复制对话
- 复盘应该自动化、无缝衔接

---

## 当前问题

1. **Cursor不调用chroma MCP**：V18验证，Cursor用的是Grep+Read，不调`.cursor/mcp.json`里配置的chroma
2. **MCP启动新窗口能力未知**：需调研Cursor MCP是否支持"启动新Agent会话"

---

## 调研任务（阶段A）

### A1. 确认Cursor MCP的正确配置方式

1. 查Cursor官方文档，确认：
   - `.cursor/mcp.json` 是否是正确位置？
   - MCP Server需要什么格式？
   - 是否需要在Cursor设置里手动启用？
2. 参考链接：
   - https://docs.cursor.com/context/model-context-protocol
   - https://cursormcp.dev/

### A2. 测试chroma MCP能否被Cursor调用

1. 修正配置后，重启Cursor
2. 新对话中问："调用chroma工具列出所有collections"
3. 观察AI是否真的调用了 `chroma_list_collections`

### A3. 调研MCP启动新会话的能力

1. 查Cursor是否支持"MCP触发新Agent会话"
2. 如果不支持，调研替代方案：
   - Cursor CLI？
   - VS Code API？
   - 外部脚本调用Cursor？

---

## 实现方案（阶段B，待A完成后设计）

**预期架构**：

```
用户说"关窗"
  → 当前窗口AI检测到关窗信号
    → 调用MCP工具：保存当前对话到文件
      → MCP工具：启动新Cursor Agent窗口
        → 新窗口读取对话文件
          → 执行流程一（定性+因果链）
            → 执行流程二（画像/知识点/共识）
              → 写入知识库
```

**关键问题**：
- 当前对话如何导出？（Cursor有无API？）
- 新窗口如何启动？（MCP能否做到？）
- 新窗口如何自动加载数字真我SK？

---

## 验收标准

| 检查项 | 预期结果 |
|--------|---------|
| Cursor能调用chroma MCP | `chroma_list_collections` 返回结果 |
| MCP能启动新会话 | 有可行方案或明确不可行 |
| 关窗自动复盘可行性 | 有完整设计方案或替代方案 |

---

## 回报要求

完成阶段A后，回报数字真我窗口：
1. MCP配置问题根因
2. 启动新会话的可行方案（或不可行的原因）
3. 替代方案（如果MCP不支持）

---

## 参考资料

- V18验证记录：`vault/数字分身/数字分身/待执行指令/INFRA-001-阶段B执行报告.md`
- 数字真我SK v6（复盘方法论）：`.cursor/skills/数字真我/SKILL.md`
- V17核心共识："同上下文复盘不建议"
