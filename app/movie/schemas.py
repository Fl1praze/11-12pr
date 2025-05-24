from datetime import datetime, timedelta

from pydantic import BaseModel



class MovieSchemas(BaseModel):
    title: str
    hall_id:int
    start_time:datetime
    duration: str  # Accept duration as 'HH:MM'


    class Config:
        from_attributes = True