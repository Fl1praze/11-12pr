from app.dao.base import BaseDAO
from app.movie.models import Movie


class MovieDAO(BaseDAO):
    model = Movie