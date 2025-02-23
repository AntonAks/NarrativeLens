from pydantic import BaseModel


class BaseDTO(BaseModel):
    class Config:
        frozen = True

