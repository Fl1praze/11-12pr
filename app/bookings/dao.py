from app.dao.base import BaseDAO
from app.bookings.models import Booking


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def get_booked_seats(model, movie_id: int) -> list[int]:
        """Получить список забронированных мест для конкретного фильма"""
        bookings = await model.find_all(movie_id=movie_id)
        return [booking.seat_numbers for booking in bookings]

    @classmethod
    async def find_by_user_id(model, user_id: int):
        """Получить все бронирования пользователя"""
        return await model.find_all(user_id=user_id)
