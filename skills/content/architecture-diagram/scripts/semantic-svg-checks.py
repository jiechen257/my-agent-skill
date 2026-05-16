#!/usr/bin/env python3
from __future__ import annotations

import math
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path


SVG_NS = "{http://www.w3.org/2000/svg}"
PARTICIPANT_CLASSES = {"participant", "service", "store", "source", "process", "infra"}
REGION_CLASSES = {"region", "product", "system-boundary", "boundary"}
EDGE_CLASSES = {"edge", "edge-soft"}
LINE_TOLERANCE = 2.5
CHIP_EDGE_GAP = 20.0
EDGE_ENDPOINT_PADDING = 10.0
TEXT_EDGE_GAP = 36.0
EDGE_CLEARANCE_GAP = 8.0
EDGE_CLEARANCE_TRIM = 14.0
LAYER_REGION_INSET = 24.0
CARD_TEXT_BOTTOM_INSET = 10.0
TOP_RAIL_GAP = 16.0
TEXT_SIZE_HINTS = {
    "label": 10.0,
    "legend": 11.0,
    "note-title": 13.0,
    "note-text": 11.0,
    "phase-text": 12.0,
    "branch-title": 11.0,
}
CELL_TEXT_CONTAINER_CLASSES = {"yes", "partial", "no", "header", "rowhead", "bar-a", "bar-b", "bar-c"}
LABEL_CONTAINER_CLASSES = {"chip", "label-bg", "edge-label-bg", "phase-pill", "note-card"}
CARD_CONTAINER_CLASSES = {"note-card", "status-card"}
NODE_BODY_RECT_CLASSES = {"participant", "service", "store", "source", "process", "infra", "sink", "terminal", "io", "state", "passive", "transform", "usecase", "node-body"}


def fail(message: str) -> None:
    raise SystemExit(message)


def parse_float(value: str | None, *, default: float | None = None) -> float:
    if value is None:
        if default is None:
            fail("missing numeric SVG attribute")
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise SystemExit(f"invalid numeric SVG attribute: {value}") from exc


def classes(el: ET.Element) -> set[str]:
    return {part for part in el.get("class", "").split() if part}


def svg_elements(root: ET.Element, tag: str) -> list[ET.Element]:
    return [el for el in root.iter() if el.tag == f"{SVG_NS}{tag}"]


def tokenize_path(path_data: str) -> list[str]:
    tokens: list[str] = []
    current = []
    for ch in path_data:
        if ch.isalpha():
            if current:
                tokens.append("".join(current).strip())
                current = []
            tokens.append(ch)
        elif ch in ", \n\t\r":
            if current:
                tokens.append("".join(current).strip())
                current = []
        else:
            current.append(ch)
    if current:
        tokens.append("".join(current).strip())
    return [token for token in tokens if token]


def parse_polyline_path(path_data: str) -> list[tuple[float, float]]:
    tokens = tokenize_path(path_data)
    points: list[tuple[float, float]] = []
    index = 0
    current = (0.0, 0.0)
    start = None
    command = None
    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            command = token
            index += 1
            if command in {"Z", "z"}:
                if start is not None and current != start:
                    points.append(start)
                    current = start
                continue
        if command is None:
            fail("path data missing command")
        if command in {"M", "L"}:
            x = float(tokens[index])
            y = float(tokens[index + 1])
            current = (x, y)
            points.append(current)
            if start is None:
                start = current
            if command == "M":
                command = "L"
            index += 2
        elif command == "H":
            x = float(tokens[index])
            current = (x, current[1])
            points.append(current)
            index += 1
        elif command == "V":
            y = float(tokens[index])
            current = (current[0], y)
            points.append(current)
            index += 1
        else:
            fail(f"unsupported path command for semantic validation: {command}")
    return points


def rect_box(el: ET.Element) -> dict[str, float]:
    x = parse_float(el.get("x"), default=0.0)
    y = parse_float(el.get("y"), default=0.0)
    width = parse_float(el.get("width"))
    height = parse_float(el.get("height"))
    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "right": x + width,
        "bottom": y + height,
        "cx": x + width / 2,
        "cy": y + height / 2,
    }


def line_box(el: ET.Element) -> dict[str, float]:
    x1 = parse_float(el.get("x1"))
    y1 = parse_float(el.get("y1"))
    x2 = parse_float(el.get("x2"))
    y2 = parse_float(el.get("y2"))
    return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}


def pick_inner_frame(rects: list[ET.Element], view_width: float, view_height: float) -> dict[str, float] | None:
    candidates = []
    for rect in rects:
        box = rect_box(rect)
        if box["x"] <= 0 or box["y"] <= 0:
            continue
        if box["right"] >= view_width or box["bottom"] >= view_height:
            continue
        candidates.append((box["width"] * box["height"], box))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def aligned(value: float, target: float, tolerance: float = LINE_TOLERANCE) -> bool:
    return abs(value - target) <= tolerance


def any_alignment(value: float, candidates: list[float], tolerance: float = LINE_TOLERANCE) -> bool:
    return any(aligned(value, candidate, tolerance) for candidate in candidates)


def element_y(el: ET.Element) -> float | None:
    if el.tag == f"{SVG_NS}line":
        line = line_box(el)
        return line["y1"] if abs(line["y1"] - line["y2"]) <= LINE_TOLERANCE else None
    if el.tag == f"{SVG_NS}text":
        return parse_float(el.get("y"), default=None)
    if el.tag == f"{SVG_NS}rect":
        return rect_box(el)["cy"]
    return None


