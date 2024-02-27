
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from typing import Optional, List
from .. import models, shemas, utils
from sqlalchemy.orm import Session
from ..database import  get_db
import time
from .. import oauth2
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[shemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int =
                       Depends(oauth2.get_current_user), limit: int = 10,skip: int = 0,
                       search: Optional[str]=" "):
    """En los comados debajo usamos sql normal para hacer consultass"""
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    """
    En los comandos de abajo usamos sqlalchemy, donde no necesitamos sql normal
    """
    posts = db.query(models.Post).filter(models.Post.title_post.contains(search)).limit(limit).offset(skip).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="posts doesn't exist")
    
    
    return posts
    #results = db.query(models.Post,
      #                  func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id_post, isouter=True).group_by(models.Post.id_post).all()
    #results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id_post, isouter=True).group_by(models.Post.id_post).all()
    
    
    
    
    

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=shemas.Post)
async def create_posts(post: shemas.PostCreate,db: Session = Depends(get_db), current_user: int =
                       Depends(oauth2.get_current_user)):
    
    #cursor.execute(""" INSERT INTO posts(title, content_post, published) VALUES (%s,%s,%s) RETURNING
    #                * """,
    #               (post.title, post.content, post.published))
    
    #new_post = cursor.fetchone()
    #conn.commit()
    #print(current_user.email)
    new_post = models.Post(owner_id= current_user.id_user, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post





@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=shemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),current_user: int =
                       Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id_post = %s""",(str(id)))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id_post == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id_post, isouter=True).group_by(
        models.Post.id_post).filter(models.Post.id_post == id).first()

    
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} doesn't exist")
    if hasattr(post, 'owner_id') and post.owner_id != current_user.id_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action") 


    json = {
        "Post": post[0],
        "vote": post[1]
    }
        
    return json


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db: Session = Depends(get_db),current_user: int =
                       Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id_post = %s RETURNING * """,(str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id_post == id)
    post = post_query.first()
    if  post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} doesn't exist, could not be eliminated ")
    
    if post.owner_id != current_user.id_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}",response_model=shemas.Post)
def update_post(id: int, update_post: shemas.PostCreate, db: Session = Depends(get_db),current_user: int =
                       Depends(oauth2.get_current_user)):
    #cursor.execute(""" UPDATE posts SET title = %s, content_post = %s, published = %s WHERE id_post = %s RETURNING *""",
    #              (post.title, post.content,post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
                   
    post_query = db.query(models.Post).filter(models.Post.id_post == id)
    post = post_query.first()
    if  post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} doesn't exist.")
    
    if post.owner_id != current_user.id_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    
    post_query.update(update_post.dict(),synchronize_session=False)
    db.commit()
    
    return  post_query.first()