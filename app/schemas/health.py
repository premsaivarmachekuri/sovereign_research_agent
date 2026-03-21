from pydantic import BaseModel


class Status(BaseModel):
    status: str
    project: str
