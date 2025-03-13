from fastapi import FastAPI, Depends

from .auth import auth2
from .db.database import engine
from .models import modules
from fastapi.middleware.cors import CORSMiddleware
from .routes import tools, users, auth, actions, votes


modules.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def default_route(user: int = Depends(auth2.get_users)):
    users = user
    print(users)
    return {"message": "hello welcome"}

app.include_router(tools.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(actions.router)
app.include_router(votes.router)