from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
SPEC = importlib.util.spec_from_file_location("validate_biweekly", ROOT / "scripts" / "validate_biweekly.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def validate(name: str, *, mode: str = "personal", source_names: tuple[str, ...] = ()) -> list[str]:
    return MODULE.validate(
        FIXTURES / name,
        mode,
        [FIXTURES / source for source in source_names],
        None,
        False,
        False,
    )


class BiweeklyValidatorTest(unittest.TestCase):
    sources = (
        "2026-07-01-to-2026-07-07-weekly-summary.md",
        "2026-07-08-to-2026-07-14-weekly-summary.md",
    )

    def test_valid_personal_report_and_continuous_sources(self) -> None:
        self.assertEqual(validate("2026-07-01-to-2026-07-14-biweekly-summary.md", source_names=self.sources), [])

    def test_valid_portfolio_and_module_modes(self) -> None:
        portfolio = validate(
            "2026-07-01-to-2026-07-14-project-biweekly-summary.md",
            mode="portfolio",
            source_names=self.sources,
        )
        module = validate(
            "2026-07-01-to-2026-07-14-valid-module-biweekly-summary.md",
            mode="module",
            source_names=self.sources,
        )
        self.assertEqual(portfolio, [])
        self.assertEqual(module, [])

    def test_nonstandard_period_requires_explicit_override(self) -> None:
        report = FIXTURES / "2026-07-01-to-2026-07-11-biweekly-summary.md"
        sources = [
            FIXTURES / "2026-07-01-to-2026-07-07-weekly-summary.md",
            FIXTURES / "2026-07-08-to-2026-07-11-weekly-summary.md",
        ]
        errors = MODULE.validate(report, "personal", sources, None, False, False)
        allowed = MODULE.validate(report, "personal", sources, None, True, False)
        self.assertTrue(any("14 天" in error for error in errors))
        self.assertEqual(allowed, [])

    def test_requires_exactly_two_valid_sources(self) -> None:
        report = FIXTURES / "2026-07-01-to-2026-07-14-biweekly-summary.md"
        missing = MODULE.validate(report, "personal", [], None, False, False)
        nonexistent = MODULE.validate(
            report,
            "personal",
            [FIXTURES / self.sources[0], FIXTURES / "missing-weekly-summary.md"],
            None,
            False,
            False,
        )
        self.assertTrue(any("恰好两份有效" in error for error in missing))
        self.assertTrue(any("来源文件不存在" in error for error in nonexistent))

    def test_rejects_overlapping_and_gapped_sources(self) -> None:
        overlap = validate(
            "2026-07-01-to-2026-07-14-biweekly-summary.md",
            source_names=(self.sources[0], "2026-07-07-to-2026-07-13-overlap-weekly-summary.md"),
        )
        gap = validate(
            "2026-07-01-to-2026-07-14-biweekly-summary.md",
            source_names=(self.sources[0], "2026-07-09-to-2026-07-15-gap-weekly-summary.md"),
        )
        self.assertTrue(any("重叠" in error for error in overlap))
        self.assertTrue(any("缺口" in error for error in gap))

    def test_rejects_unsubstantiated_status_upgrade(self) -> None:
        errors = validate("2026-07-01-to-2026-07-14-status-biweekly-summary.md", source_names=self.sources)
        self.assertTrue(any("已上线" in error for error in errors))
        self.assertTrue(any("已完成" in error for error in errors))

    def test_rejects_broken_lists_empty_workflow_and_unrequested_okr(self) -> None:
        errors = validate("2026-07-01-to-2026-07-14-broken-biweekly-summary.md", source_names=self.sources)
        self.assertTrue(any("字母列表" in error for error in errors))
        self.assertTrue(any("工作流为空" in error for error in errors))
        self.assertTrue(any("Unicode" in error for error in errors))
        self.assertTrue(any("OKR" in error for error in errors))

    def test_rejects_forbidden_module_heading(self) -> None:
        errors = validate(
            "2026-07-01-to-2026-07-14-module-biweekly-summary.md",
            mode="module",
            source_names=self.sources,
        )
        self.assertTrue(any("禁止" in error for error in errors))

    def test_rejects_empty_portfolio_fields_and_extra_heading(self) -> None:
        errors = validate(
            "2026-07-01-to-2026-07-14-empty-project-biweekly-summary.md",
            mode="portfolio",
            source_names=self.sources,
        )
        self.assertTrue(any("字段不能为空" in error for error in errors))
        self.assertTrue(any("至少一个非空列表项" in error for error in errors))
        self.assertTrue(any("不允许的标题" in error for error in errors))

    def test_rejects_empty_module_fields_and_lists(self) -> None:
        errors = validate(
            "2026-07-01-to-2026-07-14-empty-module-biweekly-summary.md",
            mode="module",
            source_names=self.sources,
        )
        self.assertTrue(any("字段不能为空" in error for error in errors))
        self.assertTrue(any("至少一个非空列表项" in error for error in errors))

    def test_rejects_hyphen_only_filename_suffix(self) -> None:
        errors = validate("2026-07-01-to-2026-07-14----biweekly-summary.md", source_names=self.sources)
        self.assertTrue(any("文件名" in error for error in errors))

    def test_cli_works_outside_skill_directory(self) -> None:
        report = FIXTURES / "2026-07-01-to-2026-07-14-biweekly-summary.md"
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_biweekly.py"),
                str(report),
                "--source",
                str(FIXTURES / self.sources[0]),
                "--source",
                str(FIXTURES / self.sources[1]),
            ],
            cwd=Path("/Users/zhici/work-pro/daily-report"),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_skill_keeps_status_and_okr_evidence_gates(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Do not promote `开发中`", skill)
        self.assertIn("only when the user explicitly asks for OKR alignment", skill)
        self.assertIn("ask one question", skill)


if __name__ == "__main__":
    unittest.main()
