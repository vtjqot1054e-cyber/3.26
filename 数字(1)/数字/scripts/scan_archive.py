import os, re

archive_dir = r"E:\数字\vault\数字分身\对话存档"
delete_dir = r"E:\数字\vault\数字分身\对话删除"

def scan_dir(d, label):
    results = []
    for fname in sorted(os.listdir(d)):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(d, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        if not content.strip():
            continue
        info = {"file": fname, "dir": label, "size": len(content), "lines": len(content.split('\n'))}
        fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            for key in ['title', 'turns', 'status']:
                m = re.search(rf'^{key}:\s*(.+)$', fm, re.MULTILINE)
                if m:
                    info[key] = m.group(1).strip().strip('"').strip("'")
        results.append(info)
    return results

archive = scan_dir(archive_dir, "存档")
deleted = scan_dir(delete_dir, "删除")

print(f"对话存档：{len(archive)}篇")
print(f"对话删除：{len(deleted)}篇")

print(f"\n=== 已归档（已走完管线）===")
for r in archive:
    print(f"  {r['file'][:60]}  ({r['lines']}行, {r.get('turns','?')}轮)")

print(f"\n=== 已删除 ===")
for r in deleted:
    print(f"  {r['file'][:60]}  ({r['lines']}行, {r.get('turns','?')}轮)")

total = len(archive) + len(deleted) + 108
print(f"\n=== 全量统计 ===")
print(f"  总对话数：{total}")
print(f"  已归档（done）：{len(archive)}")
print(f"  已删除（cancelled）：{len(deleted)}")
print(f"  待确认（pending）：108")
print(f"  管线处理率：{(len(archive)+len(deleted))/total*100:.1f}%")
print(f"  有效归档率：{len(archive)/total*100:.1f}%")
