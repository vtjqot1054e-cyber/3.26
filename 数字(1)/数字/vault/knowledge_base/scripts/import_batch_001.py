# 数字真我·第一批精炼入库（32条）
# 审核人：数字真我-03，2026-03-19
# 审核结果：32/32通过，0退回

import json
import os
from vector_db import get_client, get_collection, add_refined, count

DATA_FILE = os.path.join(os.path.dirname(__file__), "batch_001.json")

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        batch = json.load(f)

    client = get_client()
    col = get_collection(client)

    before = count(col)
    success = 0
    for item in batch:
        try:
            add_refined(col, item["id"], item["text"], item["meta"])
            success += 1
        except Exception as e:
            print(f"入库失败 {item['id']}: {e}")

    after = count(col)
    print(f"入库完成：{success}/{len(batch)}条成功")
    print(f"库中条目：{before} -> {after}")

    all_items = col.get()
    a_count = sum(1 for m in all_items["metadatas"] if m["category"] == "A")
    b_count = sum(1 for m in all_items["metadatas"] if m["category"] == "B")
    c_count = sum(1 for m in all_items["metadatas"] if m["category"] == "C")
    print(f"分类统计：A画像={a_count}条, B知识={b_count}条, C用户观点={c_count}条")

if __name__ == "__main__":
    main()
