from pydantic import BaseModel, EmailStr, Field


class AuthorIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr | None = None
    bio: str = ""


class AuthorEvent(BaseModel):
    event_type: str = "author.created"
    name: str
    email: str | None
    bio: str = ""
