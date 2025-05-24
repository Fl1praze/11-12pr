from fastapi import APIRouter,HTTPException
from app.movie.schemas import MovieSchemas
from datetime import timezone
from app.movie.time_utils import to_moscow_time

from app.movie.dao import MovieDAO
from app.halls.dao import HallDAO

router = APIRouter(prefix='/movies',tags=['Movie 🎥'])


@router.get('')
async def get_movie():
    '''Получение фильмов'''
    result = MovieDAO.find_all()
    return await result

@router.post("")
async def get_movie(data: MovieSchemas):
    '''
    Добавление новых фильмов
    '''
    #Делаем время в мск
    if data.start_time.tzinfo is not None:
        data.start_time = data.start_time.astimezone(timezone.utc).replace(tzinfo=None)
    data.start_time = to_moscow_time(data.start_time)

    #Преобразование duration из строки 'HH:MM' в формат 'HH:MM'
    try:
        hours, minutes = map(int, data.duration.split(':'))
        if hours < 0 or minutes < 0 or minutes >= 60:
            raise ValueError("Invalid time format")
        data.duration = f"{hours:02}:{minutes:02}"
    except ValueError:
        raise HTTPException(status_code=400, detail="Duration must be in the format 'HH:MM'")
    #Проверка наличия зала

    hall_exists = await HallDAO.find_by_id(data.hall_id)
    if not hall_exists:
        raise HTTPException(status_code=404, detail="Hall not found")

    #Сохранение фильма
    await MovieDAO.add(**data.model_dump())
    return {"message": "Movie added successfully"}

@router.get("/{id}")
async def get_movie_by_id(id:int):
    '''
    Получение фильма по id
    '''
    result = MovieDAO.find_by_id(id)
    return await result

@router.put("/{id}")
async def update_movie(id: int, product_data: MovieSchemas):
    '''Изменить фильм по id'''
    existing_movie = await MovieDAO.find_by_id(id)
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    update_data = product_data.dict(exclude_unset=True)
    await MovieDAO.update(id, **update_data)
    return {"message": "Movie updated successfully"}


@router.delete('/{id}')
async def delete_movie(id:int):
    '''Удалить фильм по id'''
    existing_movie = await MovieDAO.find_by_id(id)
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await MovieDAO.delete(id)
    return {"message": "Movie deleted successfully"}