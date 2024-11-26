from fastapi import APIRouter
import services.games as GamesService
from models.game import *

router = APIRouter()

@router.get("/game-types")
async def get_game_types() -> list[GameType]:
    return GamesService.get_game_types()

@router.get("")
async def get_active_games() -> list[GameMetadata]:
    return GamesService.get_active_games()

@router.get("/{game_type}")
async def get_active_games_by_type(game_type: str) -> list[GameMetadata]:
    return GamesService.get_active_games_by_type(game_type)

# TODO: Proper error handling
@router.get("/{game_type}/{game_id}")
async def get_game_by_id(game_type: str, game_id: int) -> Game | None:
    return GamesService.get_game_by_id(game_type, game_id)