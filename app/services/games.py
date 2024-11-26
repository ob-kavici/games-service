from core.dependencies import get_supabase_client
from models.game import *

GAMES_METADATA_COLUMNS = "id, created_at, status, editor_id, game_type, stars"

def get_game_types() -> list[GameType]:
    supabase = get_supabase_client()
    response = supabase.table("game-types").select("*").execute()
    print(response)
    return [GameType(**game_type) for game_type in response.data]

def get_active_games() -> list[GameMetadata]:
    supabase = get_supabase_client()
    response = supabase.table("games").select(GAMES_METADATA_COLUMNS).eq("status", GameStatus.ACTIVE.value).execute()
    print(response.data)
    return [GameMetadata(**game) for game in response.data]

def get_active_games_by_type(game_type: str) -> list[GameMetadata]:
    supabase = get_supabase_client()
    response = supabase.table("games").select(GAMES_METADATA_COLUMNS).eq("game_type", game_type).eq("status", GameStatus.ACTIVE.value).execute()
    return [GameMetadata(**game) for game in response.data]

def get_game_by_id(game_type, game_id: int) -> Game | None:
    supabase = get_supabase_client()
    response = supabase.table("games").select("*").eq("game_type", game_type).eq("id", game_id).execute()
    if len(response.data) == 0:
        return None
    return Game(**response.data[0])
