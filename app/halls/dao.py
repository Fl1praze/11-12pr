from app.dao.base import BaseDAO
from app.halls.models import Hall


class HallDAO(BaseDAO):
    model = Hall