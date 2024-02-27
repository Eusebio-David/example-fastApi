from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from typing import Optional, List
from .. import models, shemas
from sqlalchemy.orm import Session
from ..database import  get_db
import time
from .. import oauth2
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder
import json


router=APIRouter(
    prefix="/likes",
    tags=["Likes"]

)

@router.get("/",response_model=List[shemas.likeOut])
async def likes(db: Session = Depends(get_db), current_user: int =
                       Depends(oauth2.get_current_user), limit: int = 10,skip: int = 0,
                       search: Optional[str]=" "):
    
    #inner = db.query(models.Post, models.User).join(models.User, models.Post.owner_id==models.User.id_user)
    #results_inner = inner.all()
    
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id_post, isouter=True).group_by(models.Post.id_post).filter(
        models.Post.title_post.contains(search)).limit(limit).offset(skip).all()
    #results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id_post, isouter=True).group_by(models.Post.id_post).all()
    
    print(results)
    lista_like = []
# Imprimir el resultado en formato JSON
    for post, vote in results:
        post_out=post.__dict__
        likeout = {
            "Post": post,
            "vote": vote
        }
        lista_like.append(likeout)
    
    return lista_like