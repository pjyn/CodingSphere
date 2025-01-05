from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
from bcrypt import hashpw, gensalt, checkpw

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return checkpw(password.encode(), hashed.encode())

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    payload = decode_access_token(token.credentials)
    return payload
