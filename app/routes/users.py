from fastapi import status, Depends, HTTPException, APIRouter, Response
from ..models import modules
from ..scheme import schema
from ..auth import auth2
from .. import utils
from sqlalchemy.orm import Session
from ..db.database import get_db

router = APIRouter(
    prefix="/api/v1/users",
    tags=["USERS"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=schema.userResponse)
def get_users( db: Session = Depends(get_db), users: int = Depends(auth2.get_users)):

    user = db.query(modules.Users).filter(modules.Users.id == users.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="can\'t find user with that id")

    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_users(user: schema.CreateUser,db: Session = Depends(get_db)):
    
    user.password = utils.hash(user.password)

    new_user = modules.Users(**user.model_dump())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="email already exist")
    
    return new_user
