from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "games-service", "status": "running"}

def test_get_active_games():
    response = client.get("/games")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_daily_game():
    response = client.get("/games/connections/daily")
    if response.status_code == 200:
        data = response.json()
        assert "game_data" in data
        assert data["game_type_id"] == "connections"
    elif response.status_code == 404:
        assert response.json() == {"detail": "Daily game not found"}
