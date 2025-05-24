from fastapi import APIRouter, HTTPException
from app.halls.dao import HallDAO
from app.halls.schemas import SHallCreate, SHallRead
from typing import List

router = APIRouter(prefix='/halls', tags=['Залы 🎦'])

@router.post("")
async def create_hall(hall_data: SHallCreate):
    # Проверяем, существует ли зал с таким именем
    existing_hall = await HallDAO.find_one_or_none(name=hall_data.name)
    if existing_hall:
        raise HTTPException(status_code=400, detail=f"Зал с названием '{hall_data.name}' уже существует")
    # Создаем новый зал
    await HallDAO.add(**hall_data.model_dump())
    return {"message": "Зал успешно создан"}

@router.get("", response_model=List[SHallRead])
async def get_all_halls():
    """Получить список всех залов"""
    return await HallDAO.find_all()

@router.get("/{hall_id}", response_model=SHallRead)
async def get_hall(hall_id: int):
    """Получить информацию о конкретном зале"""
    hall = await HallDAO.find_by_id(hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Зал не найден")
    return hall

@router.delete("/{hall_id}")
async def delete_hall(hall_id: int):
    """Удалить зал"""
    hall = await HallDAO.find_by_id(hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Зал не найден")
    await HallDAO.delete(hall_id)
    return {"message": "Зал успешно удален"}


