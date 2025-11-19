from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from app.core.auth_utils import REFRESH_SECRET_KEY, ALGORITHM, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

    new_access = create_access_token({"user_id": user_id})

    return {"access_token": new_access, "token_type": "bearer"}