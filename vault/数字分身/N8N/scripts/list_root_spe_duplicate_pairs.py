"""
列出 E:\\----2\\.specstory\\history 中「同时存在带秒数与不带秒数」的配对，
仅不带秒数的文件可作为 WF1 副本文删除候选（须人工确认后再删）。

规则（与工程指令一致）：
- 带秒数：YYYY-MM-DD_HH-MM-SSZ-标题.md
- 不带秒数：YYYY-MM-DD_HH-MMZ-标题.md
- 仅当同一 (日期时间前缀, 标题后缀) 同时存在两种命名时，不带秒数版列入待删清单。
"""
from __future__ import annotations

import os
import re
import sys

RE_WITH_SEC = re.compile(
    r"^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})-(\d{2})Z-(.+\.md)$"
)
RE_WITHOUT_SEC = re.compile(r"^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})Z-(.+\.md)$")


def main() -> None:
    root = os.path.join("E:", os.sep, "----2", ".specstory", "history")
    if len(sys.argv) > 1:
        root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"错误：目录不存在 {root}")
        sys.exit(1)

    files = [f for f in os.listdir(root) if f.endswith(".md")]
    pairs: dict[tuple[str, str], dict[str, str | None]] = {}

    for f in files:
        m1 = RE_WITH_SEC.match(f)
        if m1:
            prefix, rest = m1.group(1), m1.group(3)
            key = (prefix, rest)
            e = pairs.setdefault(key, {"with": None, "without": None})
            e["with"] = f
        m2 = RE_WITHOUT_SEC.match(f)
        if m2:
            prefix, rest = m2.group(1), m2.group(2)
            key = (prefix, rest)
            e = pairs.setdefault(key, {"with": None, "without": None})
            e["without"] = f

    to_delete: list[str] = []
    for key, e in pairs.items():
        if e.get("with") and e.get("without"):
            to_delete.append(str(e["without"]))

    to_delete.sort()
    print(f"目录：{root}")
    print(f"配对可删（不带秒数且存在带秒数同名）：{len(to_delete)} 个")
    for name in to_delete:
        print(name)


if __name__ == "__main__":
    main()
