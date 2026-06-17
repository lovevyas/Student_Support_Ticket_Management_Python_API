from fastapi import APIRouter, HTTPException
from schemas.user import UserLogin
from schemas.response import APIResponse
from database import users_db
from utils.jwt_handler import create_access_token
from utils.logger import logger

router = APIRouter()

@router.post("/login", response_model = APIResponse)
def userlogin(user: UserLogin):
    for user_detail in users_db:
        if(user_detail["username"] == user.username
           and user_detail["password"] == user.password):
            token = create_access_token({
                "id": user_detail["id"],
                "username": user_detail["username"],
                "role": user_detail["role"]
            })
            logger.info(
                f"User {user_detail['username']} logged in successfully"
            )
            return APIResponse(
                success=True,
                message="Login successful",
                data= {
                    "access_token": token,
                    "token_type": "bearer"
                }
            )
    logger.warning(
    f"Failed login attempt for username: {user.username}"
    )
    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )