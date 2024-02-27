from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import shemas, database, models
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config  import setting

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algotithm
#Expiration time
SECRET_KEY = setting.secret_key
ALGORITH = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy() #copia de los datos y los guardo en una variable
    
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
    return encoded_jwt

def verify_access_token(token: str, credentials_exeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITH])
        id: int  = payload.get("user_id")
        print(id)
        if id is None:
            raise credentials_exeption
        token_data = shemas.TokenData(id_user = id)
    except JWTError:
        raise credentials_exeption
    print(token_data)
    return token_data

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials", 
                                          headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    print(token)
    user = db.query(models.User).filter(models.User.id_user == token.id_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the user doesn't exist")
    
    return user