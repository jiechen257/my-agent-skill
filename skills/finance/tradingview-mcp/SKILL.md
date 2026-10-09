---
name: tradingview-mcp
description: "Query TradingView quotes, technical indicators, multi-timeframe alignment, scans, and backtests without the desktop app."
---

# tradingview-mcp

Repository routing wrapper for `himself65/finance-skills` (`tradingview-mcp`).

Read `../../../vendor/skills/himself65/finance-skills/plugins/data-providers/skills/tradingview-mcp/SKILL.md` completely and follow it. Resolve upstream bundled files from `../../../vendor/skills/himself65/finance-skills/plugins/data-providers/skills/tradingview-mcp/`, relative to this wrapper. Keep upstream snapshots unchanged; local compatibility overrides belong here.

## Codex compatibility

Skill-only installation does not auto-load upstream plugin `.mcp.json`. The upstream read-only server is registered separately as `finance-tradingview`; use that namespace in Codex. Pin Python to 3.13 because upstream excludes 3.14.

When the namespace is unavailable in the current chat, use the same upstream MCP server via the bundled stdio client. This is a transport fallback, retaining upstream validation and error handling:

```bash
uv run --python 3.13 --with 'mcp>=1.14,<2' python scripts/query.py --list
uv run --python 3.13 --with 'mcp>=1.14,<2' python scripts/query.py --tool coin_analysis --arguments '{"symbol":"BTCUSDT.P","exchange":"BINANCE","timeframe":"4h"}'
```

Resolve `scripts/query.py` relative to this wrapper. For Binance USDT perpetuals explicitly use `BINANCE:BTCUSDT.P` and `BINANCE:ETHUSDT.P`. Funding, open interest, liquidation and account-position data require a verified source; indicators alone do not establish leverage positioning. Distinguish source update time from fetch time.

## Interpretation checks

- Upstream `timestamp: real-time` is a label, not an exchange update timestamp. State fetch time and disclose that the exact source update time is absent.
- `change_percent` / `change_pct` uses the current candle's open and close; it is not a rolling 24-hour return.
- A `Normal` volume signal with a missing average or ratio cannot establish volume confirmation. The OBV direction is inferred from a single candle and is not a measured OBV trend.
- `macd.crossover` indicates which line is currently above the other. Likewise, an EMA50 > EMA200 relation does not establish that a cross just occurred.
- Automatic BUY/SELL labels and High confidence are rule-based classifications, not calibrated probabilities or executable trade instructions. Check contradictory indicators and contract-specific positioning before interpreting them.
