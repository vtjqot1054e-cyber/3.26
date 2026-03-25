# 验证batch_002入库结果
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from vector_db import get_client, get_collection, query, count

client = get_client()
col = get_collection(client)
print(f"总条目：{count(col)}")

r = query(col, "用户注意力跳跃", n_results=3)
for i, (doc, meta) in enumerate(zip(r["documents"][0], r["metadatas"][0])):
    print(f"\n--- 结果{i+1} [{meta['category']}] ---")
    print(doc[:120])

print("\n--- 测试B类检索 ---")
r2 = query(col, "跨窗口风险", n_results=3)
for i, (doc, meta) in enumerate(zip(r2["documents"][0], r2["metadatas"][0])):
    print(f"\n结果{i+1} [{meta['category']}]: {doc[:100]}")
