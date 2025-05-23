from fastapi import  HTTPException,status

class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail='Пользователь уже существует'

class UserNotFoundException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail='Пользователя не с данной почтой не существует'

class PasswordNotCorrectException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail='Неверный пароль'

class TokeNotCorrectException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail='Нету токена'

class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail='Токен истёк'

class IncorrectFormatTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail='Неверный формат токена'

class RoomCannotBeBookedException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail='Не осталось свободных номеров'


