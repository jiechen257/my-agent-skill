#!/usr/bin/env python3
"""Read-only structural and evidence-boundary validator for biweekly reports."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path


META_KEYS = ("周期", "范围", "统计口径", "来源", "使用技能")
PERSONAL_LABELS = ("双周进展概述", "双周进展明细", "下阶段里程碑", "下阶段计划明细")
PORTFOLIO_HEADINGS = ("双周总览", "项目/仓库总结", "双周推进索引", "下阶段优先级")
PROJECT_LABELS = ("双周进展概述", "双周进展明细", "下阶段里程碑", "下阶段计划明细")
ROMAN = ("ⅰ", "ⅱ", "ⅲ", "ⅳ", "ⅴ", "ⅵ", "ⅶ", "ⅷ", "ⅸ", "ⅹ")
STATUSES = ("开发中", "待提测", "已提测", "已上线", "已完成")
FILENAME_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})-to-(\d{4}-\d{2}-\d{2})"
    r"(?:-[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)?-biweekly-summary\.md$"
)


def _metadata(text: str, key: str, mode: str) -> str | None:
    if mode == "module":
        match = re.search(rf"^\*\*{re.escape(key)}：\*\*\s*(.*)$", text, re.MULTILINE)
    else:
        match = re.search(rf"^- {re.escape(key)}：(.*)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def _period_value(value: str | None) -> tuple[date, date] | None:
    if not value:
        return None
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2}) 至 (\d{4}-\d{2}-\d{2})", value)
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1)), date.fromisoformat(match.group(2))
    except ValueError:
        return None


def _source_period(path: Path) -> tuple[date, date] | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?:^- 周期：|^\*\*周期：\*\*\s*)(\d{4}-\d{2}-\d{2}) 至 (\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    if not match:
        match = re.match(r"(\d{4}-\d{2}-\d{2})-to-(\d{4}-\d{2}-\d{2})", path.name)
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1)), date.fromisoformat(match.group(2))
    except ValueError:
        return None


def _continuous_letters(markers: list[str]) -> bool:
    return markers == [chr(ord("a") + index) for index in range(len(markers))]


def _validate_personal(lines: list[str], errors: list[str]) -> None:
    nonempty = [line for line in lines if line.strip()]
    if not nonempty or not re.fullmatch(r"# .+双周报", nonempty[0]):
        errors.append("personal 模式首个非空行必须是 # <姓名>双周报")
    headings = [line for line in lines if re.match(r"^#{1,6}\s", line)]
    allowed = 2 if any(line == "## OKR 对齐补充" for line in headings) else 1
    if len(headings) != allowed or any(line not in (nonempty[0], "## OKR 对齐补充") for line in headings):
        errors.append("personal 模式除标题和获准的 OKR 附录外不得包含 Markdown 标题")

    body_limit = next((i for i, line in enumerate(lines) if line == "## OKR 对齐补充"), len(lines))
    all_top_numbers = [
        int(match.group(1))
        for line in lines[:body_limit]
        if (match := re.match(r"^(\d+)\.\s", line))
    ]
    if all_top_numbers != [1, 2, 3, 4]:
        errors.append("personal 正文不得包含四个固定章节之外的顶层数字列表")
    top = []
    for index, line in enumerate(lines):
        match = re.match(r"^(\d+)\.\s*([^：:]+)[：:]", line)
        if match:
            top.append((index, int(match.group(1)), match.group(2).strip()))
    if [number for _, number, _ in top] != [1, 2, 3, 4]:
        errors.append("personal 正文必须且只能连续使用 1. 到 4.")
        return
    if [label for _, _, label in top] != list(PERSONAL_LABELS):
        errors.append("personal 四个固定字段的名称或顺序不正确")
    for position in (0, 2):
        if not re.search(r"[：:]\s*\S", lines[top[position][0]]):
            errors.append(f"{PERSONAL_LABELS[position]} 不能为空")

    section_end = next((i for i, line in enumerate(lines[top[3][0] + 1 :], top[3][0] + 1) if line.startswith("## ")), len(lines))
    ranges = {2: (top[1][0] + 1, top[2][0]), 4: (top[3][0] + 1, section_end)}
    for section, (start, end) in ranges.items():
        letters = []
        for index in range(start, end):
            match = re.match(r"^  ([a-z])\.\s*(.*)$", lines[index])
            if match:
                letters.append((index, match.group(1), match.group(2).strip()))
        if not letters:
            errors.append(f"personal 第 {section} 节至少需要一个字母列表项")
            continue
        if not _continuous_letters([letter for _, letter, _ in letters]):
            errors.append(f"personal 第 {section} 节字母列表必须从 a. 开始连续编号")
        for _, letter, value in letters:
            if not value:
                errors.append(f"personal 第 {section} 节 {letter}. 条目不能为空")
        if section == 2:
            for item_index, (line_index, letter, _) in enumerate(letters):
                item_end = letters[item_index + 1][0] if item_index + 1 < len(letters) else end
                numerals = []
                for line in lines[line_index + 1 : item_end]:
                    match = re.match(r"^    ([ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹ])\.\s*(.*)$", line)
                    if match:
                        numerals.append((match.group(1), match.group(2).strip()))
                if not numerals:
                    errors.append(f"personal 第 2 节 {letter}. 工作流为空")
                elif [number for number, _ in numerals] != list(ROMAN[: len(numerals)]):
                    errors.append(f"personal 第 2 节 {letter}. 的罗马数字必须连续编号")
    if any(re.match(r"^\s+(?:[ivxIVX]+)\.\s", line) for line in lines):
        errors.append("罗马数字明细必须使用 Unicode ⅰ. / ⅱ.，不能使用 i. / ii.")


def _validate_fixed_fields(
    block_lines: list[str],
    errors: list[str],
    context: str,
) -> None:
    matches: dict[str, list[tuple[int, str]]] = {label: [] for label in PROJECT_LABELS}
    for index, line in enumerate(block_lines):
        for label in PROJECT_LABELS:
            match = re.fullmatch(rf"\*\*{re.escape(label)}：\*\*\s*(.*)", line)
            if match:
                matches[label].append((index, match.group(1).strip()))

    for label, occurrences in matches.items():
        if not occurrences:
            errors.append(f"{context} 缺少固定字段：{label}")
            continue
        if len(occurrences) > 1:
            errors.append(f"{context} 固定字段重复：{label}")
            continue

        index, inline_value = occurrences[0]
        if label in ("双周进展概述", "下阶段里程碑"):
            if not inline_value:
                errors.append(f"{context} 字段不能为空：{label}")
            continue

        following_indexes = [
            entries[0][0]
            for other_label, entries in matches.items()
            if other_label != label and len(entries) == 1 and entries[0][0] > index
        ]
        end = min(following_indexes, default=len(block_lines))
        list_items = [
            line
            for line in block_lines[index + 1 : end]
            if re.match(r"^\s*-\s+\S", line)
        ]
        if inline_value or not list_items:
            errors.append(f"{context} {label} 必须包含至少一个非空列表项")


def _validate_portfolio(lines: list[str], errors: list[str]) -> None:
    nonempty = [line for line in lines if line.strip()]
    if not nonempty or not re.fullmatch(r"# .+双周报", nonempty[0]):
        errors.append("portfolio 模式首个非空行必须是项目双周报标题")
    title_index = next((index for index, line in enumerate(lines) if line.strip()), -1)
    headings = [line[3:].strip() for line in lines if line.startswith("## ") and not line.startswith("### ")]
    core = [heading for heading in headings if heading != "OKR 对齐补充"]
    if core != list(PORTFOLIO_HEADINGS):
        errors.append("portfolio 模式的四个 ## 一级结构缺失或顺序不正确")
    if headings.count("OKR 对齐补充") > 1:
        errors.append("portfolio 模式最多允许一个 ## OKR 对齐补充")
    for index, line in enumerate(lines):
        if not re.match(r"^#{1,6}\s", line):
            continue
        if index == title_index or line in {f"## {heading}" for heading in PORTFOLIO_HEADINGS}:
            continue
        if line == "## OKR 对齐补充" or re.fullmatch(r"### 项目：\s*\S.*", line):
            continue
        errors.append(f"portfolio 模式包含不允许的标题：{line}")
    project_indexes = [index for index, line in enumerate(lines) if line.startswith("### 项目：")]
    if not project_indexes:
        errors.append("portfolio 模式至少需要一个 ### 项目： 小节")
    for item, start in enumerate(project_indexes):
        later_sections = [
            index
            for index in range(start + 1, len(lines))
            if lines[index].startswith("## ") or lines[index].startswith("### 项目：")
        ]
        end = min(later_sections, default=len(lines))
        _validate_fixed_fields(lines[start + 1 : end], errors, f"portfolio 项目 {lines[start][6:].strip()}")


def _validate_module(lines: list[str], errors: list[str]) -> None:
    headings = [line for line in lines if re.match(r"^#{1,6}\s", line)]
    if any(not line.startswith("#### ") or line.startswith("##### ") for line in headings):
        errors.append("module 模式禁止 # / ## / ###，且只允许 #### 模块标题")
    module_indexes = [index for index, line in enumerate(lines) if line.startswith("#### ")]
    if not module_indexes:
        errors.append("module 模式至少需要一个 #### 模块标题")
    for item, start in enumerate(module_indexes):
        end = module_indexes[item + 1] if item + 1 < len(module_indexes) else len(lines)
        if not lines[start][5:].strip():
            errors.append("module 模块标题不能为空")
        _validate_fixed_fields(lines[start + 1 : end], errors, f"module 模块 {lines[start][5:].strip()}")


def validate(
    path: Path,
    mode: str,
    sources: list[Path],
    okr_source: Path | None,
    allow_nonstandard_period: bool,
    allow_okr: bool,
) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"文件不存在：{path}"]
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    values = {key: _metadata(text, key, mode) for key in META_KEYS}
    for key, value in values.items():
        if not value:
            errors.append(f"缺少或为空的元信息：{key}")
    if values["使用技能"] and values["使用技能"] != "`biweekly-report-template`":
        errors.append("使用技能必须是 `biweekly-report-template`")

    report_period = _period_value(values["周期"])
    if values["周期"] and not report_period:
        errors.append("周期必须使用 YYYY-MM-DD 至 YYYY-MM-DD 的有效闭区间")
    elif report_period and report_period[0] > report_period[1]:
        errors.append("周期开始日期不能晚于结束日期")
    elif report_period and not allow_nonstandard_period and (report_period[1] - report_period[0]).days + 1 != 14:
        errors.append("默认双周周期必须为连续 14 天；显式非标准周期需传 --allow-nonstandard-period")

    filename = FILENAME_RE.fullmatch(path.name)
    if not filename:
        errors.append("文件名必须是 <start>-to-<end>[-mode-or-scope]-biweekly-summary.md")
    elif report_period:
        filename_period = (date.fromisoformat(filename.group(1)), date.fromisoformat(filename.group(2)))
        if filename_period != report_period:
            errors.append("文件名日期必须与周期元信息一致")

    if len(sources) != 2:
        errors.append("双周合并必须提供恰好两份有效周报 source")
    source_periods = []
    for source in sources:
        if not source.is_file():
            errors.append(f"来源文件不存在：{source}")
            continue
        period = _source_period(source)
        if not period:
            errors.append(f"无法解析来源周期：{source}")
        else:
            source_periods.append((period[0], period[1], source))
    if len(source_periods) == 2:
        source_periods.sort(key=lambda item: item[0])
        first, second = source_periods
        if second[0] <= first[1]:
            errors.append(f"来源周期重叠：{first[2].name} 与 {second[2].name}")
        elif second[0] != first[1] + timedelta(days=1):
            errors.append(f"来源周期存在缺口：{first[1] + timedelta(days=1)} 至 {second[0] - timedelta(days=1)}")
        union = (first[0], max(first[1], second[1]))
        if report_period and union != report_period:
            errors.append("报告周期必须等于两份来源周报的日期并集")

    body_text = "\n".join(
        line
        for line in lines
        if not re.match(r"^- (?:周期|范围|统计口径|来源|使用技能)：", line)
        and not re.match(r"^\*\*(?:周期|范围|统计口径|来源|使用技能)：\*\*", line)
    )
    reported_statuses = {status for status in STATUSES if status in body_text}
    if reported_statuses:
        if len(sources) == 2 and all(source.is_file() for source in sources):
            source_text = "\n".join(source.read_text(encoding="utf-8") for source in sources if source.is_file())
            for status in sorted(reported_statuses):
                if status not in source_text:
                    errors.append(f"来源材料未明确支持进度状态：{status}")

    has_okr = bool(re.search(r"OKR\s*对齐", text, re.IGNORECASE))
    if has_okr and not allow_okr:
        errors.append("OKR 对齐内容需要显式传入 --allow-okr")
    if allow_okr:
        if not okr_source or not okr_source.is_file():
            errors.append("允许 OKR 对齐时必须通过 --okr-source 提供有效文档")
        elif values["来源"] and okr_source.name not in values["来源"] and str(okr_source) not in values["来源"]:
            errors.append("OKR 文档必须写入来源元信息")

    if mode == "personal":
        _validate_personal(lines, errors)
    elif mode == "portfolio":
        _validate_portfolio(lines, errors)
    else:
        _validate_module(lines, errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="biweekly Markdown file to validate")
    parser.add_argument("--mode", choices=("personal", "portfolio", "module"), default="personal")
    parser.add_argument("--source", type=Path, action="append", default=[], help="weekly source; repeat twice")
    parser.add_argument("--okr-source", type=Path, help="OKR source used by an explicitly requested appendix")
    parser.add_argument("--allow-nonstandard-period", action="store_true")
    parser.add_argument("--allow-okr", action="store_true")
    args = parser.parse_args(argv)
    errors = validate(
        args.report,
        args.mode,
        args.source,
        args.okr_source,
        args.allow_nonstandard_period,
        args.allow_okr,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
