# 数字真我·第四批精炼入库（5条通过+1条合并更新B3-A2）
# 来源：数字真我-08复盘报告（复盘大脑独立分析）
# 审核人：数字真我-12，2026-03-23
# C-精炼-2降级为信号强化（不入库），C-精炼-3已存在（不入库）
# A-精炼-1合并到B3-A2（更新已有条目）

import json
import os
from vector_db import get_client, get_collection, add_refined, count

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "batch_data", "batch_004.json")

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        batch = json.load(f)

    client = get_client()
    col = get_collection(client)

    before = count(col)

    # 先处理A-精炼-1的合并：更新B3-A2
    try:
        col.update(
            ids=["B3-A2"],
            documents=["用户的焦虑聚焦在'信息丢失'和'系统不完整'两个具体触发点，不是泛化焦虑。'需要写入！！！'和'这轮对话关了，这些讨论过程和决策逻辑就丢了'都指向同一个焦虑核心：对话结束后上下文消失。跨篇补充（数字真我-08）：这种焦虑有一个固定模式——发现缺口->意识到修复代价->陷入进退两难。'面上看能够提高准确性……忘了本身该做的事是审稿。郁闷'——用户清楚地看到了改进路径，也清楚地看到了改进的副作用（流程又出问题、本职工作被挤占）。这不是对改进本身的抗拒，而是对'每次改进都会引发新问题'的系统性体验的积累性疲惫。"],
            metadatas=[{
                "category": "A",
                "tags": "profile_anxiety_pattern,profile_emotion_trigger,information_loss_anxiety,system_anxiety,improvement_fatigue",
                "source_file": "2026-03-23_05-37-59Z+2026-03-22_09-59-51Z",
                "line_numbers": "282,1069-1071,689",
                "confidence": "高",
                "review_status": "通过",
                "review_date": "2026-03-23"
            }]
        )
        print("已更新 B3-A2（合并A-精炼-1）")
    except Exception as e:
        print(f"更新B3-A2失败: {e}")

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
    print(f"\n入库完成：{success}条新增，{skip}条跳过，1条合并更新")
    print(f"库中条目：{before} -> {after}")

    all_items = col.get()
    a_count = sum(1 for m in all_items["metadatas"] if m["category"] == "A")
    b_count = sum(1 for m in all_items["metadatas"] if m["category"] == "B")
    c_count = sum(1 for m in all_items["metadatas"] if m["category"] == "C")
    print(f"分类统计：A画像={a_count}条, B知识={b_count}条, C用户观点={c_count}条")

if __name__ == "__main__":
    main()
