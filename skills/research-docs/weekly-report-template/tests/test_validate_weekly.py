from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
SPEC = importlib.util.spec_from_file_location("validate_weekly", ROOT / "scripts" / "validate_weekly.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class WeeklyValidatorTest(unittest.TestCase):
    def test_valid_report(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12-weekly-summary.md"
        self.assertEqual(MODULE.validate(report), [])

    def test_rejects_report_repository_and_ambiguous_author_scope(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12-daily-report-weekly-summary.md"
        errors = MODULE.validate(report)
        self.assertTrue(any("daily-report" in error for error in errors))
        self.assertTrue(any("他人提交" in error for error in errors))

    def test_rejects_hyphen_only_filename_suffix(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12----weekly-summary.md"
        errors = MODULE.validate(report)
        self.assertTrue(any("文件名" in error for error in errors))

    def test_cli_works_outside_skill_directory(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12-weekly-summary.md"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_weekly.py"), str(report)],
            cwd=Path("/Users/zhici/work-pro/daily-report"),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_empty_workflow_and_noncontinuous_markers(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12-broken-weekly-summary.md"
        errors = MODULE.validate(report)
        self.assertTrue(any("字母列表" in error for error in errors))
        self.assertTrue(any("工作流为空" in error for error in errors))
        self.assertTrue(any("Unicode" in error for error in errors))

    def test_skill_requires_author_filter_and_hash_deduplication(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("--author=", skill)
        self.assertIn("deduplicate by commit hash", skill)
        self.assertIn("Do not treat commits from other authors", skill)
        self.assertIn("Never select the `daily-report` repository", skill)


if __name__ == "__main__":
    unittest.main()
