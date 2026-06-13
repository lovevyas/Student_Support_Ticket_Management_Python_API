from fastapi import Depends
from fastapi import HTTPException
from utils.security import oauth2_scheme
from utils.jwt_handler import verify_access_token

def get_current_user( token: str = Depends(oauth2_scheme) ):
    payload = verify_access_token(token)    
    if payload is None:
        raise HTTPException(
        status_code=401,
        detail="Invalid token"
    )
    return payload
