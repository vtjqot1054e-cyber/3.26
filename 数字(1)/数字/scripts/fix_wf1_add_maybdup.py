# -*- coding: utf-8 -*-
"""
修复WF1：list-pending 节点加入「可能重复」目录扫描
确保已清理到「可能重复」的文件不会被WF1重新生成
"""

import json
import os

WF1_PATHS = [
    r"E:\数字\vault\数字分身\N8N\01-A对话清洗标注.json",
    r"E:\数字\N8N\01-A对话清洗标注.json",
]

def fix(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changed = False
    for node in data['nodes']:
        if node.get('id') == 'list-pending':
            code = node['parameters']['jsCode']
            if '可能重复' in code:
                print("  已包含「可能重复」，跳过")
                continue

            # 加 maybeDupDir 变量
            old_deleted = "const deletedDir = path.join(vaultPath, '\u5bf9\u8bdd\u5220\u9664');"
            new_deleted = "const deletedDir = path.join(vaultPath, '\u5bf9\u8bdd\u5220\u9664');\nconst maybeDupDir = path.join(vaultPath, '\u53ef\u80fd\u91cd\u590d');"
            code = code.replace(old_deleted, new_deleted)

            # 扫描目录列表加入 maybeDupDir
            code = code.replace(
                "for (const dir of [pendingDir, deletedDir])",
                "for (const dir of [pendingDir, deletedDir, maybeDupDir])"
            )

            node['parameters']['jsCode'] = code
            changed = True
            print("  list-pending: 加入「可能重复」目录")

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("  已保存")
    return changed

def main():
    for fp in WF1_PATHS:
        if not os.path.exists(fp):
            print("文件不存在:", fp)
            continue
        print("处理:", fp)
        fix(fp)

    # 验证
    print("\n=== 验证 ===")
    for fp in WF1_PATHS:
        if not os.path.exists(fp):
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        has_maybe = '可能重复' in content
        has_3dirs = 'maybeDupDir' in content
        print("%s:" % fp)
        print("  包含「可能重复」: %s" % has_maybe)
        print("  maybeDupDir变量: %s" % has_3dirs)

if __name__ == '__main__':
    main()
