from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from myapp.db.database import Base

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week = Column(Integer, nullable=False)
    plan = Column(String, nullable=False)

    user = relationship("User", back_populates="meal_plans")
