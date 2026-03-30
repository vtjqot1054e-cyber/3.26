#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
列出ChromaDB向量库中的所有collections
"""

import chromadb
from pathlib import Path

# 配置
VECTOR_DIR = Path(r"E:\家里2\3.26\knowledge_base_v2\vector_store")

def main():
    print(f"向量库路径: {VECTOR_DIR}")
    print(f"向量库存在: {VECTOR_DIR.exists()}")
    print()
    
    try:
        # 连接ChromaDB
        client = chromadb.PersistentClient(path=str(VECTOR_DIR))
        
        # 列出所有collections
        collections = client.list_collections()
        
        print(f"找到 {len(collections)} 个collection:")
        print()
        
        for coll in collections:
            print(f"Collection: {coll.name}")
            print(f"  - 文档数量: {coll.count()}")
            print(f"  - 元数据: {coll.metadata}")
            print()
            
            # 获取前3个文档示例
            if coll.count() > 0:
                results = coll.get(limit=3)
                print(f"  - 示例文档ID:")
                for doc_id in results['ids']:
                    print(f"    * {doc_id}")
                print()
    
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
