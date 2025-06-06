from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from myapp.db.database import Base

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True,nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    daily = Column(Integer, nullable=False)
    weekly = Column(Integer, nullable=False)

    user = relationship("User", back_populates="goals")