from services.games import get_active_games, get_daily_game
from unittest.mock import patch

@patch("app.services.games.query_supabase")
def test_get_active_games(mock_query):
    # Mock response data
    mock_query.return_value.execute.return_value.data = [
        {"id": 1, "status": "active", "game_type_id": "connections"}
    ]
    
    result = get_active_games()
    assert len(result) == 1
    assert result[0].game_type_id == "connections"

@patch("app.services.games.query_supabase")
def test_get_daily_game(mock_query):
    # Mock response data
    mock_query.return_value.select.return_value.eq.return_value.eq.return_value.eq.return_value.single.return_value.execute.return_value.data = {
        "id": 1,
        "game_type_id": "connections",
        "game_date": "2025-01-09",
    }

    result = get_daily_game("connections")
    assert result.game_type_id == "connections"
    assert result.game_date == "2025-01-09"
