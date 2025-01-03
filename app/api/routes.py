from fastapi import APIRouter, Query
from typing import Optional
import services.games as GamesService
from models.game import *

router = APIRouter()

@router.get("/game-types")
async def get_game_types(game_type_id: Optional[str] = Query(None)) -> list[GameType] | GameType:
    return GamesService.get_game_types(game_type_id)

@router.get("/")
async def get_active_games(game_type_id: Optional[str] = Query(None)) -> list[GameMetadata]:
    return GamesService.get_active_games(game_type_id)

@router.get("/{game_type_id}/daily")
async def get_daily_game(game_type_id: str) -> Game:
    return GamesService.get_daily_game(game_type_id)

@router.get("/{game_type_id}/{game_id}")
async def get_game(game_type_id: str, game_id: int) -> Game | None:
    return GamesService.get_game(game_type_id, game_id)
