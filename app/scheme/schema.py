from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional
from datetime import datetime

class ToolDetailsResponse(BaseModel):
    id: int
    name: str
    category: str
    popular: bool
    newly_added: bool
    total_likes: int
    is_free: bool
    link: str


class UserAction(BaseModel):
    savedTools: list
    savedTutors: list
    likedTools: list
    likedTutors: list

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class User_Login_Credentials(BaseModel):
    email: EmailStr
    password: str

class Votes(BaseModel):
    tool_id: int
    dir: conint(le=1) #type: ignore

class TokenData(BaseModel):
    id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token: str

class userResponse(BaseModel):
    name: str
    id: int

class createUserAction(BaseModel):
    saved_tools: list
    saved_tutors: list
    liked_tools: list
    liked_tutors: list
    opened_tools: list
    opened_tutors: list

class UpdateUserActions(BaseModel):
    saved_tools: Optional[list] = None
    saved_tutors: Optional[list] = None
    liked_tools: Optional[list] = None
    liked_tutors: Optional[list] = None
    opened_tools: Optional[list] = None
    opened_tutors: Optional[list] = None

class CreateTools(BaseModel):
    name: str
    category: str
    popular: bool = False
    newly_added: bool = True
    total_likes: int = 0
    is_free: bool = True
    link: str

class UpdateTools(BaseModel):
    name: str | None
    category: str | None
    popular: bool | None
    newly_added: bool | None
    total_likes: int | None
    is_free: bool | None
    link: str | None

class VoteTools(BaseModel):
    tool_id: int
    dir: conint(le=1) # type: ignore

class VoteTutors(BaseModel):
    tutor_id: int
    dir: conint(le=1) #type: ignore