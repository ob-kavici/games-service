from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class GameState(BaseModel):
    user_id: str = Field(..., description="The ID of the user", example="user_12345")
    game_id: int = Field(..., description="The ID of the game", example=1)
    started_at: datetime = Field(..., description="The datetime when the game started", example="2023-10-01T12:00:00")
    ended_at: Optional[datetime] = Field(None, description="The datetime when the game ended", example="2023-10-01T13:00:00")
    game_completed: bool = Field(False, description="Whether the game is completed", example=True)
    game_won: bool = Field(False, description="Whether the game was won", example=True)
    game_data: Optional[dict] = Field(None, description="Additional data related to the game", example={"score": 100, "level": 5})