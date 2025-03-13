from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..scheme import schema

from ..auth import auth2
from ..db.database import get_db
from ..models import modules

router = APIRouter(
    prefix="/api/v1/tools",
    tags=["TOOLS"]
)

# to get all tools
@router.get("/gets", response_model=List[schema.ToolDetailsResponse])
def get_all_tool(db: Session = Depends(get_db)):
    
    tools = db.query(modules.Tools).all()

    return tools

# to filter and get a particular tool base on the id
@router.get("/get/{id}")
def filter_tools(id: int, db: Session = Depends(get_db), user: int = Depends(auth2.get_users)):

    tool = db.query(modules.Tools).filter(modules.Tools.id == id).first()

    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the tool id: {id} can't be found ")

    return tool

@router.post("/create_tools")
def create_tools(tools: schema.CreateTools, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_users)):

    new_tool = modules.Tools(**tools.model_dump())

    try:
        db.add(new_tool)
        db.commit()
        db.refresh(new_tool)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tool Witth That Name Already Exist")
    
    return new_tool

@router.put("/update_tools/{id}")
def update_tools(id: int, tools: schema.UpdateTools, db: Session = Depends(get_db), current_users: int = Depends(auth2.get_users)):

    tool_query = db.query(modules.Tools).filter(modules.Tools.id == id)


    if not tool_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tool With ID: {id} Was Not Found")
    
    tool_data = tool_query.update(**tools.model_dump())

    db.commit()

    return tool_data

@router.patch("/partial_update/{id}")
def partial_update_tools(id: int, tools: schema.UpdateTools, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_users)):

    tool_query = db.query(modules.Tools).filter(modules.Tools.id == id)

    if not tool_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Tool With ID: {id} Was Found")
    
    tool_data = tool_query.update(**tools.model_dump())

    db.commit()

    return tool_data

@router.delete("/delete/{id}")
def delete_tools(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_users)):

    tool_query = db.query(modules.Tools).filter(modules.Tools.id == id)

    if not tool_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Tool With ID: {id} Was Found")
    
    tool_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

