from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GameState(BaseModel):
    user_id: str
    game_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    game_completed: bool = False
    game_won: bool = False
    game_data: Optional[dict] = None