from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
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
    food_preferences = relationship("FoodPreferences", back_populates="user", uselist=False)


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
                "Type_Cardio": self.type_cardio,
                "Type_Strength": self.type_strength,
                "Type_Stretching": self.type_stretching,
                "BodyPart_Abdominals": self.bodypart_abdominals,
                "BodyPart_Biceps": self.bodypart_biceps,
                "BodyPart_Chest": self.bodypart_chest,
                "BodyPart_Forearms": self.bodypart_forearms,
                "BodyPart_Neck": self.bodypart_neck,
                "BodyPart_Shoulders": self.bodypart_shoulders,
                "BodyPart_Triceps": self.bodypart_triceps,
                "Level_Beginner": self.level_beginner,
                "Level_Expert": self.level_expert,
                "Level_Intermediate": self.level_intermediate,
                "Equipment_Gym": self.equipment_gym,
                "Equipment_Body_Only": self.equipment_body_only,
                "BodyPart_Legs": self.bodypart_legs,
                "BodyPart_Back": self.bodypart_back,
                "BodyPart_FullBody": self.bodypart_fullbody
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


class FoodPreferences(Base):
    __tablename__ = 'food_preferences'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))  # Foreign Key to link to User
    calories = Column(Float)
    fat_content = Column(Float)
    saturated_fat_content = Column(Float)
    cholesterol_content = Column(Float)
    sodium_content = Column(Float)
    carbohydrate_content = Column(Float)
    fiber_content = Column(Float)
    sugar_content = Column(Float)
    protein_content = Column(Float)
    allergies = Column(String)
    max_time = Column(Float)

    user = relationship("User", back_populates="food_preferences")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "preferences": {
                'Calories': self.calories,
                'FatContent': self.fat_content,
                'SaturatedFatContent': self.saturated_fat_content,
                'CholesterolContent': self.cholesterol_content,
                'SodiumContent': self.sodium_content,
                'CarbohydrateContent': self.carbohydrate_content,
                'FiberContent': self.fiber_content,
                'SugarContent': self.sugar_content,
                'ProteinContent': self.protein_content
            },
            "filters": {
                "Allergies": self.allergies,
                "MaxTime": self.max_time,
            }
        }