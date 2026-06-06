from pydantic import BaseaModel

class APIResponse(BaseModel):
    success : bool
    data    : dict | list | None = None
    message : str