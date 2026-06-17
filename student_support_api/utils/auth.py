from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from utils.security import bearer_scheme
from utils.jwt_handler import verify_access_token

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    payload = verify_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload
