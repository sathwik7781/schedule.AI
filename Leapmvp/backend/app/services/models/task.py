from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Task(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    due_date: datetime
    priority: int
    category: str
    status: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    user_id: str
    recurring: bool = False
    recurring_pattern: Optional[str] = None
    estimated_duration: int  # in minutes
    tags: List[str] = [] 