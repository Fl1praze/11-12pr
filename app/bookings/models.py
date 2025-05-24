from sqlalchemy import Integer, ForeignKey, Column, DateTime, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    seat_numbers = Column(Integer, nullable=False)
    booking_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20))
    hall_id = Column(Integer, ForeignKey('halls.id'))

    # Отношения
    hall = relationship('Hall', back_populates='bookings')