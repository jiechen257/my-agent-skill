#!/usr/bin/env node
// 结构性校验脚本：解析 SVG → 提取 spec → 跑 case 中的 automated_checks
// 用法：node check.mjs            （比较 out/before vs out/after）
//      node check.mjs after       （只校验 out/after）
//      node check.mjs before      （只校验 out/before）

import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = __dirname;
const CASES_DIR = join(ROOT, 'cases');
const OUT_DIR = join(ROOT, 'out');

// ---------- Token 配置（与 skill design tokens 一致） ----------
const PALETTES = {
  'warm-beige': new Set([
    '#000000', '#ffffff', '#fff7e8',
    '#f8f6f3', '#fffdf8', '#a8c5e6', '#9dd4c7', '#f4e4c1', '#e8e6e3',
    '#dff3ef', '#5a5a5a', '#8a8178', '#1a1a1a', '#6a6a6a', '#d9d3ca',
    '#fffaf2', '#655a4d', '#211a14', '#427858', '#1f7584', '#c6503f',
    '#f1e5d3', '#fbf7ef', '#daf0e1', '#f6dfcd', '#ece7fb', '#dceff2',
    '#edf7f1', '#fff0eb', '#edf7f8', '#d8cbb9', '#e4d8c7', '#8c7d68',
    '#f7f1e7', '#c7663d', '#6d5aa7'
  ]),
  'cool-blue': new Set([
    '#000000', '#ffffff',
    '#f6f8fb', '#ffffff', '#28415e', '#4b6b8c', '#eef4fb', '#edf8f1',
    '#2e7d5a', '#fff3f1', '#b85644', '#fff7e8', '#9a6a12', '#18324a',
    '#496079', '#3e556f', '#597089', '#4f6b88', '#7d8ea3', '#c8d3df'
  ])
};
const ALLOWED_FONT_WEIGHTS = new Set([400, 600, 700]);

// ---------- 工具 ----------
function listCases() {
  return readdirSync(CASES_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => JSON.parse(readFileSync(join(CASES_DIR, f), 'utf8')));
}

function loadSvg(side, id) {
  const p = join(OUT_DIR, side, `${id}.svg`);
  if (!existsSync(p)) return null;
  return readFileSync(p, 'utf8');
}