def label_box_from_text(text_el: ET.Element) -> dict[str, float] | None:
    x = parse_float(text_el.get("x"), default=None)
    y = parse_float(text_el.get("y"), default=None)
    if x is None or y is None:
        return None
    return {"x": x, "y": y}


def text_anchor(el: ET.Element) -> str:
    return el.get("text-anchor", "start")


def text_font_size(el: ET.Element) -> float:
    direct = el.get("font-size")
    if direct:
        try:
            return float(direct)
        except ValueError:
            pass
    for cls in classes(el):
        if cls in TEXT_SIZE_HINTS:
            return TEXT_SIZE_HINTS[cls]
    return 12.0


def estimate_text_width(text: str, font_size: float) -> float:
    width = 0.0
    for char in text:
        if char.isspace():
            factor = 0.32
        elif unicodedata.east_asian_width(char) in {"W", "F"}:
            factor = 0.92
        elif char.isupper():
            factor = 0.62
        elif char.isdigit():
            factor = 0.56
        elif char in ".,:;!|/\\'`":
            factor = 0.28
        elif char in "()[]{}<>":
            factor = 0.38
        else:
            factor = 0.54
        width += font_size * factor
    return width


def text_runs(text_el: ET.Element) -> list[dict[str, object]]:
    runs: list[dict[str, object]] = []
    base_x = parse_float(text_el.get("x"), default=None)
    anchor = text_anchor(text_el)
    tspans = [child for child in list(text_el) if child.tag == f"{SVG_NS}tspan"]
    if tspans:
        for tspan in tspans:
            text = "".join(tspan.itertext()).strip()
            if not text:
                continue
            x = parse_float(tspan.get("x"), default=base_x)
            if x is None:
                continue
            runs.append({"text": text, "x": x, "anchor": anchor})
        return runs

    text = "".join(text_el.itertext()).strip()
    if text and base_x is not None:
        runs.append({"text": text, "x": base_x, "anchor": anchor})
    return runs


def run_bounds(run: dict[str, object], font_size: float) -> tuple[float, float]:
    text = str(run["text"])
    x = float(run["x"])
    width = estimate_text_width(text, font_size)
    anchor = str(run["anchor"])
    if anchor == "middle":
        return x - width / 2, x + width / 2
    if anchor == "end":
        return x - width, x
    return x, x + width


def distance_to_interval(value: float, lower: float, upper: float) -> float:
    if lower <= value <= upper:
        return 0.0
    if value < lower:
        return lower - value
    return value - upper


def rect_touches_segment(box: dict[str, float], start: tuple[float, float], end: tuple[float, float]) -> bool:
    x1, y1 = start
    x2, y2 = end
    if math.isclose(x1, x2, abs_tol=LINE_TOLERANCE):
        lower = min(y1, y2) + EDGE_ENDPOINT_PADDING
        upper = max(y1, y2) - EDGE_ENDPOINT_PADDING
        if lower > upper:
            lower, upper = min(y1, y2), max(y1, y2)
        y_center = box["cy"]
        if not lower - 8 <= y_center <= upper + 8:
            return False
        gap = distance_to_interval(x1, box["x"], box["right"])
        return gap <= CHIP_EDGE_GAP
    if math.isclose(y1, y2, abs_tol=LINE_TOLERANCE):
        lower = min(x1, x2) + EDGE_ENDPOINT_PADDING
        upper = max(x1, x2) - EDGE_ENDPOINT_PADDING
        if lower > upper:
            lower, upper = min(x1, x2), max(x1, x2)
        x_center = box["cx"]
        if not lower - 8 <= x_center <= upper + 8:
            return False
        gap = distance_to_interval(y1, box["y"], box["bottom"])
        return gap <= CHIP_EDGE_GAP

    dx = x2 - x1
    dy = y2 - y1
    length_sq = dx * dx + dy * dy
    if length_sq == 0:
        return False
    px = box["cx"]
    py = box["cy"]
    t = ((px - x1) * dx + (py - y1) * dy) / length_sq
    if not 0.05 <= t <= 0.95:
        return False
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y) <= CHIP_EDGE_GAP


def point_near_segment(px: float, py: float, start: tuple[float, float], end: tuple[float, float], tolerance: float) -> bool:
    x1, y1 = start
    x2, y2 = end
    if math.isclose(x1, x2, abs_tol=LINE_TOLERANCE):
        lower = min(y1, y2) - 6
        upper = max(y1, y2) + 6
        return lower <= py <= upper and abs(px - x1) <= tolerance
    if math.isclose(y1, y2, abs_tol=LINE_TOLERANCE):
        lower = min(x1, x2) - 6
        upper = max(x1, x2) + 6
        return lower <= px <= upper and abs(py - y1) <= tolerance

    dx = x2 - x1
    dy = y2 - y1
    length_sq = dx * dx + dy * dy
    if length_sq == 0:
        return False
    t = ((px - x1) * dx + (py - y1) * dy) / length_sq
    if not -0.05 <= t <= 1.05:
        return False
    proj_x = x1 + max(0.0, min(1.0, t)) * dx
    proj_y = y1 + max(0.0, min(1.0, t)) * dy
    return math.hypot(px - proj_x, py - proj_y) <= tolerance


def extract_edge_segments(el: ET.Element) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    if el.tag == f"{SVG_NS}line":
        line = line_box(el)
        return [((line["x1"], line["y1"]), (line["x2"], line["y2"]))]
    if el.tag == f"{SVG_NS}path":
        points = parse_polyline_path(el.get("d", ""))
        return list(zip(points, points[1:]))
    return []


