from fastapi import FastAPI

from app.users.router import router as users_router
from app.movie.router import router as movie_router
from app.halls.router import router as halls_router
from app.bookings.router import router as booking_router
app = FastAPI()

app.include_router(users_router)
app.include_router(movie_router)
app.include_router(halls_router)
app.include_router(booking_router)