from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Hall(Base):
    __tablename__ = 'halls'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    total_seats = Column(Integer)

    # Отношение к Booking
    bookings = relationship('Booking', back_populates='hall')
