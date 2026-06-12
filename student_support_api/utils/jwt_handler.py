from jose import jwt, JWTError
SECRET_KEY  = "mysecretmyword"
ALGORITHM   = "HS256"

def create_access_token(data:dict):
    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms = [ALGORITHM]
            )
        return payload
    except JWTError:
        return None
    
