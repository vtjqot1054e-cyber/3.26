const fs = require('fs');
const path = require('path');

const filePath = 'e:\\----2\\vault\\数字分身\\待确认\\[待确认] 2026-01-26_03-42-36Z-重启.md';
const content = fs.readFileSync(filePath, 'utf-8');

const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
const frontmatter = fmMatch ? fmMatch[1] : '';

console.log('=== frontmatter ===');
console.log(JSON.stringify(frontmatter));
console.log('');

const isDone = /status:\s*done/i.test(frontmatter) || /status:\s*\n\s*-\s*done/i.test(frontmatter);
const isCancelled = /status:\s*cancelled/i.test(frontmatter) || /status:\s*\n\s*-\s*cancelled/i.test(frontmatter);

console.log('isDone:', isDone);
console.log('isCancelled:', isCancelled);

if (!isDone && !isCancelled) {
  console.log('>>> SKIPPED: neither done nor cancelled');
  process.exit(0);
}

if (isCancelled) {
  const titleMatch = frontmatter.match(/archive_title:\s*"?([^"\n]+)"?/);
  let archiveTitle = titleMatch ? titleMatch[1].trim().replace(/^"|"$/g, '') : '';
  console.log('archive_title raw match:', titleMatch);
  console.log('archiveTitle:', '[' + archiveTitle + ']');

  if (!archiveTitle || archiveTitle === '""') {
    const fallbackTitle = frontmatter.match(/title:\s*"?([^"\n]+)"?/);
    archiveTitle = fallbackTitle ? fallbackTitle[1].trim().replace(/^"|"$/g, '') : '';
    console.log('fallback title:', '[' + archiveTitle + ']');
  }

  // test replace
  let newContent = content
    .replace(/type:\s*待确认/, 'type: 对话删除')
    .replace(/status:\s*cancelled/i, 'status: deleted')
    .replace(/status:\s*\n\s*-\s*cancelled/i, 'status: deleted');

  console.log('');
  console.log('=== newContent first 300 chars ===');
  console.log(newContent.slice(0, 300));
}
