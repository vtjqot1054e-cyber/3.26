/**
 * 将指定待确认文件列表迁移至 对话删除（type/ status 与 WF3 cancelled 一致）
 */
const fs = require('fs');
const path = require('path');

const pendingDir = 'e:\\新建文件夹\\vault\\数字分身\\待确认';
const deleteDir = 'e:\\新建文件夹\\vault\\数字分身\\对话删除';

const FILES = [
  '[待确认] 2026-03-19_12-05-06Z-技术总工窗口对话分析.md',
  '[待确认] 2026-03-19_12-13-42Z-复盘大脑文档分析.md',
  '[待确认] 2026-03-19_13-05-43Z-判断文件区段的知识价值.md',
  '[待确认] 2026-03-20_04-09-20Z-数字真我启动.md',
  '[待确认] 2026-03-20_07-27-08Z-阶段一任务复盘.md',
  '[待确认] 2026-03-20_07-33-08Z-数字分身路径适配vault前缀.md',
  '[待确认] 2026-03-20_09-24-37Z-启动复盘大脑.md',
  '[待确认] 2026-03-20_10-14-11Z-总控大脑启动.md',
  '[待确认] 2026-03-20_10-15-54Z-启动ob系统.md',
  '[待确认] 2026-03-20_11-41-24Z-用户审阅文件处理流程.md',
  '[待确认] 2026-03-20_11-51-54Z-用户审阅文件处理流程.md',
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

function main() {
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

  const results = [];
  const errors = [];

  FILES.forEach((f, idx) => {
    const src = path.join(pendingDir, f);
    if (!fs.existsSync(src)) {
      errors.push(f + ': 文件不存在');
      return;
    }

    let content;
    try {
      content = fs.readFileSync(src, 'utf-8');
    } catch (e) {
      errors.push(f + ': ' + e.message);
      return;
    }

    const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!fmMatch) {
      errors.push(f + ': 无 frontmatter');
      return;
    }

    const newFm = patchFrontmatter(fmMatch[1]);
    const newContent = content.replace(/^---\r?\n[\s\S]*?\r?\n---/, '---\r\n' + newFm + '\r\n---');

    const titleLine = newFm.match(/^title:\s*["']?([^"'\r\n]+)/m);
    let title = titleLine ? titleLine[1].trim() : f.replace(/^\[待确认\]\s*/i, '').replace(/\.md$/i, '');
    title = sanitizeFileName(title) || 'untitled';

    const destName = `[对话删除] ${ts}-${String(idx + 1).padStart(2, '0')}-${title}.md`;

    try {
      fs.writeFileSync(path.join(deleteDir, destName), newContent, 'utf-8');
      fs.unlinkSync(src);
      results.push(f + ' -> ' + destName);
    } catch (e) {
      errors.push(f + ': ' + e.message);
    }
  });

  console.log('已归档 ' + results.length + ' 个文件到对话删除：');
  results.forEach((r) => console.log('  ' + r));
  if (errors.length) {
    console.log('\n错误：');
    errors.forEach((e) => console.log('  ' + e));
    process.exit(1);
  }
}

main();
