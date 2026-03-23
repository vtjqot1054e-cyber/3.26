/**
 * WF1/WF2/WF3：在解析后的 jsCode 中替换 vaultPath
 * 已执行（家里）：OLD_LINE → NEW_LINE（见下）
 * 公司机器：把 NEW_LINE 改为
 *   "const vaultPath = 'D:\\\\数字分身2\\\\vault\\\\数字分身';"
 * 后重新 node 本脚本（或手工在 n8n 里替换）
 */
const fs = require('fs');
const path = require('path');

const files = [
  '01-A对话清洗标注.json',
  '02-用户校对提炼.json',
  '03-用户校对归档.json',
];

// 与 JSON.parse 后的 jsCode 内整行完全一致（见 node 调试 JSON.stringify(line)）
const OLD_LINE = "const vaultPath = 'D:\\\\数字分身2\\\\数字分身';";
const NEW_LINE = "const vaultPath = 'E:\\\\----2\\\\vault\\\\数字分身';";

for (const name of files) {
  const fp = path.join(__dirname, name);
  const j = JSON.parse(fs.readFileSync(fp, 'utf8'));
  let n = 0;
  for (const node of j.nodes) {
    const p = node.parameters;
    if (!p || typeof p.jsCode !== 'string') continue;
    const before = p.jsCode;
    if (!before.includes(OLD_LINE)) continue;
    p.jsCode = before.split(OLD_LINE).join(NEW_LINE);
    n += before.split(OLD_LINE).length - 1;
  }
  if (n === 0) {
    console.error('未替换任何节点:', name);
    process.exit(1);
  }
  fs.writeFileSync(fp, JSON.stringify(j, null, 2) + '\n', 'utf8');
  console.log(name, '→', n, '处 vaultPath');
}
