# Finance Skills 安装与使用

上游：[himself65/finance-skills](https://github.com/himself65/finance-skills)，MIT 许可。
本仓库在 2026-10-04 安装其 26 个 skill；2026-10-09 删除 `finance-skill-creator`、`generative-ui` 的 active 入口后，保留 24 个。上游版本见 `vendor/skills/himself65/finance-skills/SYNC.md`。

- 源快照：`vendor/skills/himself65/finance-skills/`，由同步脚本维护，不直接修改。
- Codex 入口：`skills/finance/*/SKILL.md`，由 registry 登记并链接到 `~/.codex/skills/`。
- 创建或优化 skill 使用 Codex 内置 `skill-creator`；上游 `skill-creator`、`generative-ui` 仅保留在镜像中，不安装。
- `tradingview-mcp`、`sepa-strategy` 允许自动匹配，其余 22 个金融入口仅通过 `$skill-name` 手动调用；策略位于 wrapper 的 `agents/openai.yaml`。
- 本次只启用 Codex；其它 skill 的账户、付费 API、桌面应用或 CLI 依赖按使用需要配置。

## 更新与验证

```bash
./scripts/sync-vendored-skills.sh source-finance-skills
./install.sh
./scripts/audit-global-skills.sh
```

同步后检查 wrapper 的相对路径、skill 数量和上游 MCP 配置是否改变，并运行 quick validation。

## TradingView 数据服务

仅安装 skill 不会加载 Claude 插件里的 `.mcp.json`。本次另行登记只读服务 `finance-tradingview`，采用上游固定版本，使用 Python 3.13；上游不支持 Python 3.14。

```bash
codex mcp add finance-tradingview -- uvx --python 3.13 --from git+https://github.com/atilaahmettaner/tradingview-mcp@d77db101edc1b57b260450ddda5ca4f7f0211ecd tradingview-mcp
```

新的 skill 入口在下一轮可被发现；MCP 原生工具需要新会话加载。当前会话也能通过 wrapper 附带的 stdio 客户端调用同一服务：

```bash
uv run --python 3.13 --with 'mcp>=1.14,<2' python skills/finance/tradingview-mcp/scripts/query.py --list
uv run --python 3.13 --with 'mcp>=1.14,<2' python skills/finance/tradingview-mcp/scripts/query.py --tool coin_analysis --arguments '{"symbol":"BTCUSDT.P","exchange":"BINANCE","timeframe":"4h"}'
```

## 币安永续合约分析

USDT 本位 BTC、ETH 永续符号分别为 `BINANCE:BTCUSDT.P`、`BINANCE:ETHUSDT.P`。不要混用现货符号。
先核对来源、币种、交易所、合约类型和更新时间，再比较多周期指标。
资金费率、未平仓量、多空比例和强平数据需要另外核验。若交易所接口受限或某字段缺失，应明确报告；不能从 RSI、MACD 或自动 BUY/SELL 标签推断这些数据。
