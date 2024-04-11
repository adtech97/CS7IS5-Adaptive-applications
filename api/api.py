import api.utils as utils

from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Security
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.db import SessionLocal
from database.models import User, ExerciseHistory, FoodHistory, ExercisePreferences

app = FastAPI()


async def get_current_user_id(token: str = Security(utils.oauth2_scheme)):
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


class UserSignup(BaseModel):
    name: str
    email: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup")
def signup(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_signup = UserSignup(name=name, email=email, password=password)
    hashed_password = utils.pwd_context.hash(user_signup.password)
    db_user = User(email=user_signup.email, name=user_signup.name, password=hashed_password)
    db.add(db_user)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User created successfully."}


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not utils.pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(
        user_id=user.id, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


def _create_access_token(user_id: int, expires_delta: timedelta = None):
    to_encode = {"sub": str(user_id)}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, utils.SECRET_KEY, algorithm=utils.ALGORITHM)
    return encoded_jwt


@app.post("/exercise/log")
async def log_exercise(
    exercise_id: int = Form(...),
    user_id: int = Depends(get_current_user_id),
    timestamp: datetime = None,
    db: Session = Depends(get_db)):

    if timestamp is None:
        timestamp = datetime.utcnow()
    new_entry = ExerciseHistory(exercise_id=exercise_id, user_id=user_id, timestamp=timestamp)
    db.add(new_entry)
    db.commit()
    return {"message": "Exercise logged successfully."}


@app.get("/exercise/history")
async def get_exercise_history(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    history = db.query(ExerciseHistory).filter(ExerciseHistory.user_id == user_id).all()

    ret_data = []
    for history_item in history:
        history_item_dict =  history_item.to_dict()
        history_item_dict["details"] = app.state.workout_recommender.workout_details(history_item_dict["exercise_id"])
        ret_data.append(history_item_dict)

    return ret_data


@app.get("/exercise/details/{exercise_id}")
async def get_exercise_history(exercise_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return  app.state.workout_recommender.workout_details(exercise_id)


@app.post("/exercise/search")
async def search_exercise(
        Type_Cardio: int = Form(...),
        Type_Strength: int = Form(...),
        Type_Stretching: int = Form(...),
        BodyPart_Abdominals: int = Form(...),
        BodyPart_Biceps: int = Form(...),
        BodyPart_Chest: int = Form(...),
        BodyPart_Forearms: int = Form(...),
        BodyPart_Neck: int = Form(...),
        BodyPart_Shoulders: int = Form(...),
        BodyPart_Triceps: int = Form(...),
        Level_Beginner: int = Form(...),
        Level_Expert: int = Form(...),
        Level_Intermediate: int = Form(...),
        Equipment_Gym: int = Form(...),
        Equipment_Body_Only: int = Form(...),
        BodyPart_Legs: int = Form(...),
        BodyPart_Back: int = Form(...),
        BodyPart_FullBody: int = Form(...),
):

    return app.state.workout_recommender.get_recommendations({
        "type_cardio": Type_Cardio,
        "type_strength": Type_Strength,
        "type_stretching": Type_Stretching,
        "bodypart_abdominals": BodyPart_Abdominals,
        "bodypart_biceps": BodyPart_Biceps,
        "bodypart_chest": BodyPart_Chest,
        "bodypart_forearms": BodyPart_Forearms,
        "bodypart_neck": BodyPart_Neck,
        "bodypart_shoulders": BodyPart_Shoulders,
        "bodypart_triceps": BodyPart_Triceps,
        "level_beginner": Level_Beginner,
        "level_expert": Level_Expert,
        "level_intermediate": Level_Intermediate,
        "equipment_gym": Equipment_Gym,
        "equipment_body_only": Equipment_Body_Only,
        "bodypart_legs": BodyPart_Legs,
        "bodypart_back": BodyPart_Back,
        "bodypart_fullbody": BodyPart_FullBody
    }, 10)


@app.post("/exercise/preferences")
async def set_exercise_preferences(
        Type_Cardio: int = Form(...),
        Type_Strength: int = Form(...),
        Type_Stretching: int = Form(...),
        BodyPart_Abdominals: int = Form(...),
        BodyPart_Biceps: int = Form(...),
        BodyPart_Chest: int = Form(...),
        BodyPart_Forearms: int = Form(...),
        BodyPart_Neck: int = Form(...),
        BodyPart_Shoulders: int = Form(...),
        BodyPart_Triceps: int = Form(...),
        Level_Beginner: int = Form(...),
        Level_Expert: int = Form(...),
        Level_Intermediate: int = Form(...),
        Equipment_Gym: int = Form(...),
        Equipment_Body_Only: int = Form(...),
        BodyPart_Legs: int = Form(...),
        BodyPart_Back: int = Form(...),
        BodyPart_FullBody: int = Form(...),
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    # Attempt to find an existing preference record for the user
    preferences = db.query(ExercisePreferences).filter(ExercisePreferences.user_id == user_id).first()

    if preferences:
        preferences.type_cardio = Type_Cardio
        preferences.type_strength = Type_Strength
        preferences.type_stretching = Type_Stretching
        preferences.bodypart_abdominals = BodyPart_Abdominals
        preferences.bodypart_biceps = BodyPart_Biceps
        preferences.bodypart_chest = BodyPart_Chest
        preferences.bodypart_forearms = BodyPart_Forearms
        preferences.bodypart_neck = BodyPart_Neck
        preferences.bodypart_shoulders = BodyPart_Shoulders
        preferences.bodypart_triceps = BodyPart_Triceps
        preferences.level_beginner = Level_Beginner
        preferences.level_expert = Level_Expert
        preferences.level_intermediate = Level_Intermediate
        preferences.equipment_gym = Equipment_Gym
        preferences.equipment_body_only = Equipment_Body_Only
        preferences.bodypart_legs = BodyPart_Legs
        preferences.bodypart_back = BodyPart_Back
        preferences.bodypart_fullbody = BodyPart_FullBody
    else:
        preferences = ExercisePreferences(
            user_id=user_id,
            type_cardio=Type_Cardio,
            type_strength=Type_Strength,
            type_stretching=Type_Stretching,
            bodypart_abdominals = BodyPart_Abdominals,
            bodypart_biceps = BodyPart_Biceps,
            bodypart_chest = BodyPart_Chest,
            bodypart_forearms = BodyPart_Forearms,
            bodypart_neck = BodyPart_Neck,
            bodypart_shoulders = BodyPart_Shoulders,
            bodypart_triceps = BodyPart_Triceps,
            level_beginner = Level_Beginner,
            level_expert = Level_Expert,
            level_intermediate = Level_Intermediate,
            equipment_gym = Equipment_Gym,
            equipment_body_only = Equipment_Body_Only,
            bodypart_legs = BodyPart_Legs,
            bodypart_back = BodyPart_Back,
            bodypart_fullbody=BodyPart_FullBody
        )
        db.add(preferences)

    db.commit()
    return {"message": "Exercise preferences updated successfully."}


@app.get("/exercise/preferences")
async def get_exercise_preferences(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    preferences = db.query(ExercisePreferences).filter(ExercisePreferences.user_id == user_id).first()

    if preferences:
        return preferences.to_dict()
    else:
        raise HTTPException(status_code=404, detail="No exercise preferences set")

@app.get("/exercise/recommendations/history")
async def get_exercise_recommendations_history(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    history = db.query(ExerciseHistory).filter(ExerciseHistory.user_id == user_id).all()

    exercise_ids = []
    for history_item in history[-5:]:
        history_item_dict = history_item.to_dict()
        exercise_ids.append(history_item_dict["exercise_id"])

    return app.state.workout_recommender.get_recommendations_for_selected_indices(exercise_ids, 5)


@app.get("/exercise/recommendations/preferences")
async def get_exercise_recommendations_preferences(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    preferences = db.query(ExercisePreferences).filter(ExercisePreferences.user_id == user_id).first()

    if preferences:
        return app.state.workout_recommender.get_recommendations(preferences.to_dict()["preferences"], 10)
    else:
        raise HTTPException(status_code=404, detail="No exercise preferences set")


@app.post("/food/log")
async def log_food(
    food_id: int = Form(...),
    user_id: int = Depends(get_current_user_id),
    timestamp: datetime = None,  # Timestamp will be dealt with inside the function
    db: Session = Depends(get_db)):

    if timestamp is None:
        timestamp = datetime.utcnow()
    new_entry = FoodHistory(food_id=food_id, user_id=user_id, timestamp=timestamp)
    db.add(new_entry)
    db.commit()
    return {"message": "Food logged successfully."}


@app.get("/food/history")
async def get_food_history(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    history = db.query(FoodHistory).filter(FoodHistory.user_id == user_id).all()
    return history


def _get_current_user_id(token: str = Depends(utils.oauth2_scheme)):
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")