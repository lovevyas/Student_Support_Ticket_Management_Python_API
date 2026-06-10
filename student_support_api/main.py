from fastapi import FastAPI
from schemas.ticket import TicketCreate
from schemas.response import APIResponse
from schemas.ticket import TicketBase

app = FastAPI(title="Student Support Ticket API")
tickets_db = []

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
        

