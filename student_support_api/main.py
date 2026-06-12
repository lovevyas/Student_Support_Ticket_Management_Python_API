from fastapi import FastAPI, Depends
from schemas.user import UserLogin
from schemas.ticket import TicketCreate
from schemas.response import APIResponse
from utils.auth import get_current_user
from utils.jwt_handler import create_access_token

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
    "/tickets",
    response_model = APIResponse
)
def create_ticket(ticket: TicketCreate, current_user = Depends(get_current_user)):    
    tickets_db.append(ticket.model_dump())
    ticket_data = {
        "id": len(tickets_db) + 1,
        "title": ticket.title,
        "description": ticket.description,
        "priority": ticket.priority,

        "status": "Open",

        "owner_id": current_user["id"],
        "owner_name": current_user["username"]
    }

    tickets_db.append(ticket_data)
    return APIResponse(
        success=True,
        message="Ticket created successfully",
        data=ticket_data
    )

@app.get("/tickets",
         response_model=APIResponse)
def get_tickets(current_user = Depends(get_current_user)):    
    
    if current_user["role"] == "support":
        return APIResponse(
            success=True,
            message="All tickets fetched",
            data=tickets_db
        )

    user_tickets = []

    for ticket in tickets_db:
        if ticket["owner_id"] == current_user["id"]:
            user_tickets.append(ticket)

    return APIResponse(
        success=True,
        message="User tickets fetched",
        data=user_tickets
    )
       


@app.post("/login", response_model = APIResponse) 
def userlogin(user: UserLogin):
    for user_detail in users_db:
        if(user_detail["username"] == user.username 
           and user_detail["password"] == user.password):            
            token = create_access_token({
                "id": user_detail["id"],
                "username": user_detail["username"],
                "role": user_detail["role"]
            })        
            return APIResponse(
                success=True,
                message="Login successful",
                data= {
                    "access_token": token,
                    "token_type": "bearer"
                }
                    
                )
    return APIResponse(
        success=False,
        message="Invalid credentials",
        data=None
    )
    

    
        

