from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "aDapTive@123secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
