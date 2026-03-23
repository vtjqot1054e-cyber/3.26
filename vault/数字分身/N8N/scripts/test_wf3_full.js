const fs = require('fs');
const path = require('path');
const vaultPath = 'E:\\----2\\vault\\数字分身';
const pendingDir = path.join(vaultPath, '待确认');
const archiveDir = path.join(vaultPath, '对话存档');
const deletedDir = path.join(vaultPath, '对话删除');

console.log('pendingDir:', pendingDir);
console.log('pendingDir exists:', fs.existsSync(pendingDir));
console.log('archiveDir:', archiveDir);
console.log('deletedDir:', deletedDir);

let files = [];
try { files = fs.readdirSync(pendingDir); } catch(e) { console.log('readdirSync error:', e.message); process.exit(1); }

const mdFiles = files.filter(f => f.endsWith('.md'));
console.log('Total md files:', mdFiles.length);

let done = 0, cancelled = 0;
let errors = [];
let skipped = 0;

for (const f of mdFiles) {
  const filePath = path.join(pendingDir, f);
  let content = '';
  try { content = fs.readFileSync(filePath, 'utf-8'); } catch(e) { continue; }

  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  const frontmatter = fmMatch ? fmMatch[1] : '';
  
  if (!fmMatch) {
    if (f.includes('重启')) console.log('>>> 重启文件: NO frontmatter match!');
    continue;
  }

  const isDone = /status:\s*done/i.test(frontmatter) || /status:\s*\n\s*-\s*done/i.test(frontmatter);
  const isCancelled = /status:\s*cancelled/i.test(frontmatter) || /status:\s*\n\s*-\s*cancelled/i.test(frontmatter);
  
  if (f.includes('重启')) {
    console.log('>>> 重启文件 frontmatter:', JSON.stringify(frontmatter.slice(0, 100)));
    console.log('>>> isDone:', isDone, 'isCancelled:', isCancelled);
  }

  if (!isDone && !isCancelled) { skipped++; continue; }

  try {
    if (isDone) {
      done++;
      if (f.includes('重启')) console.log('>>> 重启: would ARCHIVE');
    } else {
      cancelled++;
      if (f.includes('重启')) console.log('>>> 重启: would DELETE');
      
      const now2 = new Date();
      const timeStr2 = now2.getFullYear() + '-' +
        String(now2.getMonth()+1).padStart(2,'0') + '-' +
        String(now2.getDate()).padStart(2,'0') + '-' +
        String(now2.getHours()).padStart(2,'0') +
        String(now2.getMinutes()).padStart(2,'0') +
        String(now2.getSeconds()).padStart(2,'0');
      const titleMatch2 = frontmatter.match(/archive_title:\s*"?([^"\n]+)"?/);
      let archiveTitle2 = titleMatch2 ? titleMatch2[1].trim().replace(/^"|"$/g, '') : '';
      if (!archiveTitle2 || archiveTitle2 === '""') {
        const fallbackTitle2 = frontmatter.match(/title:\s*"?([^"\n]+)"?/);
        archiveTitle2 = fallbackTitle2 ? fallbackTitle2[1].trim().replace(/^"|"$/g, '') : '';
      }
      const suffix2 = archiveTitle2 ? '-' + archiveTitle2 : '';
      const deletedFileName = '[对话删除] ' + timeStr2 + suffix2 + '.md';
      
      if (f.includes('重启')) {
        console.log('>>> target path:', path.join(deletedDir, deletedFileName));
      }
    }
  } catch(e) {
    errors.push(f + ': ' + String(e).slice(0, 100));
  }
}

console.log('');
console.log('=== RESULT ===');
console.log('done:', done);
console.log('cancelled:', cancelled);
console.log('skipped (pending):', skipped);
console.log('errors:', errors);
