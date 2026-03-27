# -*- coding: utf-8 -*-
"""
将 knowledge_base_v2 的 MD 文件导入到 ChromaDB
"""
import chromadb
from pathlib import Path
import re

# 初始化 ChromaDB 客户端
client = chromadb.PersistentClient(path="E:/数字/knowledge_base_v2/vector_store")

# 创建或获取集合
collection = client.get_or_create_collection(
    name="knowledge_base",
    metadata={"description": "数字真我知识库v2"}
)

# 扫描所有 MD 文件
kb_dir = Path("E:/数字/knowledge_base_v2")
md_files = list(kb_dir.glob("*.md"))

print(f"找到 {len(md_files)} 个 MD 文件")

# 导入文件
imported_count = 0
for md_file in md_files:
    if md_file.name.startswith("_"):
        print(f"跳过: {md_file.name}")
        continue
    
    # 读取文件内容
    content = md_file.read_text(encoding="utf-8")
    
    # 提取文件名作为 ID（去除 .md 后缀）
    doc_id = md_file.stem
    
    # 提取标题（第一个 # 开头的行）
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else doc_id
    
    # 导入到 ChromaDB
    try:
        collection.add(
            documents=[content],
            ids=[doc_id],
            metadatas=[{
                "title": title,
                "filename": md_file.name,
                "source": "knowledge_base_v2"
            }]
        )
        print(f"[OK] 导入: {md_file.name}")
        imported_count += 1
    except Exception as e:
        print(f"[FAIL] 失败: {md_file.name} - {str(e)}")

print(f"\n导入完成: {imported_count}/{len(md_files)} 个文件")

# 验证导入
total_docs = collection.count()
print(f"向量库当前文档数: {total_docs}")
