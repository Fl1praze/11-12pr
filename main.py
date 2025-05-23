from fastapi import FastAPI

from app.users.router import router as users_router
from app.movie.router import router as movie_router
from app.session.router import router as session_router
app = FastAPI()

app.include_router(users_router)
app.include_router(movie_router)
app.include_router(session_router)