from fastapi import APIRouter, HTTPException, status, Depends
from database import session, engine
from schemas import UserModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from config import mail_config
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import BackgroundTasks

session = session(bind=engine)

auth_routes = APIRouter(prefix="/auth")


async def send_email(to: str, code: int):
    message = MessageSchema(
        subject="Email Verification",
        recipients=[to],
        body=f"Your verification code is {code}",
        subtype=MessageType.plain,
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)


@auth_routes.post("/register")
async def register(user: UserModel, background_tasks: BackgroundTasks):

    db_user = (
        session.query(User)
        .filter(
            or_(User.email == user.email, User.username == user.username),
        )
        .first()
    )
    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    new_user = User(**user.dict())
    new_user.password = generate_password_hash(user.password)
    code = new_user.generate_code()
    background_tasks.add_task(send_email, user.email, int(code))
    session.add(new_user)
    session.commit()
    return {"message": "User registered successfully"}


@auth_routes.post("/list")
def list_users(Authorize: AuthJWT = Depends()):

    users = session.query(User).all()
    return users


@auth_routes.delete("/delete/{user_id}")
def delete_user(user_id: int, Authorize: AuthJWT = Depends()):

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}
