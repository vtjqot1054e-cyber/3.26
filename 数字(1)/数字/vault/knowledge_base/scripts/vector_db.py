# 数字真我·精炼层向量库
# ChromaDB本地持久化，存放经审核的ABC精炼短文本
# 路径：数字分身/brain/vector_db.py

import chromadb
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "vector_store")

def get_client():
    return chromadb.PersistentClient(path=DB_PATH)

def get_collection(client=None):
    if client is None:
        client = get_client()
    return client.get_or_create_collection(
        name="refined_abc",
        metadata={"description": "数字真我精炼层：经审核的ABC短文本结晶"}
    )

def add_refined(collection, refined_id, text, metadata):
    """入库一条精炼。metadata必须包含：category(A/B/C), tags, source_file, line_numbers, confidence, review_status"""
    collection.add(
        ids=[refined_id],
        documents=[text],
        metadatas=[metadata]
    )

def query(collection, query_text, n_results=5, where_filter=None):
    """语义检索精炼库"""
    kwargs = {"query_texts": [query_text], "n_results": n_results}
    if where_filter:
        kwargs["where"] = where_filter
    return collection.query(**kwargs)

def count(collection):
    return collection.count()

def list_all(collection):
    """列出库中所有条目（调试用）"""
    return collection.get()


if __name__ == "__main__":
    client = get_client()
    col = get_collection(client)
    print(f"精炼层向量库已就绪，当前条目数：{count(col)}")
    print(f"存储路径：{os.path.abspath(DB_PATH)}")
