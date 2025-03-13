from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..models import modules

from ..scheme import schema

from ..auth import auth2

from ..db import database
from .. import utils

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schema.Token)
def auth_users(user_credentials: schema.User_Login_Credentials, db: Session = Depends(database.get_db)):

    user = db.query(modules.Users).filter(modules.Users.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    if not utils.verify_users(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid user credentials")
    
    access_token = auth2.create_access_token(data ={"user_id": str(user.id)})
    
    return {"access_token": access_token, "token": "bearer", "user_details": user}
