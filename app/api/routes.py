from fastapi import APIRouter, Depends, HTTPException, Header, Query
from typing import Optional
import services.games as GamesService
from models.game import *
from models.gamestate import *

router = APIRouter()

# Dependency for extracting JWT and refresh token
async def get_auth_headers(
    authorization: Optional[str] = Header(None),
    x_refresh_token: Optional[str] = Header(None),
) -> dict:
    """
    Extract JWT and refresh token from request headers.
    """
    if not authorization or not x_refresh_token:
        raise HTTPException(status_code=400, detail="Missing JWT or Refresh Token in headers")

    jwt = authorization.replace("Bearer ", "")
    return {"jwt": jwt, "refresh_token": x_refresh_token}

# Routes
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

@router.get("/state")
async def get_game_state(
    user_id: str,
    game_id: int,
    auth: dict = Depends(get_auth_headers),
) -> GameState | None:
    return GamesService.get_game_state(user_id, game_id, auth)

@router.post("/state")
async def update_game_state(
    game_state: dict,
    auth: dict = Depends(get_auth_headers),
) -> GameState | None:
    print(game_state)
    return GamesService.update_game_state(game_state, auth)