from fastapi import FastAPI, Depends, HTTPException
from schemas.user import UserLogin
from schemas.ticket import TicketCreate, TicketUpdate
from schemas.response import APIResponse
from utils.auth import get_current_user
from utils.jwt_handler import create_access_token
from utils.logger import logger
from fastapi import Request

app = FastAPI(title="Student Support Ticket API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} -> {response.status_code}")
    return response

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

def get_ticket_by_id(ticket_id:int):
    ticket_found = None
    for ticket in tickets_db:
        if ticket["id"] == ticket_id:
            ticket_found = ticket
            return ticket_found            
                        
    if ticket_found is None:        
        logger.warning(
            f"Ticket Not found "
            f"Ticket Id: {ticket_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
            )
                

@app.get("/")
def home():
    return APIResponse(
        success = True,
        message = "Student Support Ticket API is running",
        data = None
    )
    
@app.post( "/tickets", response_model = APIResponse)
def create_ticket(ticket: TicketCreate, current_user = Depends(get_current_user)):    
    
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
    logger.info(
        f"Ticket {ticket_data['id']} created by {current_user['username']}"
    )
    return APIResponse(
        success=True,
        message="Ticket created successfully",
        data=ticket_data
    )

@app.get("/tickets", response_model=APIResponse)
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
    
@app.put("/tickets/{ticket_id}", response_model=APIResponse)
def update_ticket_status(
    ticket_id: int,
    ticket_update: TicketUpdate,
    current_user=Depends(get_current_user) ):
    
    if current_user["role"] != "support":
     logger.warning(
        f"Unauthorized ticket update attempt "
        f"by {current_user['username']}"
    )
     raise HTTPException(
        status_code=403,
        detail="Only support staff can update tickets"
        )   
    
    ticket_found = get_ticket_by_id(ticket_id)    
        
    old_status = ticket_found["status"]
    ticket_found["status"] = ticket_update.status
    logger.info(
        f"Ticket {ticket_id} updated from "
        f"{old_status} to {ticket_update.status} "
        f"by {current_user['username']}"
    )
    
    return APIResponse(
        success=True,
        message="Ticket status updated successfully",
        data=ticket_found
        )
    
@app.get("/tickets/{ticket_id}",
         response_model=APIResponse)
def fetch_ticket(ticket_id: int,    
        current_user=Depends(get_current_user)):
    
    ticket_found = get_ticket_by_id(ticket_id)    
        
    if current_user["role"] == "student":        
        if ticket_found["owner_id"] != current_user["id"]:
            raise HTTPException(
            status_code=403,
            detail="Unauthorized from viewing the ticket"
            )                                                             
    return APIResponse(
        success=True,
        message="Ticket fetched successfully",
        data=ticket_found
        )
    
    
        

