# -*- coding: utf-8 -*-
"""
任务一：D盘SPE历史文件导入E盘（去重后复制）
- 读取D盘 .specstory/history/ 下所有 .md
- 按分钟级时间戳分组，同组只保留 File A（不带秒）
- 同组只有 File B 没有 File A 的情况保留 File B
- 复制到 E盘 .specstory/history/
- E盘已存在同名文件则跳过
- 同时将所有D盘文件（含被丢弃的File B）复制到比对文件夹供审查
"""

import os
import re
import shutil
from collections import defaultdict

D_SPE_DIR = r"D:\数字分身2\.specstory\history"
E_SPE_DIR = r"E:\数字\.specstory\history"
COMPARE_DIR = r"E:\数字\.specstory\D盘原始文件比对"

FILE_B_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})-(\d{2})Z')
FILE_A_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})Z')

def classify_file(filename):
    """返回 (分钟级时间戳, 'A'或'B')"""
    m = FILE_B_PATTERN.match(filename)
    if m:
        return m.group(1), 'B'
    m = FILE_A_PATTERN.match(filename)
    if m:
        return m.group(1), 'A'
    return None, None

def main():
    os.makedirs(E_SPE_DIR, exist_ok=True)
    os.makedirs(COMPARE_DIR, exist_ok=True)

    d_files = [f for f in os.listdir(D_SPE_DIR) if f.endswith('.md')]
    print(f"D盘SPE文件总数: {len(d_files)}")

    # 先把所有D盘文件复制到比对文件夹
    compare_copied = 0
    for f in d_files:
        src = os.path.join(D_SPE_DIR, f)
        dst = os.path.join(COMPARE_DIR, f)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            compare_copied += 1
    print(f"比对文件夹: 复制了 {compare_copied} 个文件到 {COMPARE_DIR}")

    # 按分钟级时间戳分组
    groups = defaultdict(lambda: {'A': [], 'B': []})
    unclassified = []
    for f in d_files:
        ts, typ = classify_file(f)
        if ts:
            groups[ts][typ].append(f)
        else:
            unclassified.append(f)

    # 决定每组保留哪些文件
    to_import = []
    discarded_b = []
    for ts in sorted(groups.keys()):
        g = groups[ts]
        if g['A']:
            to_import.extend(g['A'])
            discarded_b.extend(g['B'])
        else:
            # 只有 File B，保留
            to_import.extend(g['B'])

    # 未分类文件也导入
    to_import.extend(unclassified)

    print(f"\n分组统计:")
    print(f"  总分组数: {len(groups)}")
    print(f"  待导入文件: {len(to_import)}")
    print(f"  丢弃的File B: {len(discarded_b)}")
    print(f"  未分类文件: {len(unclassified)}")

    # 复制到E盘
    imported = 0
    skipped = 0
    for f in to_import:
        src = os.path.join(D_SPE_DIR, f)
        dst = os.path.join(E_SPE_DIR, f)
        if os.path.exists(dst):
            skipped += 1
        else:
            shutil.copy2(src, dst)
            imported += 1

    print(f"\n导入结果:")
    print(f"  成功导入: {imported}")
    print(f"  跳过(已存在): {skipped}")
    print(f"  丢弃File B: {len(discarded_b)}")

    if discarded_b:
        print(f"\n丢弃的File B清单:")
        for f in sorted(discarded_b):
            print(f"  - {f}")

    if unclassified:
        print(f"\n未分类文件（已导入）:")
        for f in sorted(unclassified):
            print(f"  - {f}")

    # 验收统计
    e_files_after = [f for f in os.listdir(E_SPE_DIR) if f.endswith('.md')]
    e_file_a = [f for f in e_files_after if FILE_A_PATTERN.match(f) and not FILE_B_PATTERN.match(f)]
    e_file_b = [f for f in e_files_after if FILE_B_PATTERN.match(f)]
    print(f"\n验收: E盘SPE目录现有 {len(e_files_after)} 个文件 (File A: {len(e_file_a)}, File B: {len(e_file_b)})")

if __name__ == '__main__':
    main()
