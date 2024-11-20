from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class GameStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    PENDING = "pending"

class GameType(BaseModel):
    id: int
    title: str
    
class Game(BaseModel):
    game_id: int
    created_at: datetime
    status: str = GameStatus.PENDING
    editor_id: str | None = None
    stars: int
    game_type_id: int