from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=100)
    priority: int = Field(ge=1, le=10)
    completed: bool