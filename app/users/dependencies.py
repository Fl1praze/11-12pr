from datetime import datetime
from fastapi import Request,Depends
from jose import jwt,JWTError
from app.config import settings
from app.users.dao import UsersDAO

from exeptions import *

def get_token(request:Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokeNotCorrectException
    return token


async def get_current_user(token:str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectFormatTokenException
    expire:str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise TokenExpiredException
    user_id:str = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401)
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        HTTPException(status_code=401)
    return user