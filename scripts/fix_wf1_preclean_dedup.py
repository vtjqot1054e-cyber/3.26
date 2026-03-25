# -*- coding: utf-8 -*-
"""
修复WF1 specstory-preclean：加强去重逻辑
在 processedSpeNames 构建时，额外扫描待确认+可能重复+对话删除目录
用 normalizeSpeName 做比对，确保 File A 和 File B 来源的文件都被识别为已处理
"""

import json
import os

WF1_PATHS = [
    r"E:\数字\vault\数字分身\N8N\01-A对话清洗标注.json",
    r"E:\数字\N8N\01-A对话清洗标注.json",
]

# 要在 processedSpeNames 构建完成后、for 循环之前插入的代码
EXTRA_DEDUP_CODE = r"""
// 额外扫描：待确认+可能重复+对话删除目录，提取SPE原始文件名加入已处理集合
// 防止同一对话的 File A / File B 因标题slug不同而漏过去重
const extraDirs = ['待确认', '可能重复', '对话删除'];
for (const dirName of extraDirs) {
  const dirPath = path.join(vaultPath, dirName);
  let dirFiles = [];
  try { dirFiles = fs.readdirSync(dirPath).filter(f => f.endsWith('.md')); } catch(e) {}
  for (const df of dirFiles) {
    // 去掉 [待确认] / [可能重复] 等前缀
    const coreName = df.replace(/^\[.*?\]\s*/, '');
    processedSpeNames.add(normalizeSpeName(coreName));
  }
}
"""

def fix(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changed = False
    for node in data['nodes']:
        if node.get('id') == 'specstory-preclean':
            code = node['parameters']['jsCode']
            if '额外扫描' in code:
                print("  已包含额外扫描逻辑，跳过")
                continue

            # 在 "源头过滤" 注释之前插入额外去重代码
            marker = "// 源头过滤：只处理 File A"
            if marker in code:
                code = code.replace(marker, EXTRA_DEDUP_CODE.strip() + "\n\n" + marker)
                node['parameters']['jsCode'] = code
                changed = True
                print("  specstory-preclean: 加入额外目录扫描去重")

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
        has_extra = '额外扫描' in content
        has_extradirs = 'extraDirs' in content
        print("%s:" % fp)
        print("  额外扫描逻辑: %s" % has_extra)
        print("  extraDirs变量: %s" % has_extradirs)

if __name__ == '__main__':
    main()
