from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .db.database import engine
from .models import modules
from fastapi.middleware.cors import CORSMiddleware

modules.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origin_regex=None,
    expose_headers=None,
    max_age=1000,
)

class User(BaseModel):
    user_name: str
    user_email: str
    user_password: str

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="devtools", user="postgres", password="Jswebpro1", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('data base connection was successful')
        break
    except Exception as err:
        print(r'couldn\'t connect to data base')
        print('re trying')

# code for interacting with sql into or code without sqlalchemy

@app.get('/users')
def get_user():
    return {"users": [
        "natty",
        "john doe",
        "james smith",
        "mary williams"
    ]}

@app.post("/users")
def create_users(user: User):
    cursor.execute(""" INSERT INTO users (name, email, password) VALUES(%s, %s, %s) RETURNING * """, (user.user_name, user.user_email, user.user_password))
    created_user = cursor.fetchone()
    conn.commit()
    # if created_user == None:
    #     raise HTTPException(status_code=status.)
    return {"user": created_user}