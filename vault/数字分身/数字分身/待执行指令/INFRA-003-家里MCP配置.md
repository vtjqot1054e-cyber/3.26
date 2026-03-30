# INFRA-003 · 家里环境MCP配置指令

**创建时间**：2026-03-28
**创建者**：数字真我-V20
**执行者**：工程窗口（Cursor Agent）
**状态**：completed

---

## 背景

公司环境（E盘Git同步）已完成INFRA-001（向量库部署）和INFRA-002阶段A（MCP排查），家里环境需要同步配置。

家里Cursor项目路径：`E:\家里2\3.26\`

---

## 阶段A：OB插件安装（Smart Connections）

### A1. 确认knowledge_base_v2可作为独立vault打开

```
路径：E:\家里2\3.26\knowledge_base_v2\
```

1. 打开Obsidian
2. 打开另一个仓库 → 选择 `E:\家里2\3.26\knowledge_base_v2\`
3. 这样Graph View只显示知识库的22条数据和双链关系

### A2. 安装Smart Connections插件

1. 在knowledge_base_v2这个vault中
2. 设置 → 第三方插件 → 关闭安全模式
3. 浏览 → 搜索 "Smart Connections"
4. 安装并启用
5. 等待索引完成（看右下角进度）

### A3. 验证

| 检查项 | 预期结果 |
|--------|---------|
| 插件已安装 | 设置中可见Smart Connections |
| 索引完成 | `.smart-env/` 文件夹存在 |
| 语义搜索可用 | Connections面板能显示相关笔记 |

---

## 阶段B：ChromaDB向量库部署

### B1. 检查环境

```powershell
python --version   # 需要3.9+
uv --version       # 如果没有：pip install uv
```

### B2. 创建存储目录

```powershell
mkdir "E:\家里2\3.26\knowledge_base_v2\vector_store"
```

### B3. 配置Cursor MCP

在项目根目录创建 `.cursor/mcp.json`：

```powershell
mkdir "E:\家里2\3.26\.cursor"
```

写入内容：

```json
{
  "mcpServers": {
    "chroma": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "chroma-mcp",
        "--client-type", "persistent",
        "--data-dir", "E:/家里2/3.26/knowledge_base_v2/vector_store"
      ]
    }
  }
}
```

**注意**：必须有 `"type": "stdio"`，公司环境之前就是因为缺少这个字段导致Cursor不调用MCP。

### B4. 导入知识库到ChromaDB

创建导入脚本 `knowledge_base_v2/import_to_chroma.py`：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入knowledge_base_v2到ChromaDB向量库
"""

import os
import chromadb
from pathlib import Path

# 配置
KB_DIR = Path(r"E:\家里2\3.26\knowledge_base_v2")
VECTOR_DIR = KB_DIR / "vector_store"
COLLECTION_NAME = "knowledge_base_v2"

def main():
    # 初始化ChromaDB
    client = chromadb.PersistentClient(path=str(VECTOR_DIR))
    
    # 获取或创建collection
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass
    collection = client.create_collection(name=COLLECTION_NAME)
    
    # 读取所有MD文件
    md_files = list(KB_DIR.glob("*.md"))
    md_files = [f for f in md_files if f.name != "_INDEX.md"]
    
    documents = []
    metadatas = []
    ids = []
    
    for f in md_files:
        content = f.read_text(encoding="utf-8")
        documents.append(content)
        metadatas.append({"filename": f.name, "path": str(f)})
        ids.append(f.stem)
    
    # 导入
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"已导入 {len(documents)} 个文档到 {COLLECTION_NAME}")
    else:
        print("没有找到MD文件")

if __name__ == "__main__":
    main()
```

执行：

```powershell
cd E:\家里2\3.26\knowledge_base_v2
pip install chromadb
python import_to_chroma.py
```

### B5. 重启Cursor并验证

1. 重启Cursor
2. 新对话中输入："请使用MCP工具chroma_list_collections"
3. 观察是否成功调用

---

## 验收标准

| 检查项 | 预期结果 |
|--------|---------|
| knowledge_base_v2独立vault | Graph View只显示22条知识+双链 |
| Smart Connections可用 | 语义搜索功能正常 |
| ChromaDB向量库 | 22个文档已导入 |
| MCP配置 | `.cursor/mcp.json` 存在且格式正确 |

---

## 注意事项

1. **家里路径**：`E:\家里2\3.26\`，不是`E:\数字\`
2. **必须有type字段**：`"type": "stdio"` 不能省略
3. **先A后B**：OB插件是必做的，ChromaDB是可选的

## 执行结果（2026-03-28）

**执行者**：工程窗口  
**执行时间**：2026-03-28

### 阶段A：OB插件安装 ✅

- knowledge_base_v2 已作为独立vault在 Obsidian 中打开
- Smart Connections 插件已安装并启用
- 索引已生成（`.smart-env/` 目录存在）
- 语义搜索功能正常

### 阶段B：ChromaDB向量库部署 ✅

#### B1. 环境检查
- Python 3.10.9 ✅
- uv 0.11.2 ✅（已安装）

#### B2. 存储目录
- 已创建：`E:\家里2\3.26\knowledge_base_v2\vector_store`

#### B3. MCP配置
- 已创建：`E:\家里2\3.26\.cursor\mcp.json`
- 配置包含 `"type": "stdio"` 字段

#### B4. 导入结果
- ChromaDB 1.5.5 已安装
- 成功导入 **33个文档** 到 collection `knowledge_base_v2`
- 向量库文件：`E:\家里2\3.26\knowledge_base_v2\vector_store\chroma.sqlite3`（1.5MB）

#### B5. 验收状态

| 检查项 | 预期结果 | 实际结果 |
|--------|---------|---------|
| knowledge_base_v2独立vault | Graph View只显示知识库数据和双链 | ✅ 已确认 |
| Smart Connections可用 | 语义搜索功能正常 | ✅ 索引已生成 |
| ChromaDB向量库 | 文档已导入 | ✅ 33个文档 |
| MCP配置 | `.cursor/mcp.json` 存在且格式正确 | ✅ 已创建 |

### 下一步操作

1. **重启Cursor**（必须）
2. **在新对话窗口中测试MCP**：输入 "请使用MCP工具chroma_list_collections"
3. 观察是否成功调用向量库

### 注意事项

- 指令中提到的"22个文档"实际为 **33个文档**（knowledge_base_v2 当前文件数）
- Python包管理在Windows上需使用 `py -m pip` 而非直接 `pip` 命令
- 导入脚本已修复Windows编码问题（GBK vs UTF-8）

---

## 完成后

- ✅ 已更新交接备忘（SYS-001状态更新为已完成）
- 待用户验证MCP调用

---
