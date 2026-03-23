# B类 · 工程修复与管线设计

> 总顾问大脑-08复盘产出。数字真我-12审核通过（2026-03-23）。

---

## B24 · WF1空文件bug——去重时间戳格式不一致

**标签**：knowledge_engineering / WF1 / dedup_logic / pitfall_solution
**来源**：[待确认] 2026-03-22_10-07-34Z-总大脑08.md
**向量库ID**：B5-B1

WF1从对话删除/读排除名时strip后得到`YYYY-MM-DD-HHmmSS-slug`格式，而对话导出coreName是`YYYY-MM-DD_HH-MM-SSZ-slug`格式，匹配失败，WF1认为文件未处理再次生成空文件。修复：增加frontmatter title字段作为备用匹配键。教训：跨目录文件匹配不能只靠文件名，需要有语义层面的匹配键。

**证据**：行163-186（根因分析），行848（修复方案）

---

## B25 · SpecStory v1.0.0 Bug #196——同Session双版本

**标签**：knowledge_engineering / SpecStory / external_dependency / pitfall_solution
**来源**：[待确认] 2026-03-22_10-07-34Z-总大脑08.md
**向量库ID**：B5-B2

SpecStory v1.0.0起，每个Cursor session生成两个文件：NOSEC版（HH-MMZ，cursor标签，可能截断末尾消息）和SEC版（HH-MM-SSZ，cursoride标签，内容更完整）。官方已知Bug（Issue #196，2026-03-20报告，Open）。修复：WF1预清洗按session ID分组，只清洗SEC版。注意：初始判断"NOSEC版质量更好"是基于表象（slug更干净），实际SEC版内容更完整。

**证据**：行1383-1402（根因确认），行1430-1450（Issue #196）

---

## B26 · 管线物理隔离设计

**标签**：knowledge_architecture / pipeline_design / physical_isolation / folder_design
**来源**：[待确认] 2026-03-22_10-07-34Z-总大脑08.md
**向量库ID**：B5-B3

待确认/=用户地盘（WF1写，用户标注，WF3归档）。对话引子/=AI地盘（WF1写原文副本，数字真我写引子，SO4.6写报告，用户不碰，WF3不删）。物理隔离保证SO4.6不能看到用户标注，只能看引子+原文副本，确保复盘大脑独立性。

**证据**：行735-758，行982-1082（完整架构图）

---

## B27 · 窗口体系设计原则——实际使用态>组织理想态

**标签**：knowledge_architecture / window_system / design_principle
**来源**：[待确认] 2026-03-22_10-07-34Z-总大脑08.md
**向量库ID**：B5-B4

窗口数量应基于实际使用频率而非理想设计，提前设计的空窗口增加管理成本不产出价值。正确做法：等数据量/使用频率支撑时再分化，不预设。空窗口三种处理方式：废弃/冻结/待决。

**证据**：行528-556
