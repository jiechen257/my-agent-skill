"""Query the upstream read-only TradingView MCP server from a current chat."""

import argparse
import asyncio
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def server_parameters():
    root = Path(__file__).resolve().parents[4]
    config = root / "vendor/skills/himself65/finance-skills/plugins/data-providers/.mcp.json"
    server = json.loads(config.read_text())["mcpServers"]["tradingview"]
    command = shutil.which(server["command"])
    if command is None:
        raise RuntimeError("uvx is required; install uv before querying TradingView")
    return StdioServerParameters(command=command, args=["--python", "3.13", *server["args"]])


async def query(args):
    async with stdio_client(server_parameters()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            if args.list:
                result = (await session.list_tools()).model_dump(mode="json")
            else:
                result = (await session.call_tool(args.tool, json.loads(args.arguments))).model_dump(mode="json")
            print(json.dumps({"fetched_at_utc": datetime.now(timezone.utc).isoformat(), "result": result}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--list", action="store_true")
    action.add_argument("--tool")
    parser.add_argument("--arguments", default="{}", help="Tool arguments as JSON")
    asyncio.run(query(parser.parse_args()))


if __name__ == "__main__":
    main()
