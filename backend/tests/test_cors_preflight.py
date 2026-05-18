from fastapi.testclient import TestClient

from app.main import app


def test_chat_cors_preflight_allows_local_svelte_dev_server():
    client = TestClient(app)

    response = client.options(
        "/chat",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "POST" in response.headers["access-control-allow-methods"]
