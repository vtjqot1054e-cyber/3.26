/**
 * 回滚 archive_all_pending_to_deleted.js（批次 2026-03-25-222556）
 * 从 对话删除 迁回 待确认，恢复文件名与 type:待确认；status 统一为 pending（原值已无法恢复）
 */
const fs = require('fs');
const path = require('path');

const deleteDir = 'e:\\新建文件夹\\vault\\数字分身\\对话删除';
const pendingDir = 'e:\\新建文件夹\\vault\\数字分身\\待确认';

/** 序号 1..88 对应当时 readdir 顺序（与归档日志一致） */
const ORIGINAL_BY_INDEX = [
  '[待确认] 2026-01-26_03-42-36Z-重启.md',
  '[待确认] 2026-03-02_10-47-32Z.md',
  '[待确认] 2026-03-04_06-20-53Z.md',
  '[待确认] 2026-03-07_06-42-50Z.md',
  '[待确认] 2026-03-07_07-39-10Z-dify.md',
  '[待确认] 2026-03-07_08-01-45Z.md',
  '[待确认] 2026-03-07_08-23-47Z-1-exit-and-fix.md',
  '[待确认] 2026-03-07_08-56-32Z-1-exit-and-fix.md',
  '[待确认] 2026-03-07_08-58-36Z.md',
  '[待确认] 2026-03-07_09-53-27Z.md',
  '[待确认] 2026-03-09_06-20-25Z.md',
  '[待确认] 2026-03-09_06-45-03Z-ran-1-stop-hook.md',
  '[待确认] 2026-03-09_07-02-17Z.md',
  '[待确认] 2026-03-09_15-19-05Z.md',
  '[待确认] 2026-03-09_15-26-59Z.md',
  '[待确认] 2026-03-09_15-34-00Z.md',
  '[待确认] 2026-03-09_15-43-20Z.md',
  '[待确认] 2026-03-10_03-58-25Z-updates-to-consumer-terms.md',
  '[待确认] 2026-03-11_08-02-14Z.md',
  '[待确认] 2026-03-11_08-13-46Z-333.md',
  '[待确认] 2026-03-11_08-14-18Z.md',
  '[待确认] 2026-03-11_10-16-18Z-在不在.md',
  '[待确认] 2026-03-11_10-24-12Z-聚合平台api集成模型讨论.md',
  '[待确认] 2026-03-11_14-50Z-model-identification-and-documentation-review-1.md',
  '[待确认] 2026-03-12_04-38-36Z-ai回复与流程简化.md',
  '[待确认] 2026-03-12_06-30-55Z-font-subscription-billing-issue.md',
  '[待确认] 2026-03-12_06-42-49Z-项目完整性和健康状况检查.md',
  '[待确认] 2026-03-12_11-32-00Z-n8n-workflow-configuration.md',
  '[待确认] 2026-03-13_04-58-15Z-2026年对话记录全量监控开源项目.md',
  '[待确认] 2026-03-13_05-11-02Z-文件搜索和关键词匹配.md',
  '[待确认] 2026-03-13_06-11-31Z-file-comparison-between-directories.md',
  '[待确认] 2026-03-13_06-59-55Z-新窗口任务和完成情况.md',
  '[待确认] 2026-03-13_12-30-46Z-n8n-data-cleaning-for-specstory.md',
  '[待确认] 2026-03-13_16-29Z-回家测试系统.md',
  '[待确认] 2026-03-13_18-22Z-march-14-home-plans.md',
  '[待确认] 2026-03-14_01-50Z-cuosor-api-call-support-1.md',
  '[待确认] 2026-03-14_01-50Z-cuosor-api-call-support.md',
  '[待确认] 2026-03-14_07-33Z-大脑01opus-4-6.md',
  '[待确认] 2026-03-14_09-34Z-胜率01opus-4-6-max.md',
  '[待确认] 2026-03-14_09-39Z-窗口体系功能启动.md',
  '[待确认] 2026-03-14_10-14Z-大脑02opus-4-6.md',
  '[待确认] 2026-03-14_10-36Z-架构师-sk匹配4-6.md',
  '[待确认] 2026-03-14_10-39Z-agent-self-improvement-and-reflection-skills.md',
  '[待确认] 2026-03-14_10-39Z-agent-skills-for-knowledge-and-session-management.md',
  '[待确认] 2026-03-14_10-39Z-multi-agent-orchestration-skills-search.md',
  '[待确认] 2026-03-14_10-39Z-决策追踪类技能搜索.md',
  '[待确认] 2026-03-14_10-43Z-agent-skill-security-review.md',
  '[待确认] 2026-03-14_10-43Z-agent-skill-security-review-1.md',
  '[待确认] 2026-03-14_10-43Z-agent-skill-security-review-2.md',
  '[待确认] 2026-03-14_10-43Z-agent-skill-security-review-3.md',
  '[待确认] 2026-03-14_10-47Z-杂务窗口处理规则.md',
  '[待确认] 2026-03-14_10-52Z-工程01-p1so4-6.md',
  '[待确认] 2026-03-14_11-02Z-n8n-workflow-execution-and-reporting.md',
  '[待确认] 2026-03-14_11-14Z-n8n-workflow-execution-and-output-collection.md',
  '[待确认] 2026-03-14_11-46Z-n8n-workflow-execution-and-output-collection.md',
  '[待确认] 2026-03-14_12-33Z-n8n-workflow-reconstruction-steps.md',
  '[待确认] 2026-03-14_12-37Z-大脑-03,opus-4-6.md',
  '[待确认] 2026-03-15_03-02Z-大脑-04-opus-4-6-max.md',
  '[待确认] 2026-03-15_03-53Z-复盘01-op4-6.md',
  '[待确认] 2026-03-15_06-17Z-cursor-auto-run-confirmation-settings.md',
  '[待确认] 2026-03-17_04-00Z-总顾问(大脑常驻层)4-6max.md',
  '[待确认] 2026-03-17_04-04-53Z-杂务.md',
  '[待确认] 2026-03-17_04-25-12Z-directory-structure-and-file-listing.md',
  '[待确认] 2026-03-17_04-25-15Z-文件内容汇总与更新日期.md',
  '[待确认] 2026-03-17_04-25-22Z-markdown-files-updated-dates-and-recent-modifications.md',
  '[待确认] 2026-03-17_06-00Z-复盘大脑op4-6.md',
  '[待确认] 2026-03-17_06-01Z-标注助手so4-6.md',
  '[待确认] 2026-03-17_06-02Z-信号助手so4-6.md',
  '[待确认] 2026-03-17_07-49Z-投标顾问op4-6max.md',
  '[待确认] 2026-03-17_09-34Z-总顾问02(大脑常驻层)4-6max.md',
  '[待确认] 2026-03-17_11-36Z-技术总工-01-op4-6.md',
  '[待确认] 2026-03-17_14-38Z-总顾问03(大脑常驻层)4-6max.md',
  '[待确认] 2026-03-18_11-13Z-数字真我系统评估任务.md',
  '[待确认] 2026-03-18_13-07Z-标注助手01-so4-6.md',
  '[待确认] 2026-03-18_13-08Z-提取助手01-松-6.md',
  '[待确认] 2026-03-18_13-31-32Z-wf1-workflow-output-verification.md',
  '[待确认] 2026-03-19_06-52Z-annotation-guidelines-for-skill-md.md',
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

function restoreFrontmatter(fm) {
  let s = fm;
  s = s.replace(/^type:\s*.*$/m, 'type: 待确认');
  s = s.replace(/status:\s*\r?\n(?:\s*-\s*[^\r\n]+\r?\n?)+/m, 'status: pending\n');
  s = s.replace(/^status:\s*[^\r\n]+/m, 'status: pending');
  return s;
}

function main() {
  if (!fs.existsSync(pendingDir)) fs.mkdirSync(pendingDir, { recursive: true });

  const files = fs.readdirSync(deleteDir).filter((f) => /\[对话删除\] 2026-03-25-222556-\d{3}-/.test(f));

  if (files.length !== ORIGINAL_BY_INDEX.length) {
    console.error('批次文件数异常：期望 ' + ORIGINAL_BY_INDEX.length + '，实际 ' + files.length);
    process.exit(1);
  }

  const results = [];
  const errors = [];

  for (const f of files) {
    const m = f.match(/222556-(\d{3})-/);
    if (!m) continue;
    const idx = parseInt(m[1], 10);
    const originalName = ORIGINAL_BY_INDEX[idx - 1];
    if (!originalName) {
      errors.push(f + ': 序号越界 ' + idx);
      continue;
    }

    const src = path.join(deleteDir, f);
    let content;
    try {
      content = fs.readFileSync(src, 'utf-8');
    } catch (e) {
      errors.push(f + ': ' + e.message);
      continue;
    }

    const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!fmMatch) {
      errors.push(f + ': 无 frontmatter');
      continue;
    }

    const newFm = restoreFrontmatter(fmMatch[1]);
    const newContent = content.replace(/^---\r?\n[\s\S]*?\r?\n---/, '---\r\n' + newFm + '\r\n---');
    const dest = path.join(pendingDir, originalName);

    try {
      fs.writeFileSync(dest, newContent, 'utf-8');
      fs.unlinkSync(src);
      results.push(f + ' -> ' + originalName);
    } catch (e) {
      errors.push(f + ': ' + e.message);
    }
  }

  console.log('已回滚 ' + results.length + ' 个文件到待确认：');
  results.forEach((r) => console.log('  ' + r));
  if (errors.length) {
    console.log('\n错误：');
    errors.forEach((e) => console.log('  ' + e));
    process.exit(1);
  }
}

main();
