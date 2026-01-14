from fastapi import HTTPException, Header
from firebase_admin import auth

async def verify_firebase_token(authorization: str = Header(None)):
    """FastAPI dependency to verify Firebase ID token present in Authorization header.
    Expects: Authorization: Bearer <token>
    """
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
