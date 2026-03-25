# -*- coding: utf-8 -*-
"""
任务五：修复WF1
1. 所有节点 vaultPath 从 D:\\数字分身2\\vault\\数字分身 改为 E:\\数字\\vault\\数字分身
2. specstory-preclean 的 speDir 改为 E:\\数字\\.specstory\\history（不再用相对路径拼接）
3. specstory-preclean 加源头过滤：遍历 speFiles 时先过滤掉 File B
4. 同时更新 vault 和根目录两个副本
"""

import json
import re
import os

WF1_PATHS = [
    r"E:\数字\vault\数字分身\N8N\01-A对话清洗标注.json",
    r"E:\数字\N8N\01-A对话清洗标注.json",
]

OLD_VAULT = r"D:\\数字分身2\\vault\\数字分身"
NEW_VAULT = r"E:\\数字\\vault\\数字分身"

def fix_wf1(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changes = []

    for node in data['nodes']:
        nid = node.get('id', '')
        nname = node.get('name', '')
        params = node.get('parameters', {})

        if 'jsCode' not in params:
            continue

        code = params['jsCode']
        original_code = code

        # 1. 替换所有 vaultPath
        if OLD_VAULT in code:
            code = code.replace(OLD_VAULT, NEW_VAULT)
            changes.append(f"  [{nid}] {nname}: vaultPath D盘→E盘")

        # 2. specstory-preclean 特殊处理
        if nid == 'specstory-preclean':
            # 改 speDir 为绝对路径
            old_spe = "const speDir = path.join(vaultPath, '..', '..', '.specstory', 'history');"
            new_spe = "const speDir = 'E:\\\\数字\\\\.specstory\\\\history';"
            if old_spe in code:
                code = code.replace(old_spe, new_spe)
                changes.append(f"  [{nid}] {nname}: speDir 改为绝对路径")

            # 加源头过滤：在 for (const f of speFiles) 之前加过滤
            old_loop = "for (const f of speFiles) {"
            new_filter_and_loop = (
                "// 源头过滤：只处理 File A（不带秒），跳过 File B（带秒）\n"
                "const fileBPattern = /^\\d{4}-\\d{2}-\\d{2}_\\d{2}-\\d{2}-\\d{2}Z/;\n"
                "const filteredSpeFiles = speFiles.filter(f => !fileBPattern.test(f));\n"
                "let filteredOut = speFiles.length - filteredSpeFiles.length;\n\n"
                "for (const f of filteredSpeFiles) {"
            )
            if old_loop in code and 'fileBPattern' not in code:
                code = code.replace(old_loop, new_filter_and_loop)
                changes.append(f"  [{nid}] {nname}: 加 File B 源头过滤")

            # 修改 return 语句加上 filteredOut 统计
            old_return = "return { json: { cleaned: cleaned, skipped: skipped, errors: errors, processedCount: processedSpeNames.size } };"
            new_return = "return { json: { cleaned: cleaned, skipped: skipped, filteredFileB: filteredOut, errors: errors, processedCount: processedSpeNames.size } };"
            if old_return in code and 'filteredFileB' not in code:
                code = code.replace(old_return, new_return)
                changes.append(f"  [{nid}] {nname}: return 加 filteredFileB 统计")

        if code != original_code:
            params['jsCode'] = code

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return changes

def main():
    for fp in WF1_PATHS:
        if not os.path.exists(fp):
            print(f"文件不存在，跳过: {fp}")
            continue
        print(f"\n处理: {fp}")
        changes = fix_wf1(fp)
        if changes:
            for c in changes:
                print(c)
        else:
            print("  无需修改")

    # 验证
    print("\n=== 验证 ===")
    for fp in WF1_PATHS:
        if not os.path.exists(fp):
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        d_count = content.count(OLD_VAULT)
        e_count = content.count(NEW_VAULT)
        has_filter = 'fileBPattern' in content
        has_abs_spe = r"E:\\数字\\.specstory\\history" in content
        print(f"\n{fp}:")
        print(f"  D盘路径残留: {d_count} (应为0)")
        print(f"  E盘路径: {e_count}")
        print(f"  File B过滤: {'有' if has_filter else '无'}")
        print(f"  speDir绝对路径: {'有' if has_abs_spe else '无'}")

if __name__ == '__main__':
    main()
