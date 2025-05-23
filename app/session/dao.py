from app.dao.base import BaseDAO
from app.session.models import Session


class SessionDAO(BaseDAO):
    model = Session