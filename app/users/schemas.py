from pydantic import BaseModel,EmailStr

#Схема регистрации пользователя
class SUserAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True