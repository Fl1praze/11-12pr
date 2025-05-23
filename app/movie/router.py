from fastapi import APIRouter,HTTPException
from app.movie.schemas import MovieSchemas

from app.movie.dao import MovieDAO

router = APIRouter(prefix='/movies',tags=['Фильмы'])


@router.get('')
async def get_movie():
    result = MovieDAO.find_all()
    return await result

@router.post('')
async def get_movie(data: MovieSchemas):
    await MovieDAO.add(**data.model_dump())
    return {"message": "Movie added successfully"}

@router.get("/{id}")
async def get_movie_by_id(id:int):
    result = MovieDAO.find_by_id(id)
    return await result

@router.put("/{id}")
async def update_movie(id: int, product_data: MovieSchemas):
    existing_movie = await MovieDAO.find_by_id(id)
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    update_data = product_data.dict(exclude_unset=True)
    await MovieDAO.update(id, **update_data)
    return {"message": "Movie updated successfully"}


@router.delete('/{id}')
async def delete_movie(id:int):
    existing_movie = await MovieDAO.find_by_id(id)
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await MovieDAO.delete(id)
    return {"message": "Movie deleted successfully"}