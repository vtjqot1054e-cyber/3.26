# -*- coding: utf-8 -*-
"""
任务四：待确认目录存量去重
- 扫描 E:\数字\vault\数字分身\待确认\ 所有 .md
- 提取核心文件名（去掉 [待确认] 前缀）
- 按分钟级时间戳分组
- 已审阅文件（status != pending）不动
- 同组有 File A + File B 来源：将 File B 来源移到对话删除/
- 同组只有 File B 来源的：保留
- 2026-03-14_10-39 和 2026-03-14_10-43 两组标记为需人工确认，不自动处理
"""

import os
import re
import shutil
from collections import defaultdict

PENDING_DIR = r"E:\数字\vault\数字分身\待确认"
DELETE_DIR = r"E:\数字\vault\数字分身\对话删除"

PENDING_PREFIX = re.compile(r'^\[待确认\] ')
FILE_B_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})-(\d{2})Z')
FILE_A_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})Z')

MANUAL_GROUPS = {'2026-03-14_10-39', '2026-03-14_10-43'}

def get_core(filename):
    m = PENDING_PREFIX.match(filename)
    if m:
        return filename[m.end():]
    return None

def classify_core(core):
    m = FILE_B_PATTERN.match(core)
    if m:
        return m.group(1), 'B'
    m = FILE_A_PATTERN.match(core)
    if m:
        return m.group(1), 'A'
    return None, None

def read_status(filepath):
    """读取文件 frontmatter 中的 status 字段"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2000)
        if not content.startswith('---'):
            return None
        end = content.find('---', 3)
        if end == -1:
            return None
        fm = content[3:end]
        for line in fm.split('\n'):
            line = line.strip()
            if line.startswith('status:'):
                return line.split(':', 1)[1].strip()
    except:
        pass
    return None

def main():
    os.makedirs(DELETE_DIR, exist_ok=True)

    files = [f for f in os.listdir(PENDING_DIR) if f.endswith('.md')]
    print(f"待确认文件总数: {len(files)}")

    groups = defaultdict(lambda: {'A': [], 'B': []})
    no_prefix = []
    no_classify = []

    for f in files:
        core = get_core(f)
        if not core:
            no_prefix.append(f)
            continue
        ts, typ = classify_core(core)
        if ts:
            groups[ts][typ].append(f)
        else:
            no_classify.append(f)

    moved = []
    skipped_reviewed = []
    skipped_manual = []

    for ts in sorted(groups.keys()):
        g = groups[ts]

        # 需人工确认的组
        if ts in MANUAL_GROUPS:
            for f in g['A'] + g['B']:
                skipped_manual.append(f)
            continue

        if g['A'] and g['B']:
            for bf in g['B']:
                filepath = os.path.join(PENDING_DIR, bf)
                status = read_status(filepath)
                if status and status != 'pending':
                    skipped_reviewed.append((bf, status))
                    continue
                dst = os.path.join(DELETE_DIR, bf)
                shutil.move(filepath, dst)
                moved.append(bf)

    print(f"\n去重结果:")
    print(f"  分组数: {len(groups)}")
    print(f"  移到对话删除: {len(moved)}")
    print(f"  跳过(已审阅): {len(skipped_reviewed)}")
    print(f"  跳过(需人工确认): {len(skipped_manual)}")
    print(f"  无前缀: {len(no_prefix)}")
    print(f"  无法分类: {len(no_classify)}")

    if moved:
        print(f"\n移动清单:")
        for f in sorted(moved):
            print(f"  - {f}")

    if skipped_reviewed:
        print(f"\n跳过的已审阅文件:")
        for f, s in sorted(skipped_reviewed):
            print(f"  - {f} (status={s})")

    if skipped_manual:
        print(f"\n需人工确认（2026-03-14_10-39 和 10-43 两组）:")
        for f in sorted(skipped_manual):
            print(f"  - {f}")

    # 验收
    remaining = [f for f in os.listdir(PENDING_DIR) if f.endswith('.md')]
    print(f"\n验收: 待确认目录剩余 {len(remaining)} 个文件 (原 {len(files)} 个, 减少 {len(files) - len(remaining)} 个)")

if __name__ == '__main__':
    main()
