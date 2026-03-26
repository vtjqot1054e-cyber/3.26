// 单次执行：修改下方 FILES 后 node 本文件
const fs = require('fs');
const path = require('path');

const pendingDir = 'e:\\新建文件夹\\vault\\数字分身\\待确认';
const deleteDir = 'e:\\新建文件夹\\vault\\数字分身\\对话删除';

const FILES = [
  '[待确认] 2026-03-19_06-52Z-annotation-guidelines-for-skill-md.md',
  '[待确认] 2026-03-18_13-31-32Z-wf1-workflow-output-verification.md',
  '[待确认] 2026-03-18_13-08Z-提取助手01-松-6.md',
];

function sanitizeFileName(name) {
  return name.replace(/[<>:"/\\|?*]/g, '-');
}

function patchFrontmatter(fm) {
  let s = fm;
  s = s.replace(/^type:\s*.*$/m, 'type: 对话删除');
  s = s.replace(/status:\s*\r?\n(?:\s*-\s*[^\r\n]+\r?\n?)+/m, 'status: deleted\n');
  s = s.replace(/^status:\s*[^\r\n]+/m, 'status: deleted');
  return s;
}

if (!fs.existsSync(deleteDir)) fs.mkdirSync(deleteDir, { recursive: true });

const now = new Date();
const ts =
  now.getFullYear() +
  '-' +
  String(now.getMonth() + 1).padStart(2, '0') +
  '-' +
  String(now.getDate()).padStart(2, '0') +
  '-' +
  String(now.getHours()).padStart(2, '0') +
  String(now.getMinutes()).padStart(2, '0') +
  String(now.getSeconds()).padStart(2, '0');

FILES.forEach((f, idx) => {
  const src = path.join(pendingDir, f);
  const content = fs.readFileSync(src, 'utf-8');
  const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!fmMatch) throw new Error(f + ': 无 frontmatter');
  const newFm = patchFrontmatter(fmMatch[1]);
  const newContent = content.replace(/^---\r?\n[\s\S]*?\r?\n---/, '---\r\n' + newFm + '\r\n---');
  const titleLine = newFm.match(/^title:\s*["']?([^"'\r\n]+)/m);
  let title = titleLine ? titleLine[1].trim() : f.replace(/^\[待确认\]\s*/i, '').replace(/\.md$/i, '');
  title = sanitizeFileName(title) || 'untitled';
  const destName = `[对话删除] ${ts}-${String(idx + 1).padStart(2, '0')}-${title}.md`;
  fs.writeFileSync(path.join(deleteDir, destName), newContent, 'utf-8');
  fs.unlinkSync(src);
  console.log(f + ' -> ' + destName);
});
