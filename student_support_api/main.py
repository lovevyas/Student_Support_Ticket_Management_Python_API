from fastapi import FastAPI

app = FastAPI(title="Student Support Ticket API")

@app.get("/")
def home():
    return {
        "message": "Student Support Ticket API is running"
    }