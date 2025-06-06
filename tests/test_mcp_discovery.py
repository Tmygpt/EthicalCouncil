import os
import sys
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utilities.mcp.mcp_discovery import MCPDiscovery


def test_mcp_list_servers(tmp_path):
    cfg = tmp_path / "mcp.json"
    data = {"mcpServers": {"srv": {"command": "cmd", "args": []}}}
    cfg.write_text(json.dumps(data))
    disc = MCPDiscovery(config_file=str(cfg))
    assert disc.list_servers() == data["mcpServers"]