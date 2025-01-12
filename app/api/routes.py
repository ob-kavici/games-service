from fastapi import APIRouter, Depends, HTTPException, Header, Query
from typing import Optional
import services.games as GamesService
from models.game import *
from models.errors import *
from models.gamestate import *

router = APIRouter()

async def get_auth_headers(
    authorization: Optional[str] = Header(None),
    x_refresh_token: Optional[str] = Header(None),
) -> dict:
    if not authorization or not x_refresh_token:
        raise HTTPException(
            status_code=400,
            detail="Missing JWT or Refresh Token in headers"
        )

    jwt = authorization.replace("Bearer ", "")
    return {"jwt": jwt, "refresh_token": x_refresh_token}

@router.get("/game-types", responses={
    200: {"model": list[GameType], "description": "List of all available game types"},
    400: {"model": ValidationError, "description": "Invalid query parameters provided"},
    404: {"model": NotFoundError, "description": "No game types found"}
})
async def get_game_types(game_type_id: Optional[str] = Query(None)) -> list[GameType] | GameType:
    return GamesService.get_game_types(game_type_id)

@router.get("/", responses={
    200: {"model": list[GameMetadata], "description": "List of all active games"},
    400: {"model": ValidationError, "description": "Invalid query parameters provided"},
    404: {"model": NotFoundError, "description": "No active games found"}
})
async def get_active_games(game_type_id: Optional[str] = Query(None)) -> list[GameMetadata]:
    return GamesService.get_active_games(game_type_id)

@router.get("/{game_type_id}/daily", responses={
    200: {"model": Game, "description": "The daily game for the specified game type"},
    400: {"model": ValidationError, "description": "Invalid game type ID provided"},
    404: {"model": NotFoundError, "description": "Daily game not found for the specified game type"}
})
async def get_daily_game(game_type_id: str) -> Game:
    return GamesService.get_daily_game(game_type_id)

@router.get("/{game_type_id}/{game_id}", responses={
    200: {"model": Game, "description": "Details of the specified game"},
    400: {"model": ValidationError, "description": "Invalid game type ID or game ID provided"},
    404: {"model": NotFoundError, "description": "Game not found for the specified IDs"}
})
async def get_game(game_type_id: str, game_id: int) -> Game | None:
    return GamesService.get_game(game_type_id, game_id)

@router.get("/state", responses={
    200: {"model": GameState, "description": "Current game state for the user"},
    400: {"model": ValidationError, "description": "Invalid request parameters"},
    401: {"model": UnauthorizedError, "description": "Unauthorized access - invalid or missing JWT/refresh token"},
    404: {"model": NotFoundError, "description": "Game state not found"},
    500: {"model": InternalServerError, "description": "Internal server error"}
})
async def get_game_state(
    user_id: str,
    game_id: int,
    auth: dict = Depends(get_auth_headers),
) -> GameState | None:
    return GamesService.get_game_state(user_id, game_id, auth)

@router.post("/state", responses={
    200: {"model": GameState, "description": "Updated game state"},
    400: {"model": ValidationError, "description": "Invalid game state payload"},
    401: {"model": UnauthorizedError, "description": "Unauthorized access - invalid or missing JWT/refresh token"},
    404: {"model": NotFoundError, "description": "Game state not found for update"},
    500: {"model": InternalServerError, "description": "Internal server error"}
})
async def update_game_state(
    game_state: dict,
    auth: dict = Depends(get_auth_headers),
) -> GameState | None:
    print(game_state)
    return GamesService.update_game_state(game_state, auth)
