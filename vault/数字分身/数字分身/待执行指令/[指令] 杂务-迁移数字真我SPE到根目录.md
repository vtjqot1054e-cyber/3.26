---
type: 待执行指令
target: 杂务
status: done
created: 2026-03-23
from: 总顾问大脑-03
---

# 指令：迁移数字真我SPE历史到根目录

## 角色定位

你是杂务窗口。机械执行，不做判断。

## 任务描述

将 `vault\数字真我\.specstory\history\` 下的所有对话记录文件移动到根目录 `D:\数字分身2\.specstory\history\`。

## 具体步骤

1. 列出 `vault\数字真我\.specstory\history\` 下所有文件
2. 列出 `D:\数字分身2\.specstory\history\` 下所有文件
3. 对比去重——同名文件跳过，只移动新文件
4. 执行移动（Move-Item，不是Copy）
5. 移动完成后，删除 `vault\数字真我\.specstory\` 整个目录（已空）
6. 报告：移动了几个文件，跳过了几个重复

## 注意事项

- 同名文件不覆盖，跳过即可
- `vault\数字真我\.specstory\` 下还有 `statistics.json` 和 `.project.json`，这些不需要迁移，直接随目录删除
- 如果 `vault\数字真我\.specstory\history\` 下还有 `cli/` 子目录，也一并删除

## 相关路径

- 源：`D:\数字分身2\vault\数字真我\.specstory\history\`
- 目标：`D:\数字分身2\.specstory\history\`

---

## 杂务执行记录（2026-03-23）

- **移动**：5 个 `.md` 对话文件（源 `history\` 全部 → 根 `.specstory\history\`，`Move-Item`）  
  - `2026-03-20_06-38-11Z-数字真我启动.md`  
  - `2026-03-20_09-24-37Z-启动复盘大脑.md`  
  - `2026-03-20_11-41-24Z-用户审阅文件处理流程.md`  
  - `2026-03-20_11-51-54Z-用户审阅文件处理流程.md`  
  - `2026-03-23_04-07-30Z-数字真我启动-10.md`
- **跳过**：0（目标无同名）
- **删除**：已删除 `D:\数字分身2\vault\数字真我\.specstory\` 整目录（含 `statistics.json`、`.project.json`、`cli/config.toml`，未迁移）
