from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime, date
from enum import Enum

class GameStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    PENDING = "pending"

class GameType(BaseModel):
    id: str = Field(..., description="Unique identifier for the game type", examples=["puzzle"])
    title: str = Field(..., description="Title of the game type", examples=["Daily Puzzle"])
    description: str = Field(..., description="Description of the game type", examples=["A challenging daily puzzle to test your skills."])
    is_active: bool = Field(..., description="Indicates if the game type is currently active", examples=[True])

class GameMetadata(BaseModel):
    id: int = Field(..., description="Unique identifier for the game", examples=[123])
    created_at: datetime = Field(..., description="Timestamp when the game was created", examples=["2025-01-11T09:49:03"])
    status: GameStatus = Field(..., description="Current status of the game", examples=["active"])
    editor_id: Optional[str] = Field(None, description="Identifier of the editor who created the game", examples=["editor_456"])
    stars: int = Field(..., description="Star rating of the game", examples=[5])
    game_type_id: str = Field(..., description="Identifier for the type of game", examples=["puzzle"])
    game_date: Optional[date] = Field(None, description="The date associated with the game", examples=["2025-01-11"])

class Game(GameMetadata):
    game_data: Optional[Dict] = Field(None, description="Detailed data specific to the game", examples=[{"level": 1, "difficulty": "easy"}])
