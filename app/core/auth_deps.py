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


def get_current_company(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        company_id = payload.get("company_id")

        if not company_id:
            raise HTTPException(403, "Company token required")

        return company_id

    except JWTError:
        raise HTTPException(401, "Invalid or expired token")

