from fastapi import APIRouter, HTTPException,Response,Depends

from app.users.auth import get_password_hash, verify_password, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth
from app.users.models import Users
from app.users.dependencies import get_current_user
router = APIRouter(prefix='/auth',tags =['Auth & Пользователи'])

from exeptions import *

@router.post('/register')
async def register_user(user_data:SUserAuth):
    try_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if try_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email = user_data.email, hashed_password=hashed_password)
    return {"message": "User registered successfully"}

@router.post('/login')
async def login_user(response: Response,user_data:SUserAuth):
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if not user:
        raise UserNotFoundException
    if user:
        password_is_valid = verify_password(user_data.password, user.hashed_password)
        if not password_is_valid:
            raise PasswordNotCorrectException
    access_token =  create_access_token({"sub":str(user.id)})
    response.set_cookie('booking_access_token',access_token,httponly=True)
    return access_token

@router.post('/logout')
async def logout_user(response:Response):
    response.delete_cookie('booking_access_token')

@router.get('/me')
async def read_user_me(current_user:Users =Depends(get_current_user)):
    return current_user


