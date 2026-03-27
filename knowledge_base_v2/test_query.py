# -*- coding: utf-8 -*-
"""
测试 ChromaDB 语义检索
"""
import chromadb

# 连接向量库
client = chromadb.PersistentClient(path="E:/数字/knowledge_base_v2/vector_store")
collection = client.get_collection(name="knowledge_base")

# 测试查询
query = "AI判断质量为什么会衰减"
results = collection.query(
    query_texts=[query],
    n_results=3
)

print(f"查询: {query}")
print(f"\n找到 {len(results['ids'][0])} 个相关文档:\n")

for i, (doc_id, distance, metadata) in enumerate(zip(
    results['ids'][0],
    results['distances'][0],
    results['metadatas'][0]
), 1):
    print(f"{i}. {metadata['title']}")
    print(f"   文件: {metadata['filename']}")
    print(f"   相似度: {1 - distance:.3f}")
    print()
