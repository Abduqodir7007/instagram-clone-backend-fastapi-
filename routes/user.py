from fastapi import APIRouter
from database import session
from schemas import UserModel
from models import User

auth_routes = APIRouter(prefix="/auth")


@auth_routes.post('/register')
async def register(user: UserModel):
    pass