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
    # exercise_title = Column(String, index=True)
    # exercise_type = Column(String, index=True)
    # exercise_body_part = Column(String, index=True)
    # exercise_equipment = Column(String, index=True)
    # exercise_level = Column(String, index=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)



class FoodHistory(Base):
    __tablename__ = "food_history"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)