from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.auth_utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(401, "Invalid or expired token")

    return payload["user_id"]