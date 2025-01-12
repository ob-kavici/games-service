import asyncio
import json
from fastapi import HTTPException
from postgrest.exceptions import APIError
from core.dependencies import *
from models.game import *
from models.gamestate import *
from typing import Optional
from datetime import date
import aio_pika
import logging

logging.basicConfig(level=logging.INFO)

GAMES_METADATA_COLUMNS = "id, created_at, status, editor_id, stars, game_type_id, game_date"

def query_supabase(table: str, auth: dict = None):
    supabase = get_supabase_client(auth)
    return supabase.table(table)


def get_game_types(game_type_id: Optional[str] = None) -> list[GameType] | GameType:
    query = query_supabase("game-types").select("*").order("is_active", desc=True)
    if game_type_id:
        query = query.eq("id", game_type_id)
        response = query.single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Game type not found")
        return GameType(**response.data)
    response = query.execute()
    return [GameType(**game_type) for game_type in response.data]


def get_active_games(game_type_id: Optional[str] = None) -> list[GameMetadata]:
    query = query_supabase("games").select(GAMES_METADATA_COLUMNS).eq("status", GameStatus.ACTIVE.value)
    if game_type_id:
        query = query.eq("game_type_id", game_type_id)
    response = query.execute()
    return [GameMetadata(**game) for game in response.data]


def get_daily_game(game_type_id: str) -> Game:
    response = (
        query_supabase("games")
        .select("*")
        .eq("game_type_id", game_type_id)
        .eq("status", GameStatus.ACTIVE.value)
        .eq("game_date", date.today())
        .single()
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="Daily game not found")
    return Game(**response.data)


def get_game(game_type_id: str, game_id: int) -> Game | None:
    response = (
        query_supabase("games")
        .select("*")
        .eq("game_type_id", game_type_id)
        .eq("id", game_id)
        .single()
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="Game not found")
    return Game(**response.data)


def get_game_state(user_id: str, game_id: int, auth: dict) -> GameState | None:
    try:
        response = (
            query_supabase("game-states", auth)
            .select("*")
            .eq("user_id", user_id)
            .eq("game_id", game_id)
            .single()
            .execute()
        )
        return GameState(**response.data) if response.data else None
    except APIError as e:
        if "PGRST116" in str(e):
            return None
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

def update_game_state(game_state: dict, auth: dict) -> GameState | None:
    print("UPDATE GAME STATE")
    print("Input game state:", game_state)

    if "game_id" not in game_state or "user_id" not in game_state:
        raise HTTPException(status_code=400, detail="Missing required fields: 'game_id' or 'user_id' in game_state")

    user_id = game_state["user_id"]
    game_id = game_state["game_id"]

    # Check if game state exists
    existing_state = get_game_state(user_id, game_id, auth)
    if not existing_state:
        try:
            response = (
                query_supabase("game-states", auth)
                .insert(game_state)
                .execute()
            )
            print(response)
            # Publish event to RabbitMQ
            asyncio.create_task(publish_event(GameState(**response.data[0])))
            return GameState(**response.data[0])
        except APIError as e:
            raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    
    # Update game state
    try:
        response = (
            query_supabase("game-states", auth)
            .update(game_state)
            .eq("user_id", user_id)
            .eq("game_id", game_id)
            .execute()
        )
        print(response)
        # Publish event to RabbitMQ
        asyncio.create_task(publish_event(GameState(**response.data[0])))
        return GameState(**response.data[0])
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

async def publish_event(event_data: GameState):
    try:
        connection = await aio_pika.connect_robust(get_rabbitmq_url())
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(event_data.model_dump(), default=str).encode()),
                routing_key="game.states",
            )
    except Exception as e:
        logging.error(f"Failed to publish event: {str(e)}")
