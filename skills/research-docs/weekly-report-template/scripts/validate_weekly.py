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
PERSONAL_TOP_LABELS = (
    "阶段目标",
    "业务 & 研发核心指标数据",
    "与 OKR 关联的目标进展",
    "周进展",
    "问题与风险",
    "周目标与计划",
)
PERSONAL_METRICS = ("Agent 任务交付成功率", "Query 分析问题回收情况", "无效工具调用比例")
PERSONAL_PROGRESS = ("录音纪要", "Query 抽检平台", "其他")
PERSONAL_PLANS = ("Query 分析与问题治理", "夸克会议纪要需求")
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
    "Trace",
    "观测",
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


def _validate_combined_metrics_table(
    lines: list[str], top: list[tuple[int, int, str]], scope: str, errors: list[str]
) -> None:
    if [number for _, number, _ in top] != [1, 2, 3, 4, 5]:
        return
    metrics = lines[top[1][0] + 1 : top[2][0]]
    context = scope + "\n" + "\n".join(metrics)
    if "产物" not in context or "商业会员" not in context:
        return
    table: list[list[str]] = []
    for line in metrics:
        if line.strip().startswith("|"):
            table.append([cell.strip() for cell in line.strip().strip("|").split("|")])
        elif table:
            break
    header = ["模块", "目标值", "当前达成（上期 → 本期）", "环比变化", "分析"]
    if not table or table[0] != header:
        errors.append("产物链路与商业会员必须使用包含上期、本期、环比变化和分析列的同一主表")
        return
    for label in ("产物链路 - 流量", "商业会员 - 流量", "商业会员 - 转换率"):
        row = next((row for row in table[2:] if row and row[0] == label), None)
        if row is None:
            errors.append(f"数据主表缺少 {label}，表后段落或其他表格不能替代")
        elif len(row) != 5 or any(not row[index] for index in (2, 3, 4)):
            errors.append(f"数据主表 {label} 必须保留上期/本期、环比变化和分析；暂缺时标明缺口")


def _validate_period_and_filename(path: Path, period: str | None, errors: list[str]) -> None:
    report_period = _period(period)
    if not report_period:
        errors.append("周期必须使用 YYYY-MM-DD 至 YYYY-MM-DD 的有效闭区间")
    elif report_period[0] > report_period[1]:
        errors.append("周期开始日期不能晚于结束日期")

    filename = FILENAME_RE.fullmatch(path.name)
    if not filename:
        errors.append("文件名必须是 <start>-to-<end>[-scope]-weekly-summary.md")
    elif period and period != f"{filename.group(1)} 至 {filename.group(2)}":
        errors.append("文件名日期必须与周期元信息一致")


def _table_rows(lines: list[str]) -> list[list[str]]:
    return [
        [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip()[1:-1])]
        for line in lines
        if line.strip().startswith("|") and line.strip().endswith("|")
    ]


def _check_data_rows(
    rows: list[list[str]], labels: tuple[str, ...], columns: int, section: str, errors: list[str],
) -> None:
    if len(rows) != len(labels) + 2 or any(
        len(row) != columns or not all(row) for row in rows
    ):
        errors.append(f"{section}必须保留完整表头及 {len(labels)} 行数据，缺失时标明缺口")
        return
    if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
        errors.append(f"{section}表格分隔行无效")
    names = [re.sub(r"[（(].*$", "", row[0].replace("**", "")).strip() for row in rows[2:]]
    if names != list(labels):
        errors.append(f"{section}的行名和顺序应为 {'、'.join(labels)}")


def _validate_personal(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    lines = text.splitlines()
    headings = [line for line in lines if re.match(r"^#{1,6}\s", line)]
    first_line = next((line for line in lines if line.strip()), "")
    if headings != [first_line] or not re.fullmatch(r"# 之瓷周报(?:｜.+)?", first_line):
        errors.append("个人周报应以 # 之瓷周报 开头，可用 ｜ 加主题")
    period = re.search(r"^\*\*统计周期：\*\*\s*(\d{4}-\d{2}-\d{2} 至 \d{4}-\d{2}-\d{2})", text, re.M)
    _validate_period_and_filename(path, period.group(1) if period else None, errors)

    top = [
        (i, number, label)
        for i, line in enumerate(lines)
        if (match := re.fullmatch(r"(\d+)\. \*\*(.+?)\*\*", line))
        for number, label in [match.groups()]
    ]
    expected = [(str(i), label) for i, label in enumerate(PERSONAL_TOP_LABELS, start=1)]
    if [(number, label) for _, number, label in top] != expected or sum(
        bool(re.match(r"^\d+\.\s", line)) for line in lines
    ) != len(expected):
        errors.append("个人周报必须依次包含六个章节：" + "、".join(PERSONAL_TOP_LABELS))
        return errors

    sections = {}
    for pos, (start, _, label) in enumerate(top):
        end = top[pos + 1][0] if pos + 1 < len(top) else len(lines)
        sections[label] = lines[start + 1:end]
        if not any(line.strip() for line in sections[label]):
            errors.append(f"{label}不能为空")

    metrics = _table_rows(sections["业务 & 研发核心指标数据"])
    if not metrics or metrics[0] != ["指标", "OKR 目标", "正式基线", "本期回收与分析"]:
        errors.append("指标表必须包含指标、OKR 目标、正式基线、本期回收与分析")
    _check_data_rows(metrics, PERSONAL_METRICS, 4, "指标表", errors)

    progress = sections["周进展"]
    groups = [
        (i, match.group(1), match.group(2))
        for i, line in enumerate(progress)
        if (match := re.match(r"^   (\d+)\. \*\*【([^】]+)】", line))
    ]
    if [(number, label) for _, number, label in groups] != [
        (str(i), label) for i, label in enumerate(PERSONAL_PROGRESS, start=1)
    ] or sum(bool(re.match(r"^   \d+\.\s", line)) for line in progress) != len(PERSONAL_PROGRESS):
        errors.append("周进展必须依次包含录音纪要、Query 抽检平台、其他")
    for pos, (start, _, label) in enumerate(groups):
        end = groups[pos + 1][0] if pos + 1 < len(groups) else len(progress)
        if not any(re.match(r"^      1\.\s+\S", line) for line in progress[start + 1:end]):
            errors.append(f"周进展中的{label}至少应有一条说明")

    plans = _table_rows(sections["周目标与计划"])
    if (
        not plans or len(plans[0]) != 3 or plans[0][0] != "核心目标"
        or not re.fullmatch(r"本周（\d{1,2} 月 \d{1,2} 日当周）", plans[0][1])
        or not re.fullmatch(r"下周（\d{1,2} 月 \d{1,2} 日当周）", plans[0][2])
    ):
        errors.append("计划表必须分为核心目标、本周（M 月 D 日当周）、下周（M 月 D 日当周）")
    _check_data_rows(plans, PERSONAL_PLANS, 3, "计划表", errors)
    return errors


def validate(path: Path, *, report_format: str = "personal") -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"文件不存在：{path}"]
    text = path.read_text(encoding="utf-8")
    if report_format == "personal":
        return _validate_personal(path, text)
    if report_format != "general":
        raise ValueError(f"Unknown weekly report format: {report_format}")
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

    _validate_period_and_filename(path, values["周期"], errors)

    top = _validate_body(lines, errors)
    _validate_completion_claims(lines, top, errors)
    _validate_combined_metrics_table(lines, top, values["范围"] or "", errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="weekly Markdown file to validate")
    parser.add_argument("--format", choices=("personal", "general"), default="personal")
    args = parser.parse_args(argv)
    errors = validate(args.report, report_format=args.format)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
