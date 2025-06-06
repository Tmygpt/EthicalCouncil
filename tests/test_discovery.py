import os
import sys
import json
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utilities.a2a.agent_discovery import DiscoveryClient

@pytest.mark.asyncio
async def test_list_agent_cards(monkeypatch, tmp_path):
    registry = tmp_path / "registry.json"
    json.dump(["http://agent.test"], registry.open('w'))
    client = DiscoveryClient(registry_file=str(registry))

    fake_card = {
        "name": "Agent",
        "description": "desc",
        "url": "http://agent.test",
        "version": "1",
        "capabilities": {},
        "skills": []
    }

    class DummyHTTPX:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        async def get(self, url, timeout=5.0):
            class Resp:
                def raise_for_status(self):
                    pass
                def json(self):
                    return fake_card
            return Resp()

    monkeypatch.setattr("utilities.a2a.agent_discovery.httpx.AsyncClient", lambda: DummyHTTPX())
    cards = await client.list_agent_cards()
    assert len(cards) == 1
    assert cards[0].name == "Agent"