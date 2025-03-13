from fastapi import status, Depends, HTTPException, APIRouter, Response
from ..models import modules
from ..scheme import schema
from ..auth import auth2
from .. import utils
from sqlalchemy.orm import Session
from ..db.database import get_db

router = APIRouter(
    prefix="/api/v1/votes/create",
    tags=["Votes"]
)

@router.post("/tool_vote")
def create_tool_vote(vote: schema.VoteTools, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_users)):

    tool_query = db.query(modules.Tools).filter(modules.Tools.id == vote.tool_id)

    tool = tool_query.first()

    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tool ID: {vote.tool_id} is Not Found")
    
    vote_query = db.query(modules.VoteTools).filter(modules.VoteTools.tool_id == vote.tool_id, modules.VoteTools.user_id == current_user.id )

    found_vote = vote_query.first()
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Tool ID: {vote.tool_id} Has Been Liked By You")
        
        new_tool_vote = modules.VoteTools(tool_id = vote.tool_id, user_id = current_user.id)
        
        db.add(new_tool_vote)
        db.commit()
        
        return {"message": "Tool Liked "}
    else:

        if not vote_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tool ID: {vote.tool_id} is Not Found")
        
        vote_query.delete(synchronize_session=False)
        
        db.commit()

        return {"message": "Tool unliked"}

@router.post("/tutor_vote")
def create_tutor_vote(vote: schema.VoteTutors, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_users)):

    tutor_query = db.query(modules.Tutors).filter(modules.Tutors.id == vote.tutor_id)

    tutor = tutor_query.first()

    if not tutor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tutor Id: {vote.tutor_id} Is Not Found")
    
    vote_query = db.query(modules.VoteTutors).filter(modules.VoteTutors.tutor_id == vote.tutor_id, modules.VoteTutors.user_id == current_user.id)

    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This Tutor Was Liked By You")
        
        new_vote = modules.VoteTutors(tutor_id = vote.tutor_id, user_id = current_user.id)
        
        db.add(new_vote)
        db.commit()

        return {"Messsage": "Tutor Liked"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tutor Not Found")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Message": "Post UnLiked"}


    

