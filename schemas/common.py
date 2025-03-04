from pydantic import BaseModel 

class DelResponse(BaseModel):
    message: str
    status: bool