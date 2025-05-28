from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from myapp.db.database import Base

class FoodEntry(Base):
    __tablename__ = 'food_entries'

    id = Column(Integer, primary_key=True ,nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship('User', back_populates='entries')