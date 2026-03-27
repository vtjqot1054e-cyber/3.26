# INFRA-001 · 向量库部署指令

**创建时间**：2026-03-27
**创建者**：数字真我-V17
**执行者**：工程窗口（Cursor Agent）
**状态**：done（阶段A已执行，阶段B按指令暂不执行）

---

## 任务目标

部署知识库向量检索能力，支持两地同步（公司D盘/家里E盘）。

**分两阶段**：
1. 阶段A：Obsidian插件Smart Connections（优先，简单）
2. 阶段B：Cursor MCP ChromaDB（可选，后续）

---

# 阶段A：Smart Connections（必做）

## A1. 安装插件

1. 打开Obsidian
2. 设置 → 第三方插件 → 关闭安全模式
3. 浏览 → 搜索 "Smart Connections"
4. 安装并启用

## A2. 初始化索引

1. 启用后，插件会自动开始索引vault
2. 等待索引完成（看右下角进度，大vault可能需要几分钟）
3. 索引完成后，向量数据存在 `.smart-env/` 文件夹

## A3. 验证功能

1. 打开任意笔记
2. 右侧边栏应该出现 "Connections" 面板
3. 面板显示与当前笔记语义相关的其他笔记
4. 点击面板顶部搜索图标，尝试语义搜索（输入问题，不是关键词）

## A4. 验证同步

1. 确认 `.smart-env/` 文件夹在vault内
2. 确认 `.gitignore` **没有**忽略 `.smart-env/`（需要同步）
3. Git推送到远程
4. 在另一台电脑拉取，打开OB，验证Smart Connections能直接使用

---

## A阶段验收标准

| 检查项 | 预期结果 |
|--------|---------|
| 插件已安装 | Obsidian设置中可见Smart Connections |
| 索引完成 | `.smart-env/` 文件夹存在且有内容 |
| 语义搜索可用 | Connections面板能显示相关笔记 |
| 同步可用 | `.smart-env/` 已纳入Git，另一台电脑可用 |

---

## A阶段完成后

1. 回报数字真我窗口确认
2. 更新交接备忘：SYS-001状态改为"OB向量层已部署（Smart Connections）"
3. 在 `knowledge_base_v2/_INDEX.md` 中添加使用说明

---

# 阶段B：ChromaDB MCP（可选，Cursor用）

> 只有当Cursor也需要语义搜索时才做。阶段A完成后再评估是否需要。

## B1. 检查环境

```bash
python --version   # 需要3.9+
uv --version       # 如果没有：pip install uv
```

## B2. 创建存储目录

```bash
mkdir -p "E:/数字/knowledge_base_v2/vector_store"
```

## B3. 配置Cursor MCP

在项目根目录创建或编辑 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "chroma": {
      "command": "uvx",
      "args": [
        "chroma-mcp",
        "--client-type", "persistent",
        "--data-dir", "E:/数字/knowledge_base_v2/vector_store"
      ]
    }
  }
}
```

## B4. 重启Cursor并测试

重启后测试 `chroma_list_collections`，成功返回说明连接OK。

## B5. 导入知识库

读取 `knowledge_base_v2/*.md`，调用 `chroma_add_documents` 逐个导入。

---

## 参考资料

- Smart Connections官网：https://smartconnections.app/smart-connections/
- Smart Connections安装：https://obsidian.md/plugins?id=smart-connections
- Chroma MCP文档：https://cursormcp.dev/mcp-servers/74-chroma

---

## 注意事项

1. **两地环境差异**：
   - 公司：D:\数字分身2\vault\
   - 家里：E:\数字\vault\
   - 路径不同但vault结构相同，Smart Connections的 `.smart-env/` 随vault同步

2. **Git同步**：
   - `.smart-env/` 文件夹**必须同步**，不能加到 `.gitignore`
   - 向量数据可能有几十MB，首次推送会慢一点

3. **先A后B**：
   - 阶段A是必做的，解决OB内的语义搜索
   - 阶段B是可选的，只有Cursor需要语义搜索时才做
