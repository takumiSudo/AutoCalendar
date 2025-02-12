from pydantic import BaseModel
from typing import Optional
from dataclasses import dataclass, field

class DataLoader:
    def __init__(self, summary: str, start_time: str, end_time: str, description: Optional[str] = None, location: Optional[str] = None):
        self.summary = summary
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.location = location

# class CalendarEvent(BaseModel):
#     summary: str 
#     start_time: str
#     end_time: str
#     description: str
#     location: str

@dataclass
class EventDateTime:
    dateTime: str
    timeZone: str

@dataclass
class CalendarEvent(BaseModel):
    summary: str
    start: EventDateTime
    end: EventDateTime
    description: Optional[str] 
    location: Optional[str]