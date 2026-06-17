from fastapi import FastAPI, Request
from schemas.response import APIResponse
from utils.logger import logger
from routes import auth, tickets

app = FastAPI(title="Student Support Ticket API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} -> {response.status_code}")
    return response

app.include_router(auth.router)
app.include_router(tickets.router)

@app.get("/")
def home():
    return APIResponse(
        success = True,
        message = "Student Support Ticket API is running",
        data = None
    )