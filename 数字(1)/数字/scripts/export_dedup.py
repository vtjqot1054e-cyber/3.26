# -*- coding: utf-8 -*-
"""
任务三：对话导出目录存量去重
- 扫描 E:\数字\vault\数字分身\对话导出\ 所有 .md
- 提取 SPE 核心文件名（去掉 [导出] YYYY-MM-DD-HHMM- 前缀）
- 按分钟级时间戳分组
- 同组有 File A 来源 + File B 来源：删除 File B 来源的
- 同组只有 File B 来源的：保留
"""

import os
import re

EXPORT_DIR = r"E:\数字\vault\数字分身\对话导出"

# 提取核心SPE文件名：去掉 [导出] YYYY-MM-DD-HHMM- 前缀
EXPORT_PREFIX = re.compile(r'^\[导出\] \d{4}-\d{2}-\d{2}-\d{4}-')

FILE_B_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})-(\d{2})Z')
FILE_A_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})Z')

def get_spe_core(filename):
    """从导出文件名提取SPE核心部分"""
    m = EXPORT_PREFIX.match(filename)
    if m:
        return filename[m.end():]
    return None

def classify_spe_core(core):
    """判断SPE核心文件名是 File A 还是 File B"""
    m = FILE_B_PATTERN.match(core)
    if m:
        return m.group(1), 'B'
    m = FILE_A_PATTERN.match(core)
    if m:
        return m.group(1), 'A'
    return None, None

def main():
    from collections import defaultdict

    files = [f for f in os.listdir(EXPORT_DIR) if f.endswith('.md')]
    print(f"对话导出文件总数: {len(files)}")

    groups = defaultdict(lambda: {'A': [], 'B': []})
    no_prefix = []
    no_classify = []

    for f in files:
        core = get_spe_core(f)
        if not core:
            no_prefix.append(f)
            continue
        ts, typ = classify_spe_core(core)
        if ts:
            groups[ts][typ].append(f)
        else:
            no_classify.append(f)

    deleted = []
    for ts in sorted(groups.keys()):
        g = groups[ts]
        if g['A'] and g['B']:
            for bf in g['B']:
                path = os.path.join(EXPORT_DIR, bf)
                os.remove(path)
                deleted.append(bf)

    print(f"\n去重结果:")
    print(f"  分组数: {len(groups)}")
    print(f"  删除File B来源: {len(deleted)}")
    print(f"  无前缀文件: {len(no_prefix)}")
    print(f"  无法分类: {len(no_classify)}")

    if deleted:
        print(f"\n删除清单:")
        for f in sorted(deleted):
            print(f"  - {f}")

    if no_prefix:
        print(f"\n无[导出]前缀的文件（未处理）:")
        for f in sorted(no_prefix):
            print(f"  - {f}")

    # 验收
    remaining = [f for f in os.listdir(EXPORT_DIR) if f.endswith('.md')]
    print(f"\n验收: 对话导出目录剩余 {len(remaining)} 个文件")

if __name__ == '__main__':
    main()
