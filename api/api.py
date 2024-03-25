import api.utils as utils

from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Security
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.db import SessionLocal, engine, Base
from database.models import User, ExerciseHistory, FoodHistory

app = FastAPI()
Base.metadata.create_all(bind=engine)


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


@app.post("/log/exercise")
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


@app.post("/log/food")
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


@app.get("/history/exercise")
async def get_exercise_history(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    history = db.query(ExerciseHistory).filter(ExerciseHistory.user_id == user_id).all()
    return history


@app.get("/history/food")
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