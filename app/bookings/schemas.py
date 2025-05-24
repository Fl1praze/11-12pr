from pydantic import BaseModel
from typing import List
from pydantic.types import conint
from datetime import datetime
from pydantic import  Field
from typing import Annotated



from pydantic import BaseModel
from pydantic.types import conint
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated

class SMovieInfo(BaseModel):
    id: int
    title: str
    duration: str
    start_time: datetime
    available_seats: int

    class Config:
        from_attributes = True

class SBookingCreate(BaseModel):
    movie_id: int
    seat_numbers: Annotated[int, Field(gt=0)]

class SBooking(BaseModel):
    id: int
    user_id: int
    movie_id: int
    seat_numbers: int
    booking_time: datetime
    status: str
    hall_id: int

    class Config:
        from_attributes = True

class SAvailableSeats(BaseModel):
    id: int
    title: str
    start_time: datetime
    duration: str
    available_seats: List[int]
    total_seats: int

    class Config:
        from_attributes = True

class SUserBooking(BaseModel):
    movie_title: str
    start_time: datetime
    seat_number: int

    class Config:
        from_attributes = True 