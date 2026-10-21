from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
SPEC = importlib.util.spec_from_file_location("validate_weekly", ROOT / "scripts" / "validate_weekly.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class WeeklyValidatorTest(unittest.TestCase):
    def test_combined_metrics_stay_in_main_table_with_comparison_and_analysis(self) -> None:
        text = (FIXTURES / "2026-07-06-to-2026-07-12-weekly-summary.md").read_text(encoding="utf-8")
        text = text.replace("- 范围：产物预览与反馈体验", "- 范围：产物链路与商业会员")
        table = (
            "| 模块 | 目标值 | 当前达成（上期 → 本期） | 环比变化 | 分析 |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| 产物链路 - 流量 | — | 示例上期 → 本期 | +1% | 示例分析 |\n"
            "| 商业会员 - 流量 | — | 示例上期 → 本期 | +1% | 示例分析 |\n"
            "| 商业会员 - 转换率 | — | 示例上期 → 本期 | +0.1pt | 阶段 UV 比值 |"
        )
        cases = {
            "complete": (table, True),
            "prose_only": (table.split("| 商业会员 - 流量")[0] + "\n\n  b. 商业会员流量与转换率见说明。", False),
            "separate_table": (table.replace("| 商业会员 - 流量", "\n\n" + "\n".join(table.splitlines()[:2]) + "\n| 商业会员 - 流量"), False),
            "missing_conversion": ("\n".join(table.splitlines()[:-1]), False),
            "missing_change": (table.replace("+0.1pt", ""), False),
            "missing_analysis": (table.replace("阶段 UV 比值", ""), False),
            "explicit_gap": (table.replace("示例上期 → 本期", "数据暂缺，等待补取").replace("+1%", "基线暂缺"), True),
        }
        with tempfile.TemporaryDirectory(prefix="report-main-table-") as directory:
            report = Path(directory) / "2026-07-06-to-2026-07-12-weekly-summary.md"
            for name, (content, valid) in cases.items():
                with self.subTest(name=name):
                    report.write_text(text.replace("3. 周进展：", "\n" + content + "\n\n3. 周进展："), encoding="utf-8")
                    errors = MODULE.validate(report)
                    if valid:
                        self.assertEqual(errors, [])
                    else:
                        self.assertTrue(any("主表" in error for error in errors), errors)

    def test_valid_report(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12-weekly-summary.md"
        self.assertEqual(MODULE.validate(report), [])

    def test_completion_claim_accepts_trace_evidence_and_rejects_missing_evidence(self) -> None:
        text = (FIXTURES / "2026-07-06-to-2026-07-12-weekly-summary.md").read_text(encoding="utf-8")
        original = "通过 Git 提交和日志验证整理预览路径与反馈体验的证据。"
        with tempfile.TemporaryDirectory(prefix="report-evidence-") as directory:
            report = Path(directory) / "2026-07-06-to-2026-07-12-weekly-summary.md"
            for evidence in ("OpenTrace", "通用观测", ""):
                with self.subTest(evidence=evidence):
                    claim = f"已完成示例草稿，依据 {evidence} 记录。" if evidence else "已完成示例草稿。"
                    report.write_text(text.replace(original, claim), encoding="utf-8")
                    errors = MODULE.validate(report)
                    if evidence:
                        self.assertEqual(errors, [])
                    else:
                        self.assertTrue(any("完成性措辞" in error for error in errors))

    def test_rejects_report_repository_and_ambiguous_author_scope(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12-daily-report-weekly-summary.md"
        errors = MODULE.validate(report)
        self.assertTrue(any("daily-report" in error for error in errors))
        self.assertTrue(any("他人提交" in error for error in errors))

    def test_rejects_hyphen_only_filename_suffix(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12----weekly-summary.md"
        errors = MODULE.validate(report)
        self.assertTrue(any("文件名" in error for error in errors))

    def test_rejects_legacy_four_section_format(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12-legacy-weekly-summary.md"
        errors = MODULE.validate(report)
        self.assertTrue(any("四段式" in error or "1. 到 5." in error for error in errors))

    def test_rejects_period_filename_mismatch(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-13-weekly-summary.md"
        errors = MODULE.validate(report)
        self.assertTrue(any("文件名日期" in error for error in errors))

    def test_cli_works_outside_skill_directory(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12-weekly-summary.md"
        with tempfile.TemporaryDirectory(prefix="report-validator-") as outside_dir:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "validate_weekly.py"), str(report)],
                cwd=Path(outside_dir),
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_empty_workflow_and_noncontinuous_markers(self) -> None:
        report = FIXTURES / "2026-07-06-to-2026-07-12-broken-weekly-summary.md"
        errors = MODULE.validate(report)
        self.assertTrue(any("字母列表" in error for error in errors))
        self.assertTrue(any("不能为空" in error for error in errors))
        self.assertTrue(any("Unicode" in error for error in errors))
        self.assertTrue(any("完成性措辞" in error for error in errors))

    def test_skill_requires_author_filter_and_hash_deduplication(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("--author=", skill)
        self.assertIn("deduplicate by commit hash", skill)
        self.assertIn("Do not treat commits from other authors", skill)
        self.assertIn("Never select the `daily-report` repository", skill)

    def test_skill_separates_metrics_from_delivered_and_planned_work(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        weekly_format = (ROOT / "references" / "weekly-format.md").read_text(encoding="utf-8")
        self.assertIn("A metric movement, log-query result, or problem discovery is not a delivered work item", skill)
        self.assertIn("Every item must contain an object, an action, and a verifiable result", skill)
        self.assertIn("上周具体做成了什么", weekly_format)
        self.assertIn("本周具体要做什么", weekly_format)


if __name__ == "__main__":
    unittest.main()