function extractSpec(svg) {
  const m = svg.match(/<!--\s*spec\s*\n([\s\S]*?)\n\s*-->/);
  if (!m) return null;
  // 简易 YAML 解析：只取顶层 key: value
  const spec = {};
  for (const line of m[1].split('\n')) {
    const mm = line.match(/^\s*([a-zA-Z_]+)\s*:\s*(.+?)\s*$/);
    if (mm) spec[mm[1]] = mm[2].replace(/^["']|["']$/g, '');
  }
  return spec;
}

function extractFontWeights(svg) {
  const weights = new Set();
  // 1. style 块里的 font-weight: NNN
  for (const m of svg.matchAll(/font-weight\s*:\s*(\d+)/g)) {
    weights.add(parseInt(m[1], 10));
  }
  // 2. font 简写 "700 14px ..." 里的字重
  for (const m of svg.matchAll(/font\s*:\s*(\d{3})\s+\d+px/g)) {
    weights.add(parseInt(m[1], 10));
  }
  // 3. font-weight="..."
  for (const m of svg.matchAll(/font-weight\s*=\s*"(\d+)"/g)) {
    weights.add(parseInt(m[1], 10));
  }
  return weights;
}

function extractColors(svg) {
  const cols = new Set();
  for (const m of svg.matchAll(/#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b/g)) {
    let h = m[0].toLowerCase();
    if (h.length === 4) h = '#' + [...h.slice(1)].map(c => c + c).join('');
    cols.add(h);
  }
  return cols;
}

function viewBox(svg) {
  const m = svg.match(/viewBox\s*=\s*"([^"]+)"/);
  if (!m) return null;
  const [x, y, w, h] = m[1].split(/\s+/).map(Number);
  return { x, y, w, h };
}

function extractEdges(svg) {
  // 简单抓 <path class="edge..."> 元素
  return [...svg.matchAll(/<path[^>]*class="[^"]*\bedge\b[^"]*"[^>]*>/g)].map(m => m[0]);
}

function extractEdgeSoft(svg) {
  return [...svg.matchAll(/<path[^>]*class="[^"]*\bedge-soft\b[^"]*"[^>]*>/g)].map(m => m[0]);
}

// ---------- 单项检查 ----------
const CHECKS = {
  spec_block_present(svg) {
    return { pass: !!extractSpec(svg), detail: extractSpec(svg) ? 'found' : 'missing <!-- spec --> block' };
  },
  spec_type_equals(svg, args) {
    const spec = extractSpec(svg);
    if (!spec) return { pass: false, detail: 'no spec' };
    return { pass: spec.type === args.value, detail: `spec.type=${spec.type}` };
  },
  viewBox_format(svg) {
    const vb = viewBox(svg);
    if (!vb) return { pass: false, detail: 'no viewBox' };
    return { pass: vb.x === 0 && vb.y === 0 && vb.w >= 400 && vb.h >= 300, detail: `${vb.w}x${vb.h}` };
  },
  palette_subset(svg, args) {
    const allowed = PALETTES[args.palette];
    if (!allowed) return { pass: false, detail: `unknown palette ${args.palette}` };
    const used = extractColors(svg);
    const stray = [...used].filter(c => !allowed.has(c));
    return { pass: stray.length === 0, detail: stray.length ? `stray: ${stray.slice(0, 5).join(',')}` : `${used.size} colors all valid` };
  },
  font_weight_in(svg, args) {
    const used = extractFontWeights(svg);
    const allowed = new Set(args.allowed);
    const stray = [...used].filter(w => !allowed.has(w));
    return { pass: stray.length === 0, detail: stray.length ? `stray: ${stray.join(',')}` : `weights: ${[...used].join(',')}` };
  },
  no_text_overflow(svg) {
    // 粗判：任何 text x 坐标 > viewBox.w - 8 视为溢出嫌疑
    const vb = viewBox(svg);
    if (!vb) return { pass: false, detail: 'no viewBox' };
    const overflows = [];
    for (const m of svg.matchAll(/<text[^>]*\sx="(-?\d+(?:\.\d+)?)"/g)) {
      const x = parseFloat(m[1]);
      if (x > vb.w - 8 || x < 8) overflows.push(x);
    }
    return { pass: overflows.length === 0, detail: overflows.length ? `${overflows.length} text x out of bounds` : 'ok' };
  },
  edge_ids_stable(svg) {
    const edges = extractEdges(svg);
    if (edges.length === 0) return { pass: true, detail: 'no edges' };
    const withId = edges.filter(e => /\bid="/.test(e) && /\bdata-edge-id="/.test(e));
    return { pass: withId.length === edges.length, detail: `${withId.length}/${edges.length} edges have stable id` };
  },
  legend_present_if_mixed_edges(svg) {
    const hasSoft = extractEdgeSoft(svg).length > 0;
    const hasNormal = extractEdges(svg).length > extractEdgeSoft(svg).length;
    if (!(hasSoft && hasNormal)) return { pass: true, detail: 'edges not mixed, legend not required' };
    const hasLegend = /\b(legend|图例)\b/i.test(svg) || /class="legend/.test(svg);
    return { pass: hasLegend, detail: hasLegend ? 'legend found' : 'mixed edges but no legend' };
  },
  decision_branches_labeled(svg) {
    // 启发式：若存在带 'decision' 类名的元素，每个出边应有 data-edge-label 或紧邻 text
    const decisions = [...svg.matchAll(/class="[^"]*\bdecision\b[^"]*"/g)];
    if (decisions.length === 0) return { pass: true, detail: 'no decision nodes' };
    // 这里给出简易判定：检查是否存在 data-edge-label 属性
    const labeledEdges = [...svg.matchAll(/data-edge-label="[^"]+"/g)];
    return { pass: labeledEdges.length >= 2, detail: `${labeledEdges.length} labeled edges, ${decisions.length} decision nodes` };
  },
  edges_have_payload_labels(svg) {
    const edges = extractEdges(svg);
    if (edges.length === 0) return { pass: true, detail: 'no edges' };
    const labeled = [...svg.matchAll(/data-edge-label="[^"]+"/g)];
    return { pass: labeled.length >= Math.max(3, Math.floor(edges.length * 0.6)), detail: `${labeled.length}/${edges.length} edges labeled` };
  },
  regions_count_in(svg, args) {
    const regions = [...svg.matchAll(/class="(phase|region)"/g)];
    return { pass: regions.length >= args.min && regions.length <= args.max, detail: `${regions.length} regions` };
  },
  participants_count_in(svg, args) {
    const lifelines = [...svg.matchAll(/class="[^"]*\blifeline\b/g)];
    return { pass: lifelines.length >= args.min && lifelines.length <= args.max, detail: `${lifelines.length} lifelines` };
  },
  transitions_have_guards(svg) {
    const edges = extractEdges(svg);
    if (edges.length === 0) return { pass: false, detail: 'no transitions' };
    const guards = [...svg.matchAll(/data-guard="[^"]+"/g)];
    return { pass: guards.length >= Math.floor(edges.length * 0.5), detail: `${guards.length}/${edges.length} have guards` };
  },
  has_initial_and_final_states(svg) {
    const initial = /class="[^"]*\binitial\b/.test(svg);
    const final = /class="[^"]*\bfinal\b/.test(svg);
    return { pass: initial && final, detail: `initial=${initial} final=${final}` };
  },
  matrix_rows_count_in(svg, args) {
    const rows = [...svg.matchAll(/class="[^"]*\brow-(bg|alt)\b/g)];
    return { pass: rows.length >= args.min && rows.length <= args.max, detail: `${rows.length} rows` };
  },
  matrix_cols_count_in(svg, args) {
    const headers = [...svg.matchAll(/class="header"/g)];
    return { pass: headers.length >= args.min && headers.length <= args.max, detail: `${headers.length} header cells` };
  },
  actors_outside_boundary(svg) {
    const hasActors = /class="[^"]*\bactor\b/.test(svg);
    const hasBoundary = /class="[^"]*\bsystem-boundary\b/.test(svg);
    return { pass: hasActors && hasBoundary, detail: `actors=${hasActors} boundary=${hasBoundary}` };
  }
};

