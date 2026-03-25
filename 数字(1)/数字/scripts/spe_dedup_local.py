# -*- coding: utf-8 -*-
"""
任务二：E盘SPE目录存量去重
- 扫描 E:\数字\.specstory\history\ 所有 .md
- 按分钟级时间戳分组
- 同组有 File A + File B：删除 File B
- 同组只有 File B：保留
- 同组有多个 File A（不同标题）：全部保留
"""

import os
import re
from collections import defaultdict

E_SPE_DIR = r"E:\数字\.specstory\history"

FILE_B_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})-(\d{2})Z')
FILE_A_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})Z')

def classify_file(filename):
    m = FILE_B_PATTERN.match(filename)
    if m:
        return m.group(1), 'B'
    m = FILE_A_PATTERN.match(filename)
    if m:
        return m.group(1), 'A'
    return None, None

def main():
    files = [f for f in os.listdir(E_SPE_DIR) if f.endswith('.md')]
    print(f"E盘SPE文件总数: {len(files)}")

    groups = defaultdict(lambda: {'A': [], 'B': []})
    for f in files:
        ts, typ = classify_file(f)
        if ts:
            groups[ts][typ].append(f)

    deleted = []
    kept_b_only = []
    for ts in sorted(groups.keys()):
        g = groups[ts]
        if g['A'] and g['B']:
            for bf in g['B']:
                path = os.path.join(E_SPE_DIR, bf)
                os.remove(path)
                deleted.append(bf)
        elif not g['A'] and g['B']:
            kept_b_only.extend(g['B'])

    print(f"\n去重结果:")
    print(f"  删除File B: {len(deleted)}")
    print(f"  保留(只有File B的组): {len(kept_b_only)}")

    if deleted:
        print(f"\n删除清单:")
        for f in sorted(deleted):
            print(f"  - {f}")

    if kept_b_only:
        print(f"\n保留的孤立File B:")
        for f in sorted(kept_b_only):
            print(f"  - {f}")

    # 验收
    remaining = [f for f in os.listdir(E_SPE_DIR) if f.endswith('.md')]
    r_a = [f for f in remaining if FILE_A_PATTERN.match(f) and not FILE_B_PATTERN.match(f)]
    r_b = [f for f in remaining if FILE_B_PATTERN.match(f)]
    print(f"\n验收: E盘SPE目录剩余 {len(remaining)} 个文件 (File A: {len(r_a)}, File B: {len(r_b)})")

    # 检查是否还有A+B共存
    groups2 = defaultdict(lambda: {'A': [], 'B': []})
    for f in remaining:
        ts, typ = classify_file(f)
        if ts:
            groups2[ts][typ].append(f)
    coexist = sum(1 for g in groups2.values() if g['A'] and g['B'])
    print(f"  A+B共存组数: {coexist} (应为0)")

if __name__ == '__main__':
    main()
