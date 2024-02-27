from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from datetime import datetime
from typing import List 


class User(Base): 
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True,nullable=False)
    email = Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    created_user = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    phone_number = Column(String)


class Post(Base):
    __tablename__ = 'posts'

    id_post = Column(Integer, primary_key=True,nullable=False)
    title_post = Column(String, nullable=False)
    content_post = Column(String, nullable=False)
    published = Column(Boolean, default = True)
    created_post = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")
   
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id_user"), onupdate="CASCADE", primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id_post"), onupdate="CASCADE", primary_key=True)