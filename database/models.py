from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

from database.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    exercise_history = relationship("ExerciseHistory", backref="user")
    food_history = relationship("FoodHistory", backref="user")


class ExerciseHistory(Base):
    __tablename__ = "exercise_history"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
                "id": self.id,
                "exercise_id": self.exercise_id,
                "user_id": self.user_id,
                "timestamp": self.timestamp
            }


class FoodHistory(Base):
    __tablename__ = "food_history"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
                "id": self.id,
                "food_id": self.food_id,
                "user_id": self.user_id,
                "timestamp": self.timestamp
            }