from sqlalchemy import Column, Integer, String
from myapp.db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    entries = relationship("FoodEntry", back_populates="user")
    meat_plans = relationship("MealPlan", back_populates="user")