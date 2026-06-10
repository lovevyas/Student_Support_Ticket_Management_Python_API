from fastapi import FastAPI
from schemas.ticket import TicketCreate
from schemas.response import APIResponse
from schemas.ticket import TicketBase
from schemas.user import UserLogin
app = FastAPI(title="Student Support Ticket API")
tickets_db = []
users_db = [
    {
        "id": 1,
        "username": "student",
        "password": "student123",
        "role": "student"
    },
    {
        "id": 2,
        "username": "support",
        "password": "support123",
        "role": "support"
    }
]

@app.get("/")
def home():
    return APIResponse(
        success = True,
        message = "Student Support Ticket API is running",
        data = None
    )
    
@app.post(
    "/ticket",
    response_model = APIResponse
)
def create_ticket(ticket: TicketCreate):
    tickets_db.append(ticket.model_dump())
    return APIResponse(
        success=True,
        message="Ticket created succesfully",
        data=ticket.model_dump()
    )

@app.get("/tickets",
         response_model=APIResponse)
def get_ticket():
    return APIResponse(
        success = True,
        message = "All tickets are here",
        data = tickets_db
    )
       


@app.post("/login", response_model = APIResponse) 
def userlogin(user: UserLogin):
    for user_detail in users_db:
        if(user_detail["username"] == user.username 
           and user_detail["password"] == user.password):
                return APIResponse(
                    success=True,
                    message="Login successful",
                    data= {
                        "id": user_detail["id"],
                        "username": user_detail["username"],
                        "role": user_detail["role"]
                        
                    }
                )
    return APIResponse(
        success=False,
        message="Invalid credentials",
        data=None
    )
    
        

