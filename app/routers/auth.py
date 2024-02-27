from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,shemas, models, utils, oauth2



router = APIRouter(tags=["Authentication"])


@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Ivalid Credentials")
    
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #created a token
    #return token
    access_token = oauth2.create_access_token(data={"user_id": user.id_user})
    return {'access_token': access_token,"token_type":"bearer"}