from pydantic import BaseModel
from typing import List, Optional

class ChatIntent(BaseModel):
    intent: str  # book_offline_meeting | book_online_meeting
    room_name: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD
    start_time: Optional[str] = None  # HH:MM
    end_time: Optional[str] = None
    participants: List[str] = []
