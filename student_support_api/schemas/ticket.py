from pydantic import BaseModel
from enum import Enum 

class PriorityEnum(str,Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    
class StatusEnum(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    
class TicketBase(BaseModel):
    title: str
    description : str 
    priority: PriorityEnum

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: StatusEnum
    
class TicketResponse(TicketBase):
    id: int
    status: StatusEnum
    owner_id: int
        
        
