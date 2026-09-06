from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_m3_spec", ROOT / "tools" / "validate_m3_spec.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class M3SpecTests(unittest.TestCase):
    def test_registry_and_collaboration_contract(self) -> None:
        self.assertEqual([], MODULE.validate())

    def test_a18_requires_more_than_pr_url(self) -> None:
        text = (MODULE.SPEC / "guides" / "collaboration-entry.md").read_text(encoding="utf-8")
        self.assertIn("只有 `pr_url` 时，G3 不得标记完成", text)
        self.assertIn("实际 review 结论", text)
        self.assertIn("已通过的 check/CI 结论", text)


if __name__ == "__main__":
    unittest.main()
