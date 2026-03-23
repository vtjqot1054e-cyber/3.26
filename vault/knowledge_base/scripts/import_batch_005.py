# 数字真我·第五批精炼入库（8条）
# 来源：总顾问大脑-08复盘报告（复盘大脑独立分析）
# 审核人：数字真我-12，2026-03-23

import json
import os
from vector_db import get_client, get_collection, add_refined, count

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "batch_data", "batch_005.json")

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        batch = json.load(f)

    client = get_client()
    col = get_collection(client)

    before = count(col)
    success = 0
    skip = 0
    for item in batch:
        try:
            existing = col.get(ids=[item["id"]])
            if existing and existing["ids"]:
                print(f"跳过已存在 {item['id']}")
                skip += 1
                continue
            add_refined(col, item["id"], item["text"], item["meta"])
            success += 1
        except Exception as e:
            print(f"入库失败 {item['id']}: {e}")

    after = count(col)
    print(f"\n入库完成：{success}条新增，{skip}条跳过")
    print(f"库中条目：{before} -> {after}")

    all_items = col.get()
    a_count = sum(1 for m in all_items["metadatas"] if m["category"] == "A")
    b_count = sum(1 for m in all_items["metadatas"] if m["category"] == "B")
    c_count = sum(1 for m in all_items["metadatas"] if m["category"] == "C")
    print(f"分类统计：A画像={a_count}条, B知识={b_count}条, C用户观点={c_count}条")

if __name__ == "__main__":
    main()
