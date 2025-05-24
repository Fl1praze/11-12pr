from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    duration = Column(String(5))
    hall_id = Column(Integer, ForeignKey("halls.id"))
    start_time = Column(DateTime(timezone=True))
