from sqlalchemy import Integer, ForeignKey,Column
from app.database import Base

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'), nullable=False)