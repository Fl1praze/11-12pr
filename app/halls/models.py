from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from datetime import datetime

from app.database import Base

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)