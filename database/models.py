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
    exercise_preferences = relationship("ExercisePreferences", back_populates="user", uselist=False)


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


class ExercisePreferences(Base):
    __tablename__ = "exercise_preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))  # Foreign Key to link to User
    type_cardio = Column(Integer)
    type_strength = Column(Integer)
    type_stretching = Column(Integer)
    bodypart_abdominals = Column(Integer)
    bodypart_biceps = Column(Integer)
    bodypart_chest = Column(Integer)
    bodypart_forearms = Column(Integer)
    bodypart_neck = Column(Integer)
    bodypart_shoulders = Column(Integer)
    bodypart_triceps = Column(Integer)
    level_beginner = Column(Integer)
    level_expert = Column(Integer)
    level_intermediate = Column(Integer)
    equipment_gym = Column(Integer)
    equipment_body_only = Column(Integer)
    bodypart_legs = Column(Integer)
    bodypart_back = Column(Integer)
    bodypart_fullbody = Column(Integer)

    # Establishing the relationship
    user = relationship("User", back_populates="exercise_preferences")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "preferences": {
                "type_cardio": self.type_cardio,
                "type_strength": self.type_strength,
                "type_stretching": self.type_stretching,
                "bodypart_abdominals": self.bodypart_abdominals,
                "bodypart_biceps": self.bodypart_biceps,
                "bodypart_chest": self.bodypart_chest,
                "bodypart_forearms": self.bodypart_forearms,
                "bodypart_neck": self.bodypart_neck,
                "bodypart_shoulders": self.bodypart_shoulders,
                "bodypart_triceps": self.bodypart_triceps,
                "level_beginner": self.level_beginner,
                "level_expert": self.level_expert,
                "level_intermediate": self.level_intermediate,
                "equipment_gym": self.equipment_gym,
                "equipment_body_only": self.equipment_body_only,
                "bodypart_legs": self.bodypart_legs,
                "bodypart_back": self.bodypart_back,
                "bodypart_fullbody": self.bodypart_fullbody
            }
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