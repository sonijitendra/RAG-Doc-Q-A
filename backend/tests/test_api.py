from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200

def test_chat():
    r = client.post("/chat/ask", json={"question": "test"})
    assert r.status_code == 200
