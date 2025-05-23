from fastapi import APIRouter,HTTPException


from app.session.dao import SessionDAO

router = APIRouter(prefix='/sessions',tags=['Сеансы'])


@router.get('')
async def get_sessions():
    result = SessionDAO.find_all()
    return await result

@router.get("/{id}")
async def get_sessions_by_id(id:int):
    result = SessionDAO.find_by_id(id)
    return await result

@router.delete('/{id}')
async def delete_sessions(id:int):
    existing_movie = await SessionDAO.find_by_id(id)
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Sessions not found")
    await SessionDAO.delete(id)
    return {"message": "Sessions deleted successfully"}