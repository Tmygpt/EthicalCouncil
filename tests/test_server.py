import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities
from models.json_rpc import JSONRPCResponse


def make_server():
    card = AgentCard(
        name="n",
        description="d",
        url="u",
        version="1",
        capabilities=AgentCapabilities(),
        skills=[],
    )
    return A2AServer(agent_card=card, task_manager=None)


def test_get_agent_card():
    srv = make_server()
    response = srv._get_agent_card(None)
    assert response.status_code == 200
    import json
    data = json.loads(response.body)
    assert data["name"] == "n"


def test_create_response():
    srv = make_server()
    resp = JSONRPCResponse(id="1", result={"foo": "bar"})
    out = srv._create_response(resp)
    assert out.status_code == 200
    import json
    data = json.loads(out.body)
    assert data["result"]["foo"] == "bar"