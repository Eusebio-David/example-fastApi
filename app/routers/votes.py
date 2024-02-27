from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from .. import models, shemas,database,oauth2
from typing import Optional, List

from sqlalchemy.orm import Session
from ..database import  get_db
import time


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: shemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(
    oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id_post == vote.post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {vote.post_id} doesn't exist")
    
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id ==
                                     current_user.id_user)
    found_vote=vote_query.first()
    
    if (vote.dir==1):
        if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id_user} has alredy voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id_user)
        db.add(new_vote)
        db.commit()
        return {"message": " successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}