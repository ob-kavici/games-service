from fastapi import APIRouter
import app.services.games as GamesService
from app.models.game import GameType, Game

router = APIRouter()

# Game Types
@router.get("/game-types")
async def get_game_types() -> list[GameType]:
    return GamesService.get_game_types()

@router.get("/game-types/{game_type_title}")
async def get_game_type_by_title(game_type_title: str) -> GameType:
    return GamesService.get_game_type_by_title(game_type_title)

# Games
@router.get("/games/{game_type_title}")
async def get_games_by_type(game_type_title: str) -> list[Game]:
    return GamesService.get_games_by_type(game_type_title)

@router.get("/games/game/{game_id}")
async def get_game_by_id(game_id: int) -> Game:
    return GamesService.get_game_by_id(game_id)