from fastapi import APIRouter
from config.db import conn
from models.user import users

user = APIRouter()

@user.get("/users")
def get_users():
    return conn.execute(users.select()).fetch_all()