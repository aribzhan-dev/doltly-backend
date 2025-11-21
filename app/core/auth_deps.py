from app.core.auth_utils import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

security = HTTPBearer()

def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")