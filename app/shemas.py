from pydantic import BaseModel, EmailStr, conint, Field
from pydantic.types import conint
from datetime import datetime
from email_validator import ValidatedEmail, EmailNotValidError
from typing import Optional, ForwardRef



class PostBase(BaseModel):
    title_post: str
    content_post: str
    published: bool = True

class PostCreate(PostBase):
   pass

class UserOut(BaseModel):
    id_user: int
    email: EmailStr
    created_user: datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id_post: int
    created_post: datetime
    owner_id: int
    owner : UserOut

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    dir: int = conint(le=1)

class PostOut(BaseModel):
    Post: Post
    vote: int
    
   
    class Config:
        orm_mode = True

class likeOut(BaseModel):
    Post: Post
    vote: int
    
   
   
    class Config:
        orm_mode = True


class UserCreated(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id_user: Optional[int] = None

