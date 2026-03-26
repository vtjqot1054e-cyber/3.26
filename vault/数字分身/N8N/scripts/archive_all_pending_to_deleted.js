/**
 * 将待确认目录下全部 .md 迁移至对话删除（用户指令：全部删除归档）
 * 与 WF3 cancelled 分支一致：type→对话删除，status→deleted
 */
const fs = require('fs');
const path = require('path');

const pendingDir = 'e:\\新建文件夹\\vault\\数字分身\\待确认';
const deleteDir = 'e:\\新建文件夹\\vault\\数字分身\\对话删除';

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

function main() {
  if (!fs.existsSync(deleteDir)) fs.mkdirSync(deleteDir, { recursive: true });

  const names = fs.readdirSync(pendingDir).filter((f) => f.endsWith('.md'));
  const now = new Date();
  const batch =
    now.getFullYear() +
    '-' +
    String(now.getMonth() + 1).padStart(2, '0') +
    '-' +
    String(now.getDate()).padStart(2, '0') +
    '-' +
    String(now.getHours()).padStart(2, '0') +
    String(now.getMinutes()).padStart(2, '0') +
    String(now.getSeconds()).padStart(2, '0');

  const results = [];
  let errors = [];

  names.forEach((f, idx) => {
    const src = path.join(pendingDir, f);
    let content;
    try {
      content = fs.readFileSync(src, 'utf-8');
    } catch (e) {
      errors.push(f + ': read ' + e.message);
      return;
    }

    const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!fmMatch) {
      const base = sanitizeFileName(f.replace(/\.md$/i, ''));
      const destName = `[对话删除] ${batch}-${String(idx + 1).padStart(3, '0')}-${base}.md`;
      try {
        fs.writeFileSync(path.join(deleteDir, destName), content, 'utf-8');
        fs.unlinkSync(src);
        results.push(f + ' -> ' + destName + ' (无frontmatter，原样迁移)');
      } catch (e) {
        errors.push(f + ': ' + e.message);
      }
      return;
    }

    const newFm = patchFrontmatter(fmMatch[1]);
    const newContent = content.replace(/^---\r?\n[\s\S]*?\r?\n---/, '---\r\n' + newFm + '\r\n---');

    const titleLine = newFm.match(/^title:\s*["']?([^"'\r\n]+)/m);
    let title = titleLine ? titleLine[1].trim() : f.replace(/^\[待确认\]\s*/i, '').replace(/\.md$/i, '');
    title = sanitizeFileName(title) || 'untitled';

    const destName = `[对话删除] ${batch}-${String(idx + 1).padStart(3, '0')}-${title}.md`;

    try {
      fs.writeFileSync(path.join(deleteDir, destName), newContent, 'utf-8');
      fs.unlinkSync(src);
      results.push(f + ' -> ' + destName);
    } catch (e) {
      errors.push(f + ': ' + e.message);
    }
  });

  console.log('已迁移 ' + results.length + ' 个文件到对话删除：');
  results.forEach((r) => console.log('  ' + r));
  if (errors.length) {
    console.log('\n错误 ' + errors.length + ' 个：');
    errors.forEach((e) => console.log('  ' + e));
    process.exit(1);
  }
}

main();
