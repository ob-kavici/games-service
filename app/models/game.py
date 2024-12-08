from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from enum import Enum

class GameStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    PENDING = "pending"

class GameType(BaseModel):
    id: str
    title: str
    is_active: bool
    
class GameMetadata(BaseModel):
    id: int
    created_at: datetime
    status: GameStatus
    editor_id: Optional[str] = None
    stars: int
    game_type: str
    game_date: Optional[date] = None
    
class GameData(BaseModel):
    game_data: Optional[dict] = None