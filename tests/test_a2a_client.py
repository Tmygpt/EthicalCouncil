import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from client.client import A2AClient, A2AClientHTTPError


class DummyHTTPClient:
    def __init__(self, response):
        self._response = response
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, tb):
        pass
    async def post(self, url, json=None, timeout=None):
        return self._response

class DummyResponse:
    def __init__(self, payload=None, status_error=False):
        self._payload = payload or {}
        self.status_error = status_error
        self.status_code = 500
    def raise_for_status(self):
        if self.status_error:
            import httpx
            raise httpx.HTTPStatusError("boom", request=None, response=self)
    def json(self):
        return self._payload

@pytest.mark.asyncio
async def test_send_task_success(monkeypatch):
    resp = DummyResponse({"result": {"id": "1", "status": {"state": "completed"}, "history": []}})
    monkeypatch.setattr("client.client.httpx.AsyncClient", lambda: DummyHTTPClient(resp))
    client = A2AClient(url="http://x")
    payload = {"id": "1", "sessionId": "s", "message": {"role": "user", "parts": [{"type": "text", "text": "hi"}]}}
    task = await client.send_task(payload)
    assert task.id == "1"

@pytest.mark.asyncio
async def test_send_task_http_error(monkeypatch):
    resp = DummyResponse(status_error=True)
    monkeypatch.setattr("client.client.httpx.AsyncClient", lambda: DummyHTTPClient(resp))
    client = A2AClient(url="http://x")
    payload = {"id": "1", "sessionId": "s", "message": {"role": "user", "parts": [{"type": "text", "text": "hi"}]}}
    with pytest.raises(A2AClientHTTPError):
        await client.send_task(payload)