def path_bbox(el: ET.Element) -> dict[str, float] | None:
    path_data = el.get("d")
    if not path_data:
        return None
    points = parse_polyline_path(path_data)
    if len(points) < 2:
        return None
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return {
        "x": min(xs),
        "y": min(ys),
        "right": max(xs),
        "bottom": max(ys),
        "width": max(xs) - min(xs),
        "height": max(ys) - min(ys),
        "cx": (min(xs) + max(xs)) / 2,
        "cy": (min(ys) + max(ys)) / 2,
    }


def shape_contains_point(box: dict[str, float], x: float, y: float) -> bool:
    return box["x"] <= x <= box["right"] and box["y"] <= y <= box["bottom"]


def boxes_overlap(a: dict[str, float], b: dict[str, float], padding: float = 0.0) -> bool:
    return not (
        a["right"] <= b["x"] + padding
        or b["right"] <= a["x"] + padding
        or a["bottom"] <= b["y"] + padding
        or b["bottom"] <= a["y"] + padding
    )


def is_node_body_rect(rect: ET.Element) -> bool:
    rect_classes = classes(rect)
    return bool(rect_classes & NODE_BODY_RECT_CLASSES) and not bool(rect_classes & REGION_CLASSES)


def css_fill_order(root: ET.Element) -> list[tuple[str, str]]:
    order: list[tuple[str, str]] = []
    for style in svg_elements(root, "style"):
        style_text = "".join(style.itertext())
        for match in re.finditer(r"\.([A-Za-z0-9_-]+)\s*\{([^{}]+)\}", style_text):
            class_name = match.group(1)
            body = match.group(2)
            fill_match = re.search(r"(?<![-\w])fill\s*:\s*([^;]+)", body)
            if fill_match:
                order.append((class_name, fill_match.group(1).strip()))
    return order


def inline_fill(el: ET.Element) -> str | None:
    if el.get("fill"):
        return el.get("fill")
    style = el.get("style", "")
    fill_match = re.search(r"(?<![-\w])fill\s*:\s*([^;]+)", style)
    if fill_match:
        return fill_match.group(1).strip()
    return None


def effective_fill(el: ET.Element, fill_order: list[tuple[str, str]]) -> str | None:
    direct = inline_fill(el)
    if direct:
        return direct

    el_classes = classes(el)
    fill = None
    for class_name, class_fill in fill_order:
        if class_name in el_classes:
            fill = class_fill
    return fill


def point_on_box_border(box: dict[str, float], point: tuple[float, float], tolerance: float = LINE_TOLERANCE) -> bool:
    x, y = point
    inside_x = box["x"] - tolerance <= x <= box["right"] + tolerance
    inside_y = box["y"] - tolerance <= y <= box["bottom"] + tolerance
    if not (inside_x and inside_y):
        return False

    on_vertical = (abs(x - box["x"]) <= tolerance or abs(x - box["right"]) <= tolerance) and box["y"] - tolerance <= y <= box["bottom"] + tolerance
    on_horizontal = (abs(y - box["y"]) <= tolerance or abs(y - box["bottom"]) <= tolerance) and box["x"] - tolerance <= x <= box["right"] + tolerance
    return on_vertical or on_horizontal


def polygon_from_rect(box: dict[str, float]) -> list[tuple[float, float]]:
    return [
        (box["x"], box["y"]),
        (box["right"], box["y"]),
        (box["right"], box["bottom"]),
        (box["x"], box["bottom"]),
    ]


def polygon_from_ellipse(cx: float, cy: float, rx: float, ry: float, steps: int = 24) -> list[tuple[float, float]]:
    points = []
    for index in range(steps):
        angle = (2 * math.pi * index) / steps
        points.append((cx + math.cos(angle) * rx, cy + math.sin(angle) * ry))
    return points


def normalize_polygon(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if len(points) > 1 and points[0] == points[-1]:
        return points[:-1]
    return points


def point_in_polygon(point: tuple[float, float], polygon: list[tuple[float, float]]) -> bool:
    x, y = point
    inside = False
    count = len(polygon)
    if count < 3:
        return False
    for index in range(count):
        x1, y1 = polygon[index]
        x2, y2 = polygon[(index + 1) % count]
        intersects = (y1 > y) != (y2 > y)
        if not intersects:
            continue
        cross_x = (x2 - x1) * (y - y1) / (y2 - y1) + x1
        if cross_x >= x:
            inside = not inside
    return inside


def point_segment_distance(point: tuple[float, float], start: tuple[float, float], end: tuple[float, float]) -> float:
    px, py = point
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    length_sq = dx * dx + dy * dy
    if length_sq == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / length_sq
    t = max(0.0, min(1.0, t))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)


