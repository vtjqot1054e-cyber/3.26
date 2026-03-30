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
    print(f"知识库目录: {KB_DIR}")
    print(f"向量库目录: {VECTOR_DIR}")
    
    # 初始化ChromaDB
    client = chromadb.PersistentClient(path=str(VECTOR_DIR))
    
    # 获取或创建collection
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"已删除旧collection: {COLLECTION_NAME}")
    except:
        pass
    
    collection = client.create_collection(name=COLLECTION_NAME)
    print(f"已创建collection: {COLLECTION_NAME}")
    
    # 读取所有MD文件
    md_files = list(KB_DIR.glob("*.md"))
    md_files = [f for f in md_files if f.name != "_INDEX.md"]
    
    print(f"\n找到 {len(md_files)} 个MD文件")
    
    documents = []
    metadatas = []
    ids = []
    
    for f in md_files:
        try:
            content = f.read_text(encoding="utf-8")
            documents.append(content)
            metadatas.append({"filename": f.name, "path": str(f)})
            ids.append(f.stem)
            print(f"  OK {f.name}")
        except Exception as e:
            print(f"  ERR {f.name}: {e}")
    
    # 导入
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"\n[OK] 已导入 {len(documents)} 个文档到 {COLLECTION_NAME}")
        
        # 验证
        count = collection.count()
        print(f"[OK] 向量库中现有 {count} 个文档")
    else:
        print("[ERR] 没有找到MD文件")

if __name__ == "__main__":
    main()
