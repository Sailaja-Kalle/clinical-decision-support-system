from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "clinical-decision-support-secret-key-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

USERS_DB = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@clinical.com",
        "hashed_password": pwd_context.hash("admin123"),
        "role": "admin",
        "disabled": False
    },
    "doctor": {
        "username": "doctor",
        "full_name": "Dr. Smith",
        "email": "doctor@clinical.com",
        "hashed_password": pwd_context.hash("doctor123"),
        "role": "doctor",
        "disabled": False
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    if username in USERS_DB:
        return USERS_DB[username]
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

def register_user(username: str, password: str, full_name: str, email: str, role: str = "doctor"):
    if username in USERS_DB:
        return False
    USERS_DB[username] = {
        "username": username,
        "full_name": full_name,
        "email": email,
        "hashed_password": get_password_hash(password),
        "role": role,
        "disabled": False
    }
    return True