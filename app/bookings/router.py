from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.bookings.schemas import SBookingCreate, SBooking, SMovieInfo, SAvailableSeats, SUserBooking
from app.bookings.dao import BookingDAO
from app.halls.dao import HallDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from typing import List
from app.movie.dao import MovieDAO
from datetime import datetime
import pytz
from enum import Enum

router = APIRouter(prefix='/bookings', tags=['Бронирование 🎫'])


async def get_available_movie_titles() -> List[str]:
    movies = await MovieDAO.find_all()
    current_time = datetime.now(pytz.UTC)
    return [movie.title for movie in movies if movie.start_time > current_time]

@router.post("/", response_model=SBooking)
async def create_booking(booking: SBookingCreate, current_user: Users = Depends(get_current_user)):
    """
    Создать бронирование места на фильм.
    
    Порядок действий:
    1. Получите список фильмов через GET /bookings/movies
    2. Выберите ID фильма из списка
    3. Посмотрите свободные места через GET /bookings/movies/{id}/seats
    4. Отправьте запрос с выбранным ID фильма и номером места
    """
    # Проверяем существование фильма
    movie = await MovieDAO.find_by_id(booking.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    current_time = datetime.now(pytz.UTC)
    if movie.start_time <= current_time:
        raise HTTPException(status_code=400, detail="Бронирование на этот фильм закрыто")
        
    # Получаем информацию о зале
    hall = await HallDAO.find_by_id(movie.hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Зал не найден")
        
    # Проверяем корректность номера места
    if booking.seat_numbers > hall.total_seats:
        raise HTTPException(
            status_code=400, 
            detail=f"Неверный номер места. В зале {hall.total_seats} мест"
        )
        
    # Проверяем, не занято ли место
    booked_seats = await BookingDAO.get_booked_seats(booking.movie_id)
    if booking.seat_numbers in booked_seats:
        raise HTTPException(status_code=400, detail="Это место уже забронировано")
        
    try:
        # Создаем бронирование
        booking_data = {
            "user_id": current_user.id,
            "movie_id": booking.movie_id,
            "seat_numbers": booking.seat_numbers,
            "hall_id": movie.hall_id,
            "status": "confirmed",
            "booking_time": datetime.now()
        }
        
        # Создаем бронирование
        await BookingDAO.add(**booking_data)
        
        # Получаем созданное бронирование
        created_booking = await BookingDAO.find_one_or_none(
            user_id=current_user.id,
            movie_id=booking.movie_id,
            seat_numbers=booking.seat_numbers,
            hall_id=movie.hall_id,
            status="confirmed"
        )
        
        if not created_booking:
            raise HTTPException(status_code=500, detail="Ошибка при создании бронирования")
            
        return created_booking
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании бронирования: {str(e)}")

@router.get("/movies", response_model=List[SMovieInfo])
async def get_available_movies():
    """
    Получить список доступных для бронирования фильмов с информацией о свободных местах
    """
    movies = await MovieDAO.find_all()
    available_movies = []
    
    current_time = datetime.now(pytz.UTC)
    
    for movie in movies:
        # Проверяем, что время начала фильма еще не прошло
        if movie.start_time > current_time:
            hall = await HallDAO.find_by_id(movie.hall_id)
            if not hall:
                continue
                
            booked_seats = await BookingDAO.get_booked_seats(movie.id)
            available_seats = hall.total_seats - len(booked_seats)
            
            if available_seats > 0:
                available_movies.append({
                    'id': movie.id,
                    "title": movie.title,
                    "start_time": movie.start_time,
                    "duration": movie.duration,
                    "available_seats": available_seats
                })
    
    return available_movies

@router.get("/movies/{movie_id}/seats", response_model=SAvailableSeats)
async def get_movie_seats(
    movie_id: int = Path(..., description="ID фильма (можно получить из списка /bookings/movies)")
):
    movie = await MovieDAO.find_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    current_time = datetime.now(pytz.UTC)
    if movie.start_time <= current_time:
        raise HTTPException(status_code=400, detail="Бронирование на этот фильм закрыто")
        
    hall = await HallDAO.find_by_id(movie.hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Зал не найден")
        
    booked_seats = await BookingDAO.get_booked_seats(movie_id)
    available_seats = [i for i in range(1, hall.total_seats + 1) if i not in booked_seats]
    
    return {
        "id": movie.id,
        "title": movie.title,
        "start_time": movie.start_time,
        "duration": movie.duration,
        "available_seats": available_seats,
        "total_seats": hall.total_seats
    }

@router.get("/my", response_model=List[SUserBooking])
async def get_my_bookings(current_user: Users = Depends(get_current_user)):
    """
    Получить список всех бронирований текущего пользователя
    """
    bookings = await BookingDAO.find_by_user_id(current_user.id)
    result = []
    
    for booking in bookings:
        movie = await MovieDAO.find_by_id(booking.movie_id)
        if movie:
            result.append({
                "movie_title": movie.title,
                "start_time": movie.start_time,
                "seat_number": booking.seat_numbers
            })
    
    return result


