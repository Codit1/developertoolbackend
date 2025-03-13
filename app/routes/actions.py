from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..scheme import schema

from ..auth import auth2
from ..db.database import get_db
from ..models import modules

router = APIRouter(
    prefix="/api/v1/user_actions",
    tags=["User Actions"]
)


@router.get('/get')
def get_user_actions( db: Session = Depends(get_db), userId: int = Depends(auth2.get_users)):

    actions_query = db.query(modules.UserAction).filter(modules.UserAction.user_id == userId.id )

    if not actions_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Action By User")

    actions = actions_query.first()

    return actions

@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_new_user_action(action: schema.createUserAction, db: Session = Depends(get_db), userId: int = Depends(auth2.get_users)):

    new_user_action = modules.UserAction(user_id = userId.id, **action.model_dump())

    db.add(new_user_action)
    db.commit()
    db.refresh(new_user_action)

    return new_user_action

@router.put('/full_update', status_code=status.HTTP_201_CREATED)
def update_user_actions(action: schema.UpdateUserActions, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_users)):

    user_actions = db.query(modules.UserAction).filter(modules.UserAction.user_id == current_user.id)

    if not user_actions.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Actions By User")
    
    update_actions = user_actions.update(user_id = current_user.id, **action.model_dump())

    db.commit()

    return update_actions

@router.patch("/partial_update", status_code=status.HTTP_201_CREATED)
def partial_update_actions(action: schema.UpdateUserActions, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_users)):

    action_query = db.query(modules.UserAction).filter(modules.UserAction.user_id == current_user.id)

    user_actions = action_query.first()

    if not user_actions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Action By User")
    
    if action.saved_tools == None:
        action.saved_tools = user_actions.saved_tools

    if action.saved_tutors == None:
        action.saved_tutors = user_actions.saved_tutors

    if action.liked_tools == None:
        action.liked_tools = user_actions.liked_tools

    if action.liked_tutors == None:
        action.liked_tutors = user_actions.liked_tutors
    
    if action.opened_tools == None:
        action.opened_tools = user_actions.opened_tools
    
    if action.opened_tutors == None:
        action.opened_tutors = user_actions.opened_tutors

    action_query.update(action.model_dump(), synchronize_session=False)

    db.commit()

    return user_actions

@router.delete("/delete")
def delete_user_action(db: Session = Depends(get_db), current_user: int = Depends(auth2.get_users)):

    delete_action = db.query(modules.UserAction).filter(modules.UserAction.user_id == current_user.id)

    if not delete_action.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Action By User")
    
    deleted_post_data = delete_action.first()

    if deleted_post_data.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could Not Authorize User")
    
    delete_action.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