def orientation(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> bool:
    return (
        min(a[0], c[0]) - LINE_TOLERANCE <= b[0] <= max(a[0], c[0]) + LINE_TOLERANCE
        and min(a[1], c[1]) - LINE_TOLERANCE <= b[1] <= max(a[1], c[1]) + LINE_TOLERANCE
    )


def segments_intersect(
    start_a: tuple[float, float],
    end_a: tuple[float, float],
    start_b: tuple[float, float],
    end_b: tuple[float, float],
) -> bool:
    o1 = orientation(start_a, end_a, start_b)
    o2 = orientation(start_a, end_a, end_b)
    o3 = orientation(start_b, end_b, start_a)
    o4 = orientation(start_b, end_b, end_a)

    if (o1 > 0 > o2 or o1 < 0 < o2) and (o3 > 0 > o4 or o3 < 0 < o4):
        return True
    if math.isclose(o1, 0.0, abs_tol=LINE_TOLERANCE) and on_segment(start_a, start_b, end_a):
        return True
    if math.isclose(o2, 0.0, abs_tol=LINE_TOLERANCE) and on_segment(start_a, end_b, end_a):
        return True
    if math.isclose(o3, 0.0, abs_tol=LINE_TOLERANCE) and on_segment(start_b, start_a, end_b):
        return True
    if math.isclose(o4, 0.0, abs_tol=LINE_TOLERANCE) and on_segment(start_b, end_a, end_b):
        return True
    return False


def segment_distance(
    start_a: tuple[float, float],
    end_a: tuple[float, float],
    start_b: tuple[float, float],
    end_b: tuple[float, float],
) -> float:
    if segments_intersect(start_a, end_a, start_b, end_b):
        return 0.0
    return min(
        point_segment_distance(start_a, start_b, end_b),
        point_segment_distance(end_a, start_b, end_b),
        point_segment_distance(start_b, start_a, end_a),
        point_segment_distance(end_b, start_a, end_a),
    )


def trim_segment(
    start: tuple[float, float],
    end: tuple[float, float],
    padding: float,
) -> tuple[tuple[float, float], tuple[float, float]] | None:
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length <= padding * 2 + 1:
        return None
    ux = dx / length
    uy = dy / length
    return (x1 + ux * padding, y1 + uy * padding), (x2 - ux * padding, y2 - uy * padding)


def segment_grazes_polygon(
    start: tuple[float, float],
    end: tuple[float, float],
    polygon: list[tuple[float, float]],
    clearance: float,
) -> bool:
    polygon = normalize_polygon(polygon)
    if len(polygon) < 3:
        return False

    xs = [point[0] for point in polygon]
    ys = [point[1] for point in polygon]
    seg_box = {
        "x": min(start[0], end[0]) - clearance,
        "y": min(start[1], end[1]) - clearance,
        "right": max(start[0], end[0]) + clearance,
        "bottom": max(start[1], end[1]) + clearance,
    }
    poly_box = {"x": min(xs), "y": min(ys), "right": max(xs), "bottom": max(ys)}
    if not boxes_overlap(seg_box, poly_box):
        return False

    if point_in_polygon(start, polygon) or point_in_polygon(end, polygon):
        return True

    for index in range(len(polygon)):
        edge_start = polygon[index]
        edge_end = polygon[(index + 1) % len(polygon)]
        if segment_distance(start, end, edge_start, edge_end) <= clearance:
            return True
    return False


def validate_edge_label_ownership(root: ET.Element) -> None:
    edges: dict[str, ET.Element] = {}
    for el in root.iter():
        edge_id = el.get("id")
        if not edge_id:
            continue
        if el.tag not in {f"{SVG_NS}line", f"{SVG_NS}path"}:
            continue
        edges[edge_id] = el

    texts_by_edge: dict[str, list[ET.Element]] = {}
    for text in svg_elements(root, "text"):
        edge_id = text.get("data-edge-id")
        if edge_id:
            texts_by_edge.setdefault(edge_id, []).append(text)

    chip_backed_edges: set[str] = set()
    for rect in svg_elements(root, "rect"):
        rect_classes = classes(rect)
        if not ({"chip", "label-bg", "edge-label-bg"} & rect_classes):
            continue
        edge_id = rect.get("data-edge-id")
        if not edge_id:
            continue
        if edge_id not in edges:
            fail(f"chip references missing edge id '{edge_id}'")
        chip_backed_edges.add(edge_id)

        texts = texts_by_edge.get(edge_id, [])
        if not texts:
            fail(f"chip for edge '{edge_id}' is missing matching label text")

        box = rect_box(rect)
        matched_text = None
        for text in texts:
            label_box = label_box_from_text(text)
            if label_box is None:
                continue
            if box["x"] - 4 <= label_box["x"] <= box["right"] + 4 and box["y"] - 4 <= label_box["y"] <= box["bottom"] + 8:
                matched_text = text
                break
        if matched_text is None:
            fail(f"label text for edge '{edge_id}' does not sit inside its chip")

        allowed_width = box["width"] - 10
        for run in text_runs(matched_text):
            if estimate_text_width(str(run["text"]), text_font_size(matched_text)) > allowed_width:
                fail(f"label text for edge '{edge_id}' is wider than its chip")

        segments = extract_edge_segments(edges[edge_id])
        if not segments:
            fail(f"edge '{edge_id}' has no readable segments for semantic validation")
        if not any(rect_touches_segment(box, start, end) for start, end in segments):
            fail(f"chip for edge '{edge_id}' is not attached to its owning edge")

    for edge_id, texts in texts_by_edge.items():
        if edge_id in chip_backed_edges:
            continue
        if edge_id not in edges:
            fail(f"text label references missing edge id '{edge_id}'")
        segments = extract_edge_segments(edges[edge_id])
        if not segments:
            fail(f"edge '{edge_id}' has no readable segments for semantic validation")
        for text in texts:
            runs = text_runs(text)
            if not runs:
                continue
            font_size = text_font_size(text)
            attached = False
            for run in runs:
                left, right = run_bounds(run, font_size)
                px = (left + right) / 2
                py = parse_float(text.get("y"), default=0.0)
                if any(point_near_segment(px, py, start, end, TEXT_EDGE_GAP) for start, end in segments):
                    attached = True
                    break
            if not attached:
                fail(f"text-only label for edge '{edge_id}' is not attached to its owning edge")


def validate_text_fit(root: ET.Element, inner_frame: dict[str, float] | None) -> None:
    rects = svg_elements(root, "rect")
    texts = svg_elements(root, "text")

    note_cards = [rect_box(rect) for rect in rects if "note-card" in classes(rect)]
    cards = [rect_box(rect) for rect in rects if classes(rect) & CARD_CONTAINER_CLASSES]
    phase_pills = [rect_box(rect) for rect in rects if "phase-pill" in classes(rect)]
    frames_by_id = {rect.get("data-frame-id"): rect_box(rect) for rect in rects if rect.get("data-frame-id")}

    for text in texts:
        text_classes = classes(text)
        font_size = text_font_size(text)
        runs = text_runs(text)
        if not runs:
            continue

        x = parse_float(text.get("x"), default=None)
        y = parse_float(text.get("y"), default=None)
        if x is not None and y is not None:
            card = next((box for box in cards if box["x"] <= x <= box["right"] and box["y"] <= y <= box["bottom"]), None)
            if card is not None and y > card["bottom"] - CARD_TEXT_BOTTOM_INSET:
                fail("card text sits too close to the bottom border; increase card height or move the text up")

        if "note-title" in text_classes or "note-text" in text_classes:
            box = next((box for box in note_cards if box["x"] + 8 <= parse_float(text.get("x"), default=box["x"]) <= box["right"] - 8 and box["y"] + 8 <= parse_float(text.get("y"), default=box["y"]) <= box["bottom"] + 8), None)
            if box is None:
                continue
            for run in runs:
                left, right = run_bounds(run, font_size)
                if left < box["x"] + 24 or right > box["right"] - 24:
                    fail("note text exceeds note card width; wrap or widen the card")

        if "phase-text" in text_classes:
            x = parse_float(text.get("x"), default=None)
            y = parse_float(text.get("y"), default=None)
            if x is None or y is None:
                continue
            box = next((box for box in phase_pills if box["x"] <= x <= box["right"] and box["y"] - 4 <= y <= box["bottom"] + 6), None)
            if box is None:
                continue
            for run in runs:
                left, right = run_bounds(run, font_size)
                if left < box["x"] + 12 or right > box["right"] - 12:
                    fail("phase title exceeds phase pill width; widen or shorten it")

        if "legend" in text_classes and inner_frame is not None:
            y = parse_float(text.get("y"), default=None)
            if y is None or y < inner_frame["y"] + inner_frame["height"] * 0.6:
                continue
            for run in runs:
                left, right = run_bounds(run, font_size)
                if left < inner_frame["x"] + 24 or right > inner_frame["right"] - 24:
                    fail("legend text exceeds safe rail width; wrap into multiple rows")

        if "branch-title" in text_classes:
            frame_id = text.get("data-frame-id")
            if not frame_id or frame_id not in frames_by_id:
                continue
            box = frames_by_id[frame_id]
            for run in runs:
                left, right = run_bounds(run, font_size)
                if left < box["x"] + 36 or right > box["right"] - 24:
                    fail(f"branch title for frame '{frame_id}' exceeds available frame width")


def validate_node_text_fit(root: ET.Element) -> None:
    candidates: list[dict[str, object]] = []
    for rect in svg_elements(root, "rect"):
        box = rect_box(rect)
        candidates.append({"kind": "rect", "box": box, "area": box["width"] * box["height"]})
    for ellipse in svg_elements(root, "ellipse"):
        cx = parse_float(ellipse.get("cx"))
        cy = parse_float(ellipse.get("cy"))
        rx = parse_float(ellipse.get("rx"))
        ry = parse_float(ellipse.get("ry"))
        box = {
            "x": cx - rx,
            "y": cy - ry,
            "right": cx + rx,
            "bottom": cy + ry,
            "width": rx * 2,
            "height": ry * 2,
            "cx": cx,
            "cy": cy,
            "rx": rx,
            "ry": ry,
        }
        candidates.append({"kind": "ellipse", "box": box, "area": box["width"] * box["height"]})
    for path in svg_elements(root, "path"):
        if "decision" not in classes(path):
            continue
        box = path_bbox(path)
        if box is None:
            continue
        candidates.append({"kind": "decision", "box": box, "area": box["width"] * box["height"]})

    for text in svg_elements(root, "text"):
        text_classes = classes(text)
        if not ({"node-title", "node-sub"} & text_classes):
            continue
        x = parse_float(text.get("x"), default=None)
        y = parse_float(text.get("y"), default=None)
        if x is None or y is None:
            continue
        matches = [candidate for candidate in candidates if shape_contains_point(candidate["box"], x, y)]
        if not matches:
            continue
        candidate = min(matches, key=lambda item: float(item["area"]))
        box = candidate["box"]
        kind = str(candidate["kind"])
        if kind == "rect":
            allowed_width = float(box["width"]) - (16 if "node-title" in text_classes else 24)
        elif kind == "ellipse":
            allowed_width = float(box["width"]) - 28
        else:
            allowed_width = float(box["width"]) * 0.58
        allowed_width = max(allowed_width, 24.0)
        font_size = text_font_size(text)
        for run in text_runs(text):
            width = estimate_text_width(str(run["text"]), font_size)
            if width > allowed_width:
                fail(f"node text exceeds {kind} container width; widen or wrap the node")


def validate_cell_text_fit(root: ET.Element) -> None:
    candidates: list[dict[str, object]] = []
    for rect in svg_elements(root, "rect"):
        rect_classes = classes(rect)
        if not (rect_classes & CELL_TEXT_CONTAINER_CLASSES):
            continue
        box = rect_box(rect)
        candidates.append({"box": box, "area": box["width"] * box["height"]})

    for text in svg_elements(root, "text"):
        if "label" not in classes(text):
            continue
        x = parse_float(text.get("x"), default=None)
        y = parse_float(text.get("y"), default=None)
        if x is None or y is None:
            continue
        matches = [candidate for candidate in candidates if shape_contains_point(candidate["box"], x, y)]
        if not matches:
            continue
        box = min(matches, key=lambda item: float(item["area"]))["box"]
        allowed_width = float(box["width"]) - 18
        font_size = text_font_size(text)
        for run in text_runs(text):
            width = estimate_text_width(str(run["text"]), font_size)
            if width > allowed_width:
                fail("cell or bar label exceeds container width; widen or wrap the container")


def validate_container_spacing(root: ET.Element) -> None:
    foreground: list[tuple[str, dict[str, float]]] = []
    node_bodies: list[tuple[str, dict[str, float]]] = []

    for rect in svg_elements(root, "rect"):
        rect_classes = classes(rect)
        box = rect_box(rect)
        if rect_classes & LABEL_CONTAINER_CLASSES:
            foreground.append(("rect", box))
        if rect_classes & NODE_BODY_RECT_CLASSES:
            node_bodies.append(("rect", box))

    for ellipse in svg_elements(root, "ellipse"):
        ellipse_classes = classes(ellipse)
        if "usecase" not in ellipse_classes:
            continue
        cx = parse_float(ellipse.get("cx"))
        cy = parse_float(ellipse.get("cy"))
        rx = parse_float(ellipse.get("rx"))
        ry = parse_float(ellipse.get("ry"))
        node_bodies.append(
            (
                "ellipse",
                {
                    "x": cx - rx,
                    "y": cy - ry,
                    "right": cx + rx,
                    "bottom": cy + ry,
                    "width": rx * 2,
                    "height": ry * 2,
                },
            )
        )

    for path in svg_elements(root, "path"):
        if "decision" not in classes(path):
            continue
        box = path_bbox(path)
        if box is not None:
            node_bodies.append(("decision", box))

    for index, (_, box) in enumerate(foreground):
        for _, other_box in foreground[index + 1 :]:
            if boxes_overlap(box, other_box, padding=0.0):
                fail("foreground containers overlap; add spacing or reroute labels")

    for _, fg_box in foreground:
        for _, node_box in node_bodies:
            if boxes_overlap(fg_box, node_box, padding=0.0):
                fail("label container overlaps a node body; reroute or move the label")


def collect_node_polygons(root: ET.Element) -> list[list[tuple[float, float]]]:
    polygons: list[list[tuple[float, float]]] = []

    for rect in svg_elements(root, "rect"):
        if is_node_body_rect(rect):
            polygons.append(polygon_from_rect(rect_box(rect)))

    for ellipse in svg_elements(root, "ellipse"):
        if "usecase" not in classes(ellipse):
            continue
        polygons.append(
            polygon_from_ellipse(
                parse_float(ellipse.get("cx")),
                parse_float(ellipse.get("cy")),
                parse_float(ellipse.get("rx")),
                parse_float(ellipse.get("ry")),
            )
        )

    for path in svg_elements(root, "path"):
        if "decision" not in classes(path):
            continue
        polygons.append(normalize_polygon(parse_polyline_path(path.get("d", ""))))

    return polygons


def validate_edge_clearance(root: ET.Element) -> None:
    label_polygons: list[dict[str, object]] = []
    for rect in svg_elements(root, "rect"):
        rect_classes = classes(rect)
        if not (rect_classes & LABEL_CONTAINER_CLASSES):
            continue
        label_polygons.append(
            {
                "edge_id": rect.get("data-edge-id"),
                "polygon": polygon_from_rect(rect_box(rect)),
            }
        )

    node_polygons = collect_node_polygons(root)

    for edge in root.iter():
        if edge.tag not in {f"{SVG_NS}line", f"{SVG_NS}path"}:
            continue
        edge_classes = classes(edge)
        if not (edge_classes & EDGE_CLASSES):
            continue
        if "edge-bus" in edge_classes:
            continue

        edge_id = edge.get("id")
        segments = extract_edge_segments(edge)
        for start, end in segments:
            trimmed = trim_segment(start, end, EDGE_CLEARANCE_TRIM)
            if trimmed is None:
                continue
            trimmed_start, trimmed_end = trimmed

            for polygon in node_polygons:
                if segment_grazes_polygon(trimmed_start, trimmed_end, polygon, EDGE_CLEARANCE_GAP):
                    fail("edge route grazes a node body; reroute to leave visible air")

            for item in label_polygons:
                if edge_id and item["edge_id"] == edge_id:
                    continue
                if segment_grazes_polygon(trimmed_start, trimmed_end, item["polygon"], EDGE_CLEARANCE_GAP):
                    fail("edge route grazes an unrelated label container; move the edge or label")


def validate_architecture_layers(root: ET.Element) -> None:
    is_architecture = root.get("data-diagram-type") == "architecture"
    has_layer_data = any(el.get("data-layer-id") for el in root.iter())
    if not (is_architecture or has_layer_data):
        return

    rects = svg_elements(root, "rect")
    regions: dict[str, dict[str, float]] = {}
    for rect in rects:
        layer_id = rect.get("data-layer-id")
        if not layer_id:
            continue
        if classes(rect) & REGION_CLASSES:
            regions[layer_id] = rect_box(rect)

    nodes_by_layer: dict[str, list[ET.Element]] = {}
    for rect in rects:
        if not is_node_body_rect(rect):
            continue
        layer_id = rect.get("data-layer-id")
        if not layer_id:
            if is_architecture:
                fail("architecture node body is missing data-layer-id")
            continue
        nodes_by_layer.setdefault(layer_id, []).append(rect)

    if is_architecture and not regions:
        fail("architecture diagram is missing data-layer-id regions")
    if is_architecture and not nodes_by_layer:
        fail("architecture diagram is missing data-layer-id node bodies")

    fill_order = css_fill_order(root)
    for layer_id, nodes in nodes_by_layer.items():
        if layer_id not in regions:
            fail(f"layer '{layer_id}' has nodes but no matching region")

        region = regions[layer_id]
        fills = set()
        for node in nodes:
            box = rect_box(node)
            if (
                box["x"] < region["x"] + LAYER_REGION_INSET
                or box["right"] > region["right"] - LAYER_REGION_INSET
                or box["y"] < region["y"] + LAYER_REGION_INSET
                or box["bottom"] > region["bottom"] - LAYER_REGION_INSET
            ):
                fail(f"node body in layer '{layer_id}' violates region inset")

            fill = effective_fill(node, fill_order)
            if not fill:
                fail(f"node body in layer '{layer_id}' has no resolvable fill")
            fills.add(fill)

        if len(fills) > 1:
            fail(f"layer '{layer_id}' mixes node body fills: {', '.join(sorted(fills))}")


def validate_architecture_edges(root: ET.Element) -> None:
    if root.get("data-diagram-type") != "architecture":
        return

    node_boxes = {
        rect.get("id"): rect_box(rect)
        for rect in svg_elements(root, "rect")
        if rect.get("id") and is_node_body_rect(rect)
    }

    for edge in root.iter():
        if edge.tag not in {f"{SVG_NS}line", f"{SVG_NS}path"}:
            continue

        edge_classes = classes(edge)
        if "edge-bus" in edge_classes:
            if edge.get("marker-end"):
                fail("edge-bus must not carry an arrowhead")
            continue
        if not (edge_classes & EDGE_CLASSES):
            continue
        if edge.get("data-nonsemantic") == "legend":
            continue

        if edge.tag == f"{SVG_NS}path" and tokenize_path(edge.get("d", "")).count("M") > 1:
            fail("directed architecture edge uses multiple subpaths; split it or use edge-bus")

        from_id = edge.get("data-from")
        to_id = edge.get("data-to")
        if not from_id or not to_id:
            fail("architecture edge is missing data-from or data-to")
        if from_id not in node_boxes:
            fail(f"architecture edge references missing source node '{from_id}'")
        if to_id not in node_boxes:
            fail(f"architecture edge references missing target node '{to_id}'")

        if edge.tag == f"{SVG_NS}line":
            line = line_box(edge)
            points = [(line["x1"], line["y1"]), (line["x2"], line["y2"])]
        else:
            points = parse_polyline_path(edge.get("d", ""))
        if len(points) < 2:
            fail("architecture edge has no readable route")

        if not point_on_box_border(node_boxes[from_id], points[0]):
            fail(f"architecture edge from '{from_id}' does not start on the node border")
        if not point_on_box_border(node_boxes[to_id], points[-1]):
            fail(f"architecture edge to '{to_id}' does not end on the node border")


def validate_common(root: ET.Element, inner_frame: dict[str, float] | None) -> None:
    if inner_frame is None:
        return

    rects = svg_elements(root, "rect")
    texts = svg_elements(root, "text")

    for rect in rects:
        if "note-card" not in classes(rect):
            continue
        box = rect_box(rect)
        if box["x"] < inner_frame["x"] + 24:
            fail("note card violates left safe inset")
        if box["right"] > inner_frame["right"] - 40:
            fail("note card violates right safe inset")
        if box["y"] < inner_frame["y"] + 24:
            fail("note card sits too close to the top edge")

    top_cards = [
        rect_box(rect)
        for rect in rects
        if classes(rect) & CARD_CONTAINER_CLASSES and rect_box(rect)["y"] < inner_frame["y"] + inner_frame["height"] * 0.18
    ]
    primary_regions = [
        rect_box(rect)
        for rect in rects
        if classes(rect) & (REGION_CLASSES | {"product"}) and rect_box(rect)["y"] > inner_frame["y"] + inner_frame["height"] * 0.08
    ]
    for card in top_cards:
        for region in primary_regions:
            if region["y"] <= card["bottom"]:
                continue
            horizontal_overlap = min(card["right"], region["right"]) - max(card["x"], region["x"])
            if horizontal_overlap <= 0:
                continue
            if region["y"] - card["bottom"] < TOP_RAIL_GAP:
                fail("top note rail is too close to the next region boundary")

    for text in texts:
        if "legend" not in classes(text):
            continue
        y = parse_float(text.get("y"))
        if y < inner_frame["y"] + inner_frame["height"] * 0.6:
            continue
        if inner_frame["bottom"] - y < 56:
            fail("legend violates bottom safe inset")


def validate_sequence(root: ET.Element, inner_frame: dict[str, float] | None) -> None:
    rects = svg_elements(root, "rect")
    lines = svg_elements(root, "line")

    lifelines = [line for line in lines if "lifeline" in classes(line)]
    messages = [line for line in lines if classes(line) & {"msg", "async"}]
    activations = [rect for rect in rects if "activation" in classes(rect)]
    participants = [rect for rect in rects if classes(rect) & PARTICIPANT_CLASSES]
    phase_bands = [rect for rect in rects if "phase-band" in classes(rect)]
    frames = [rect for rect in rects if "frame" in classes(rect)]
    separators = [line for line in lines if "frame-sep" in classes(line)]

    if not (lifelines or messages or activations):
        return

    lifeline_boxes = [line_box(line) for line in lifelines]
    message_boxes = [line_box(line) for line in messages]
    activation_boxes = [rect_box(rect) for rect in activations]
    participant_boxes = [rect_box(rect) for rect in participants]

    for lifeline in lifeline_boxes:
        if not aligned(lifeline["x1"], lifeline["x2"]):
            fail("lifeline is not vertical")

    if participants and lifelines:
        lifeline_xs = [box["x1"] for box in lifeline_boxes]
        for participant in participant_boxes:
            if not any_alignment(participant["cx"], lifeline_xs):
                fail("participant center is not aligned to a lifeline")

    if phase_bands and participants:
        earliest_phase = min(rect_box(rect)["y"] for rect in phase_bands)
        max_participant_bottom = max(box["bottom"] for box in participant_boxes)
        if earliest_phase < max_participant_bottom + 12:
            fail("phase band starts before participant heads clear")

    if messages:
        max_message_y = max(box["y1"] for box in message_boxes)
        for lifeline in lifeline_boxes:
            if lifeline["y2"] < max_message_y + 24:
                fail("lifeline does not extend past the final message")

    activation_centerlines = [box["cx"] for box in activation_boxes]
    lifeline_xs = [box["x1"] for box in lifeline_boxes]

    def endpoint_ok(x: float, y: float) -> bool:
        if any(aligned(x, lifeline_x) and y >= lifeline["y1"] - 2 and y <= lifeline["y2"] + 2 for lifeline_x, lifeline in zip(lifeline_xs, lifeline_boxes)):
            return True
        for activation in activation_boxes:
            if aligned(x, activation["cx"]) and activation["y"] - 6 <= y <= activation["bottom"] + 6:
                return True
        return False

    for message in message_boxes:
        if not aligned(message["y1"], message["y2"]):
            fail("sequence message is not horizontal")
        if not endpoint_ok(message["x1"], message["y1"]):
            fail("message source does not land on a lifeline or activation")
        if not endpoint_ok(message["x2"], message["y2"]):
            fail("message destination does not land on a lifeline or activation")

    for activation in activation_boxes:
        hit = False
        for message in message_boxes:
            endpoints = ((message["x1"], message["y1"]), (message["x2"], message["y2"]))
            for x, y in endpoints:
                if aligned(x, activation["cx"]) and activation["y"] - 6 <= y <= activation["bottom"] + 6:
                    hit = True
                    break
            if hit:
                break
        if not hit:
            fail("activation bar does not overlap any message endpoint")

    frame_boxes = [(rect, rect_box(rect)) for rect in frames]
    for separator in separators:
        sep = line_box(separator)
        sep_y = sep["y1"]
        frame_match = None
        for frame_el, frame in frame_boxes:
            if frame["x"] - 2 <= min(sep["x1"], sep["x2"]) and frame["right"] + 2 >= max(sep["x1"], sep["x2"]) and frame["y"] <= sep_y <= frame["bottom"]:
                frame_match = (frame_el, frame)
                break
        if frame_match is None:
            fail("frame separator is not enclosed by a frame")
        _, frame = frame_match
        if sep_y <= frame["y"] + 20 or sep_y >= frame["bottom"] - 20:
            fail("frame separator sits too close to the frame edge")
        y_positions = [message["y1"] for message in message_boxes if frame["y"] + 10 <= message["y1"] <= frame["bottom"] - 10]
        if not any(y < sep_y - 12 for y in y_positions):
            fail("frame separator has no branch content above it")
        if not any(y > sep_y + 12 for y in y_positions):
            fail("frame separator has no branch content below it")

    frame_ids = {}
    for el in root.iter():
        frame_id = el.get("data-frame-id")
        if not frame_id:
            continue
        frame_ids.setdefault(frame_id, []).append(el)

    for frame_id, elements in frame_ids.items():
        sep_y = None
        for el in elements:
            if el.tag == f"{SVG_NS}line" and "frame-sep" in classes(el):
                sep_y = line_box(el)["y1"]
                break
        if sep_y is None:
            continue
        for el in elements:
            branch = el.get("data-branch")
            if not branch:
                continue
            y = element_y(el)
            if y is None:
                continue
            if branch == "1" and y >= sep_y:
                fail(f"frame branch 1 content crosses below separator for frame '{frame_id}'")
            if branch == "2" and y <= sep_y:
                fail(f"frame branch 2 content crosses above separator for frame '{frame_id}'")

    if inner_frame is not None:
        for legend in svg_elements(root, "text"):
            if "legend" not in classes(legend):
                continue
            y = parse_float(legend.get("y"))
            if y < inner_frame["y"] + inner_frame["height"] * 0.6:
                continue
            if y > inner_frame["bottom"] - 56:
                fail("legend sits outside the bottom safe rail")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: semantic-svg-checks.py <svg-file>")

    svg_path = Path(sys.argv[1])
    root = ET.parse(svg_path).getroot()
    view_box = root.get("viewBox")
    if view_box:
        parts = [float(part) for part in view_box.split()]
        if len(parts) != 4:
            fail("invalid viewBox")
        _, _, view_width, view_height = parts
    else:
        view_width = parse_float(root.get("width"))
        view_height = parse_float(root.get("height"))

    rects = svg_elements(root, "rect")
    inner_frame = pick_inner_frame(rects, view_width, view_height)

    validate_common(root, inner_frame)
    validate_edge_label_ownership(root)
    validate_text_fit(root, inner_frame)
    validate_node_text_fit(root)
    validate_cell_text_fit(root)
    validate_container_spacing(root)
    validate_architecture_layers(root)
    validate_architecture_edges(root)
    validate_edge_clearance(root)
    validate_sequence(root, inner_frame)


if __name__ == "__main__":
    main()