// ---------- 主流程 ----------
function runCheck(svg, check) {
  const fn = CHECKS[check.kind];
  if (!fn) return { pass: false, detail: `unknown check: ${check.kind}` };
  try {
    return fn(svg, check);
  } catch (e) {
    return { pass: false, detail: `error: ${e.message}` };
  }
}

function main() {
  const arg = process.argv[2];
  const sides = arg === 'before' ? ['before'] : arg === 'after' ? ['after'] : ['before', 'after'];
  const cases = listCases();

  const rows = [['case', 'check', ...sides.map(s => `${s}_pass`), ...sides.map(s => `${s}_detail`)]];
  const summary = {};
  for (const s of sides) summary[s] = { total: 0, pass: 0 };

  for (const c of cases) {
    const svgs = {};
    for (const s of sides) svgs[s] = loadSvg(s, c.id);

    for (const check of c.automated_checks) {
      const row = [c.id, JSON.stringify(check)];
      const passes = [];
      const details = [];
      for (const s of sides) {
        if (svgs[s] === null) {
          passes.push('NA');
          details.push('missing svg');
        } else {
          const r = runCheck(svgs[s], check);
          passes.push(r.pass ? 'Y' : 'N');
          details.push(r.detail);
          summary[s].total++;
          if (r.pass) summary[s].pass++;
        }
      }
      row.push(...passes, ...details);
      rows.push(row);
    }
  }

  // CSV 输出
  const csv = rows.map(r => r.map(v => `"${String(v).replace(/"/g, '""')}"`).join(',')).join('\n');
  const reportPath = join(ROOT, 'report.csv');
  import('node:fs').then(fs => fs.writeFileSync(reportPath, csv));

  // 控制台摘要
  console.log('\n=== 评测摘要 ===');
  for (const s of sides) {
    const r = summary[s];
    const pct = r.total ? ((r.pass / r.total) * 100).toFixed(1) : 'N/A';
    console.log(`  ${s}: ${r.pass}/${r.total} (${pct}%)`);
  }
  if (sides.length === 2) {
    const delta = summary.after.pass - summary.before.pass;
    console.log(`  delta: ${delta >= 0 ? '+' : ''}${delta} 项检查改善`);
  }
  console.log(`\nreport.csv 已写入: ${reportPath}`);
}

main();
