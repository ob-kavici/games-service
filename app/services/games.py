from core.dependencies import get_supabase_client
from models.game import *

GAMES_METADATA_COLUMNS = "id, created_at, status, editor_id, stars, game_type_id, game_date"

def get_game_types(game_type_id: str = None) -> list[GameType] | GameType:
    supabase = get_supabase_client()
    query = supabase.table("game-types").select("*").order("is_active", desc=True)
    if game_type_id:
        query = query.eq("id", game_type_id)
        response = query.single().execute()
        return GameType(**response.data)
    response = query.execute()
    return [GameType(**game_type) for game_type in response.data]

def get_active_games(game_type_id: str = None) -> list[GameMetadata]:
    supabase = get_supabase_client()
    query = supabase.table("games").select(GAMES_METADATA_COLUMNS).eq("status", GameStatus.ACTIVE.value)
    if game_type_id:
        query = query.eq("game_type_id", game_type_id)
    response = query.execute()
    return [GameMetadata(**game) for game in response.data]

def get_daily_game(game_type_id: str) -> Game:
    game_date = date.today()
    supabase = get_supabase_client()
    response = supabase.table("games").select("*").eq("game_type_id", game_type_id).eq("status", GameStatus.ACTIVE.value).eq("game_date", game_date).single().execute()
    return Game(**response.data)

def get_game(game_type_id, game_id: int) -> Game | None:
    supabase = get_supabase_client()
    response = supabase.table("games").select("*").eq("game_type_id", game_type_id).eq("id", game_id).single().execute()
    return Game(**response.data)
