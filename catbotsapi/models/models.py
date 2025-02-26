from pydantic import BaseModel, Field


class Cat(BaseModel):
    name: str = Field(min_length=1)
    color: str = Field(min_length=1)
    tail_length: int = Field(gt=0)
    whiskers_length: int = Field(gt=0)
