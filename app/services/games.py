from app.core.dependencies import get_supabase_client
from app.models.game import *

GAMES_METADATA_COLUMNS = "id, created_at, status, editor_id, stars, game_type, game_date"

def get_game_types() -> list[GameType]:
    supabase = get_supabase_client()
    response = supabase.table("game-types").select("*").order("is_active", desc=True).execute()
    return [GameType(**game_type) for game_type in response.data]

def get_active_games() -> list[GameMetadata]:
    supabase = get_supabase_client()
    response = supabase.table("games").select(GAMES_METADATA_COLUMNS).eq("status", GameStatus.ACTIVE.value).execute()
    return [GameMetadata(**game) for game in response.data]

def get_active_games_by_type(game_type: str) -> list[GameMetadata]:
    supabase = get_supabase_client()
    response = supabase.table("games").select(GAMES_METADATA_COLUMNS).eq("game_type", game_type).eq("status", GameStatus.ACTIVE.value).execute()
    return [GameMetadata(**game) for game in response.data]

def get_daily_game_by_type(game_type: str) -> GameMetadata:
    game_date = date.today()
    supabase = get_supabase_client()
    response = supabase.table("games").select(GAMES_METADATA_COLUMNS).eq("game_type", game_type).eq("status", GameStatus.ACTIVE.value).eq("game_date", game_date).single().execute()
    return GameMetadata(**response.data)

def get_game_data_by_id(game_type, game_id: int) -> GameData | None:
    supabase = get_supabase_client()
    response = supabase.table("games").select("game_data").eq("game_type", game_type).eq("id", game_id).single().execute()
    return GameData(**response.data)
