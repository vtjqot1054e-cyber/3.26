const fs = require('fs');
const path = require('path');

function getFmValue(fm, key) {
  const lines = fm.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(new RegExp('^' + key + ':\\s*(.*)'));
    if (m) {
      const val = m[1].trim();
      if (val) return val.replace(/^"|"$/g, '');
      if (i + 1 < lines.length) {
        const next = lines[i + 1].match(/^\s+-\s+(.+)/);
        if (next) return next[1].trim().replace(/^"|"$/g, '');
      }
      return '';
    }
  }
  return '';
}

function sanitize(s) { return s.replace(/[:\\*?"<>|]/g, '-'); }

function replaceStatus(content, oldVal, newVal) {
  let r = content.replace(new RegExp('status:\\s*' + oldVal, 'i'), 'status: ' + newVal);
  if (r === content) r = content.replace(new RegExp('status:\\s*\\n\\s*-\\s*' + oldVal, 'i'), 'status: ' + newVal);
  return r;
}

const testFiles = [
  'e:\\----2\\vault\\数字分身\\待确认\\[待确认] 2026-03-20_11-51-54Z-用户审阅文件处理流程.md',
];

for (const filePath of testFiles) {
  console.log('=== Testing:', path.basename(filePath), '===');
  const content = fs.readFileSync(filePath, 'utf-8');
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) { console.log('NO frontmatter'); continue; }
  const fm = fmMatch[1];

  const status = getFmValue(fm, 'status').toLowerCase();
  console.log('status:', status);

  let archiveTitle = getFmValue(fm, 'archive_title');
  console.log('archive_title:', '[' + archiveTitle + ']');
  if (!archiveTitle || archiveTitle === '""') archiveTitle = getFmValue(fm, 'title');
  console.log('final title:', '[' + archiveTitle + ']');
  console.log('sanitized:', '[' + sanitize(archiveTitle) + ']');

  if (status === 'done' || status === 'cancelled') {
    const newStatus = status === 'done' ? 'archived' : 'deleted';
    const nc = replaceStatus(content, status, newStatus);
    console.log('replace OK:', nc.includes('status: ' + newStatus));
    console.log('first 200 of new content:', nc.slice(0, 200));
  } else {
    console.log('SKIP: status is', status);
  }
  console.log('');
}
