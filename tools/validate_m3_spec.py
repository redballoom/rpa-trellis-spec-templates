from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "marketplace" / "specs" / "rpa-python-shadowbot"


def require_text(path: Path, fragments: list[str], errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for fragment in fragments:
        if fragment not in text:
            errors.append(f"{path.relative_to(ROOT)} missing: {fragment}")


def validate_links(errors: list[str]) -> None:
    for path in SPEC.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "#")):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)} has broken link: {target}")


def validate() -> list[str]:
    errors: list[str] = []
    root_index = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
    marketplace_index = json.loads((ROOT / "marketplace" / "index.json").read_text(encoding="utf-8"))
    if root_index != marketplace_index:
        errors.append("index.json and marketplace/index.json differ")

    entry = SPEC / "guides" / "collaboration-entry.md"
    require_text(
        entry,
        [
            "三次主要确认",
            "正式 Task start",
            "active-task preflight",
            "require_pr=true",
            "实际 review 结论",
            "check/CI",
            "evidence-check --summary evidence/runs/{run_id}.summary.json",
            "archive-check",
            "Task 保存指针和工程结论，不复制 Gate 快照",
            "不能宣称 Trellis CLI 自身已经强制这些规则",
        ],
        errors,
    )
    require_text(
        SPEC / "guides" / "local-progress-tracking.md",
        ["accepted_baseline", "gate-history.md#<event-id>", "evidence/runs/{run_id}.summary.json"],
        errors,
    )
    require_text(
        SPEC / "backend" / "testing-and-delivery.md",
        ["PR 必须在 G3 acceptance 前真实存在", "actual review result", "passed check/CI evidence"],
        errors,
    )
    validate_links(errors)
    return errors


if __name__ == "__main__":
    failures = validate()
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        sys.exit(1)
    print("M3 spec validation passed")
