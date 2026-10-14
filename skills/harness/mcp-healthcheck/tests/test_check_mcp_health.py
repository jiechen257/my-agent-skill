from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-mcp-health.sh"


class MCPHealthcheckTest(unittest.TestCase):
    def run_helper(self, compare: str | None = None) -> tuple[subprocess.CompletedProcess[str], list[dict]]:
        with tempfile.TemporaryDirectory(prefix="mcp-healthcheck-") as directory:
            root = Path(directory)
            config = root / "config.toml"
            config.write_text('[mcp_servers.demo]\nurl = "https://mcp.example.com/mcp"\n', encoding="utf-8")
            log = root / "requests.jsonl"
            curl = root / "curl"
            curl.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "with open(os.environ['MCP_TEST_REQUEST_LOG'], 'a') as output:\n"
                "    output.write(json.dumps({'args': sys.argv[1:], 'proxy': bool(os.getenv('HTTP_PROXY'))}) + '\\n')\n"
                "print('200 application/json 0.001s', end='')\n",
                encoding="utf-8",
            )
            curl.chmod(0o755)
            env = {**os.environ, "PATH": f"{root}{os.pathsep}{os.environ['PATH']}",
                   "CODEX_CONFIG": str(config), "MCP_TEST_REQUEST_LOG": str(log),
                   "HTTP_PROXY": "http://proxy.example.com:8080"}
            env.pop("MCP_HEALTHCHECK_NO_PROXY", None)
            if compare is not None:
                env["MCP_HEALTHCHECK_NO_PROXY"] = compare
            result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True, check=False)
            requests = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            return result, requests

    def test_default_preserves_proxy_and_makes_only_two_probes(self) -> None:
        result, requests = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(requests), 2)
        self.assertTrue(all(request["proxy"] for request in requests))
        self.assertIn("-I", requests[0]["args"])
        self.assertIn("-d", requests[1]["args"])
        self.assertNotIn("no-proxy HEAD", result.stdout)

    def test_explicit_comparison_adds_two_proxy_stripped_probes(self) -> None:
        result, requests = self.run_helper("1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([request["proxy"] for request in requests], [True, True, False, False])
        self.assertIn("no-proxy HEAD", result.stdout)
        self.assertIn("no-proxy init", result.stdout)

    def test_invalid_option_fails_before_network_probes(self) -> None:
        result, requests = self.run_helper("invalid")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(requests, [])
        self.assertIn("must be 0 or 1", result.stderr)


if __name__ == "__main__":
    unittest.main()
