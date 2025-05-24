from pydantic import BaseModel

class SHallCreate(BaseModel):
    """Схема для создания зала"""
    total_seats: int
    name: str

class SHallRead(BaseModel):
    """Схема для чтения информации о зале"""
    id: int
    total_seats: int
    name: str

    class Config:
        from_attributes = True 