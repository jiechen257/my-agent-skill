#!/usr/bin/env python3
"""Read-only structural validator for weekly-report-template output."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


META_KEYS = ("周期", "范围", "统计口径", "来源", "使用技能")
TOP_LABELS = (
    "阶段目标",
    "数据看板 & 分析",
    "周进展",
    "遗留问题",
    "本周目标与计划",
)
ROMAN = ("ⅰ", "ⅱ", "ⅲ", "ⅳ", "ⅴ", "ⅵ", "ⅶ", "ⅷ", "ⅸ", "ⅹ")
COMPLETION_CLAIMS = (
    "已完成",
    "已上线",
    "已发布",
    "已推广",
    "已达标",
    "效果良好",
    "采用率提升",
    "质量提升",
    "稳定性提升",
    "异常率下降",
)
EVIDENCE_MARKERS = (
    "Git",
    "iTrace",
    "日志",
    "查询",
    "测试",
    "验证",
    "指标",
    "PV",
    "UV",
    "成功率",
    "异常率",
    "提交",
    "validator",
)
FILENAME_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})-to-(\d{4}-\d{2}-\d{2})"
    r"(?:-[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)?-weekly-summary\.md$"
)


def _metadata(text: str, key: str) -> str | None:
    match = re.search(rf"^- {re.escape(key)}：(.*)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def _period(value: str | None) -> tuple[date, date] | None:
    if not value:
        return None
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2}) 至 (\d{4}-\d{2}-\d{2})", value)
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1)), date.fromisoformat(match.group(2))
    except ValueError:
        return None


def _continuous_letters(markers: list[str]) -> bool:
    return markers == [chr(ord("a") + index) for index in range(len(markers))]


def _validate_body(lines: list[str], errors: list[str]) -> list[tuple[int, int, str]]:
    all_top_numbers = [int(match.group(1)) for line in lines if (match := re.match(r"^(\d+)\.\s", line))]
    if all_top_numbers != [1, 2, 3, 4, 5]:
        errors.append("正文不得包含四段式或其他顶层数字列表，必须连续使用 1. 到 5.")

    top: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = re.match(r"^(\d+)\.\s*([^：:]+?)\s*[：:](?:\s*.*)?$", line)
        if match:
            top.append((index, int(match.group(1)), match.group(2).strip()))

    if [number for _, number, _ in top] != [1, 2, 3, 4, 5]:
        errors.append("正文顶层必须且只能连续使用 1. 到 5.")
        return top
    if [label for _, _, label in top] != list(TOP_LABELS):
        errors.append("正文五个固定字段的名称或顺序不正确")

    section_ranges = {
        number: (top[position][0] + 1, top[position + 1][0] if position + 1 < len(top) else len(lines))
        for position, (_, number, _) in enumerate(top)
    }
    for section, (start, end) in section_ranges.items():
        letters: list[tuple[int, str, str]] = []
        for index in range(start, end):
            match = re.match(r"^  ([a-z])\.\s*(.*)$", lines[index])
            if match:
                letters.append((index, match.group(1), match.group(2).strip()))
            elif re.match(r"^\s+[a-z]\.\s", lines[index]):
                errors.append(f"第 {section} 节字母列表必须使用两个空格缩进")

        if not letters:
            errors.append(f"第 {section} 节至少需要一个字母列表项")
            continue
        if not _continuous_letters([letter for _, letter, _ in letters]):
            errors.append(f"第 {section} 节字母列表必须从 a. 开始连续编号")
        for item_index, (line_index, letter, value) in enumerate(letters):
            if not value:
                errors.append(f"第 {section} 节 {letter}. 条目不能为空")
            item_end = letters[item_index + 1][0] if item_index + 1 < len(letters) else end
            numerals: list[tuple[str, str]] = []
            for line in lines[line_index + 1 : item_end]:
                match = re.match(r"^    ([ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹ])\.\s*(.*)$", line)
                if match:
                    numerals.append((match.group(1), match.group(2).strip()))
                elif re.match(r"^\s+(?:[ivxIVX]+|[ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹ]+)\.\s", line):
                    errors.append(f"第 {section} 节 {letter}. 的明细必须使用四个空格和 Unicode 罗马数字")
            if numerals:
                if [value for value, _ in numerals] != list(ROMAN[: len(numerals)]):
                    errors.append(f"第 {section} 节 {letter}. 的罗马数字必须从 ⅰ. 开始连续编号")
                for numeral, detail in numerals:
                    if not detail:
                        errors.append(f"第 {section} 节 {letter}. 的 {numeral}. 明细不能为空")

    if any(re.match(r"^\s+(?:[ivxIVX]+)\.\s", line) for line in lines):
        errors.append("罗马数字明细必须使用 Unicode ⅰ. / ⅱ.，不能使用 i. / ii.")
    if any(re.match(r"^\s+-\s", line) for line in lines[top[0][0] :]):
        errors.append("正文必须使用规定的数字、字母和 Unicode 罗马数字标记，不能使用 -")
    return top


def _validate_completion_claims(lines: list[str], top: list[tuple[int, int, str]], errors: list[str]) -> None:
    if not top:
        return
    body_start = top[0][0]
    if any(
        any(claim in line for claim in COMPLETION_CLAIMS)
        and not any(marker in line for marker in EVIDENCE_MARKERS)
        for line in lines[body_start:]
    ):
        errors.append("完成性措辞必须在同一条目中带有 Git、日志、指标或验证等证据标记")


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"文件不存在：{path}"]
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    nonempty = [line for line in lines if line.strip()]

    if not nonempty or not re.fullmatch(r"# (?!.*双周报).+周报", nonempty[0]):
        errors.append("首个非空行必须是单周报标题 # <姓名>周报")
    headings = [line for line in lines if re.match(r"^#{1,6}\s", line)]
    if len(headings) != 1:
        errors.append("周报除文档标题外不得包含 Markdown 标题")

    values = {key: _metadata(text, key) for key in META_KEYS}
    for key, value in values.items():
        if not value:
            errors.append(f"缺少或为空的元信息：{key}")
    if values["使用技能"] and values["使用技能"] != "`weekly-report-template`":
        errors.append("使用技能必须是 `weekly-report-template`")
    if values["范围"] and "daily-report" in values["范围"].lower():
        errors.append("daily-report 不能作为默认业务范围")
    evidence_text = " ".join(filter(None, (values["统计口径"], values["来源"])))
    if "git" in evidence_text.lower() and values["统计口径"]:
        if "本人 Git 提交" not in values["统计口径"]:
            errors.append("使用 Git 证据时，统计口径必须明确写出“本人 Git 提交”")
        if re.search(r"他人|非本人|未按本人|未过滤|不区分作者|全部作者|混入", values["统计口径"]):
            errors.append("Git 统计口径包含他人提交或作者过滤冲突表述")

    report_period = _period(values["周期"])
    if values["周期"] and not report_period:
        errors.append("周期必须使用 YYYY-MM-DD 至 YYYY-MM-DD 的有效闭区间")
    elif report_period and report_period[0] > report_period[1]:
        errors.append("周期开始日期不能晚于结束日期")

    filename = FILENAME_RE.fullmatch(path.name)
    if not filename:
        errors.append("文件名必须是 <start>-to-<end>[-scope]-weekly-summary.md")
    elif report_period:
        filename_period = (date.fromisoformat(filename.group(1)), date.fromisoformat(filename.group(2)))
        if filename_period != report_period:
            errors.append("文件名日期必须与周期元信息一致")

    top = _validate_body(lines, errors)
    _validate_completion_claims(lines, top, errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="weekly Markdown file to validate")
    args = parser.parse_args(argv)
    errors = validate(args.report)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
