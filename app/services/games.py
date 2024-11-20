from app.core.dependencies import get_supabase_client
from app.models.game import GameType, Game

def get_game_types() -> list[GameType]:
    supabase = get_supabase_client()
    response = supabase.table("game_types").select("*").execute()
    return response.data

def get_game_type_by_title(game_type_title: str) -> GameType:
    supabase = get_supabase_client()
    response = supabase.table("game_types").select("*").eq("title", game_type_title).execute()
    return response.data[0]

def get_games_by_type(game_type_title: str) -> list[Game]:
    supabase = get_supabase_client()
    game_type = get_game_type_by_title(game_type_title)
    response = supabase.table("games").select("*").eq("game_type_id", game_type["id"]).execute()
    return response.data

def get_game_by_id(game_id: int) -> Game:
    supabase = get_supabase_client()
    response = supabase.table("games").select("*").eq("game_id", game_id).execute()
    print(response.data)
    return response.data[0]