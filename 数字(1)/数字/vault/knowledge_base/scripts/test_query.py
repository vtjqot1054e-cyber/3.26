# 向量库检索测试（UTF-8输出）
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from vector_db import get_client, get_collection, query, count

col = get_collection()
print(f"库中条目：{count(col)}")
print()

print("=== 测试1：用户对AI的交互要求 ===")
r = query(col, "用户希望AI怎么和他交互", n_results=3)
for i in range(len(r["documents"][0])):
    doc = r["documents"][0][i]
    cat = r["metadatas"][0][i]["category"]
    sid = r["metadatas"][0][i].get("source_file", "")
    print(f"  {i+1}. [{cat}] {doc[:120]}")
    print(f"     来源: {sid}")
print()

print("=== 测试2：技术踩坑 ===")
r = query(col, "N8N技术问题和解决方案", n_results=3)
for i in range(len(r["documents"][0])):
    doc = r["documents"][0][i]
    cat = r["metadatas"][0][i]["category"]
    print(f"  {i+1}. [{cat}] {doc[:120]}")
print()

print("=== 测试3：只查A类画像 ===")
r = query(col, "用户的认知风格和决策模式", n_results=3, where_filter={"category": "A"})
for i in range(len(r["documents"][0])):
    doc = r["documents"][0][i]
    cat = r["metadatas"][0][i]["category"]
    print(f"  {i+1}. [{cat}] {doc[:120]}")

print()
print("=== 数据完整性 ===")
all_items = col.get()
a_count = sum(1 for m in all_items["metadatas"] if m["category"] == "A")
b_count = sum(1 for m in all_items["metadatas"] if m["category"] == "B")
c_count = sum(1 for m in all_items["metadatas"] if m["category"] == "C")
print(f"总计: {count(col)}条 | A画像={a_count} | B知识={b_count} | C用户观点={c_count}")
sources = set(m["source_file"] for m in all_items["metadatas"])
print(f"来源文件数: {len(sources)}")
for s in sorted(sources):
    file_count = sum(1 for m in all_items["metadatas"] if m["source_file"] == s)
    print(f"  {s}: {file_count}条")
