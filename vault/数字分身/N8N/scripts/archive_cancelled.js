const fs = require('fs');
const path = require('path');

const pendingDir = 'E:\\新建文件夹\\vault\\数字分身\\待确认';
const deleteDir = 'E:\\新建文件夹\\vault\\数字分身\\对话删除';

const allFiles = fs.readdirSync(pendingDir).filter(f => f.endsWith('.md'));
const results = [];

const now = new Date();
const ts = now.getFullYear() + '-' +
  String(now.getMonth()+1).padStart(2,'0') + '-' +
  String(now.getDate()).padStart(2,'0') + '-' +
  String(now.getHours()).padStart(2,'0') +
  String(now.getMinutes()).padStart(2,'0') +
  String(now.getSeconds()).padStart(2,'0');

for (const f of allFiles) {
  const src = path.join(pendingDir, f);
  let content = fs.readFileSync(src, 'utf-8');

  const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!fmMatch) continue;
  const fm = fmMatch[1];

  const isCancelled = /status:\s*cancelled/i.test(fm) ||
                      /status:\s*\n\s*-\s*cancelled/i.test(fm);
  if (!isCancelled) continue;

  const titleMatch = fm.match(/title:\s*["']?([^"'\n]+)/);
  let title = titleMatch ? titleMatch[1].trim() : 'untitled';
  title = title.replace(/[:\*\?"<>|]/g, '-');

  const newName = '[对话删除] ' + ts + '-' + title + '.md';

  content = content.replace(/status:\s*cancelled/i, 'status: deleted');
  content = content.replace(/status:\s*\n\s*-\s*cancelled/i, 'status: deleted');
  content = content.replace(/type:\s*待确认/i, 'type: 对话删除');

  const dest = path.join(deleteDir, newName);
  fs.writeFileSync(dest, content, 'utf-8');
  fs.unlinkSync(src);
  results.push(f + ' -> ' + newName);
}

console.log('已归档 ' + results.length + ' 个cancelled文件:');
results.forEach(r => console.log('  ' + r));
