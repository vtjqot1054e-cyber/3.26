# -*- coding: utf-8 -*-
"""
修改WF3路径：D盘→E盘
同时更新 vault 和根目录两个副本
"""

import json
import os

WF3_PATHS = [
    r"E:\数字\vault\数字分身\N8N\03-用户校对归档.json",
    r"E:\数字\N8N\03-用户校对归档.json",
]

OLD_VAULT = "D:\\\\数字分身2\\\\vault\\\\数字分身"
NEW_VAULT = "E:\\\\数字\\\\vault\\\\数字分身"

def fix(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changes = []
    for node in data['nodes']:
        params = node.get('parameters', {})
        code = params.get('jsCode', '')
        if not code:
            continue
        if OLD_VAULT in code:
            code = code.replace(OLD_VAULT, NEW_VAULT)
            params['jsCode'] = code
            changes.append("[%s] %s: vaultPath D盘→E盘" % (node.get('id', ''), node.get('name', '')))

    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return changes

def verify(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    d_count = content.count(OLD_VAULT)
    has_e = NEW_VAULT in content
    return d_count, has_e

def main():
    for fp in WF3_PATHS:
        if not os.path.exists(fp):
            print("文件不存在: %s" % fp)
            continue
        print("处理: %s" % fp)
        changes = fix(fp)
        for c in changes:
            print("  " + c)
        if not changes:
            print("  无需修改")

    print("\n=== 自查 ===")
    for fp in WF3_PATHS:
        if not os.path.exists(fp):
            continue
        d_count, has_e = verify(fp)
        print("%s:" % fp)
        print("  D盘路径残留: %d (应为0)" % d_count)
        print("  E盘路径存在: %s (应为True)" % has_e)

        # 额外验证：提取所有 vaultPath 行
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for node in data['nodes']:
            code = node.get('parameters', {}).get('jsCode', '')
            if not code:
                continue
            for line in code.split('\n'):
                if 'vaultPath' in line and '=' in line and '//' not in line.strip()[:2]:
                    print("  [%s] %s" % (node.get('id', ''), line.strip()))

if __name__ == '__main__':
    main()
