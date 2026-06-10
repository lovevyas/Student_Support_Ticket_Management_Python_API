from pydantic import BaseModel

class APIResponse(BaseModel):
    success : bool
    data    : dict | list | None = None
    message : str