from pydantic import BaseModel

class RequestBody(BaseModel):
    query: str