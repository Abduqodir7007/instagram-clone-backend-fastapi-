from fastapi import APIRouter, HTTPException, status, Depends
from database import session, engine
from schemas import UserModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from config import mail_config
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_

session = session(bind=engine)
auth_routes = APIRouter(prefix="/auth")


async def send_email(to: str, code: int):
    pass


@auth_routes.post("/register")
async def register(user: UserModel, Authorize: AuthJWT = Depends()):

    db_user = (
        session.query(User)
        .filter(
            or_(
                User.email == user.email,
                User.email == user.email,
                User.phone_number == user.phone_number,
            ),
        )
        .first()
    )
    if db_user: 
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    
    new_user = User(**user.dict())
    new_user.password = generate_password_hash(user.password)
    code=user.generate_code()
    await send_email(user.email, code)
    session.add(user)
    session.commit()
    return {"message": "User registered successfully"}
