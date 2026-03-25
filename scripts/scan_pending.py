import os, re, json

pending_dir = r"E:\数字\vault\数字分身\待确认"
results = []

for fname in sorted(os.listdir(pending_dir)):
    if not fname.endswith('.md'):
        continue
    fpath = os.path.join(pending_dir, fname)
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        results.append({"file": fname, "error": "读取失败"})
        continue

    if not content.strip():
        results.append({"file": fname, "size": 0, "empty": True})
        continue

    info = {"file": fname, "size": len(content)}

    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        for key in ['title', 'turns', 'status', 'models', 'date']:
            m = re.search(rf'^{key}:\s*(.+)$', fm, re.MULTILINE)
            if m:
                info[key] = m.group(1).strip().strip('"').strip("'")

    lines = content.split('\n')
    user_lines = []
    ai_lines = []
    for i, line in enumerate(lines):
        if '👤' in line or '用户' in line.lower():
            for j in range(i+1, min(i+4, len(lines))):
                if lines[j].strip() and not lines[j].startswith('#') and not lines[j].startswith('_'):
                    user_lines.append(lines[j].strip()[:100])
                    break
        if 'Agent' in line and 'claude' in line.lower():
            ai_lines.append(1)

    info['user_first_msg'] = user_lines[0] if user_lines else ''
    info['user_msg_count'] = len(user_lines)
    info['ai_msg_count'] = len(ai_lines)
    info['total_lines'] = len(lines)

    results.append(info)

with open(r"E:\数字\scripts\pending_scan.json", 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"扫描完成：{len(results)}个文件")

cats = {"空文件": 0, "1-2轮": 0, "3-10轮": 0, "10-20轮": 0, "20+轮": 0}
status_count = {}
themes = {"N8N/WF": 0, "SK/窗口": 0, "数字真我/复盘": 0, "工程/技术": 0, "业务/投标": 0, "探索/调研": 0, "杂务/短对话": 0}

for r in results:
    if r.get('empty'):
        cats["空文件"] += 1
        continue
    turns = int(r.get('turns', 0))
    if turns <= 2: cats["1-2轮"] += 1
    elif turns <= 10: cats["3-10轮"] += 1
    elif turns <= 20: cats["10-20轮"] += 1
    else: cats["20+轮"] += 1

    s = r.get('status', 'unknown')
    status_count[s] = status_count.get(s, 0) + 1

    fn = r['file'].lower()
    if any(k in fn for k in ['n8n', 'wf', 'workflow']): themes["N8N/WF"] += 1
    elif any(k in fn for k in ['sk', '窗口', '架构', 'skill', 'agent']): themes["SK/窗口"] += 1
    elif any(k in fn for k in ['真我', '复盘', '精炼']): themes["数字真我/复盘"] += 1
    elif any(k in fn for k in ['工程', '技术', 'so4', 'op4']): themes["工程/技术"] += 1
    elif any(k in fn for k in ['投标', '顾问']): themes["业务/投标"] += 1
    elif any(k in fn for k in ['调研', 'search', 'comparison', 'review']): themes["探索/调研"] += 1
    else: themes["杂务/短对话"] += 1

print(f"\n=== 轮次分布 ===")
for k, v in cats.items(): print(f"  {k}: {v}")
print(f"\n=== 状态分布 ===")
for k, v in sorted(status_count.items()): print(f"  {k}: {v}")
print(f"\n=== 主题分布 ===")
for k, v in sorted(themes.items(), key=lambda x: -x[1]): print(f"  {k}: {v}")

done_files = [r for r in results if r.get('status') == 'done']
print(f"\n=== 已done但未归档 ===")
for r in done_files: print(f"  {r['file']}")

empty_files = [r for r in results if r.get('empty')]
print(f"\n=== 空文件 ===")
for r in empty_files: print(f"  {r['file']}")

big_files = sorted([r for r in results if r.get('total_lines', 0) > 500], key=lambda x: -x.get('total_lines', 0))
print(f"\n=== 大文件（>500行） ===")
for r in big_files: print(f"  {r['file']} ({r['total_lines']}行, {r.get('turns','?')}轮)")

small_files = [r for r in results if r.get('total_lines', 0) > 0 and r.get('total_lines', 0) < 30]
print(f"\n=== 极短文件（<30行） ===")
for r in small_files: print(f"  {r['file']} ({r['total_lines']}行)")
