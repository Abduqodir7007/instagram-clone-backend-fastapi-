from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from database import SessionLocal, engine
from schemas import UserModel, CodeModel, UserResponseModel, UserLoginModel
from models import User, VerifyEmail
from werkzeug.security import generate_password_hash, check_password_hash
from config import mail_config
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import BackgroundTasks

session = SessionLocal()

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
async def register(
    user: UserModel, background_tasks: BackgroundTasks, Authorize: AuthJWT = Depends()
):
    access_lifetime = timedelta(days=3)
    refresh_lifetime = timedelta(days=5)
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

    new_user = User(**user.model_dump())
    new_user.password = generate_password_hash(user.password)
    code = new_user.generate_code()
    access_token = Authorize.create_access_token(
        user.email, expires_time=access_lifetime
    )
    refresh_token = Authorize.create_refresh_token(
        user.email, expires_time=refresh_lifetime
    )
    data = {"access_token": access_token, "refresh_token": refresh_token}
    background_tasks.add_task(send_email, user.email, int(code))
    session.add(new_user)
    session.commit()
    return {"message": "User registered successfully", "tokens": data}


@auth_routes.post("/list")
def list_users(Authorize: AuthJWT = Depends(), response_model=UserResponseModel):

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


def check_code(code: int, user: User):
    verify_code = user.codes.filter(
        or_(
            VerifyEmail.code == code,
            VerifyEmail.is_confirmed == False,
            VerifyEmail.expiration_time > datetime.now(),
        )
    ).first()
    if verify_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Code is expired"
        )
    return True


@auth_routes.post("/verify")
async def verify_email(code: CodeModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authrized"
        )
    email = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.email == email).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    check_code(code.code, db_user)
    access_token = db_user.create_access_token(db_user.email)
    refresh_token = db_user.create_refresh_token(db_user.email)
    data = {"access_token": access_token, "refresh_token": refresh_token}

    return {"message": "Email verified successfully", "tokens": data}


@auth_routes.post("/login")
async def login(user: UserLoginModel, Authorize: AuthJWT = Depends()):
    access_lifetime = timedelta(days=3)
    refresh_lifetime = timedelta(days=5)

    db_user = session.query(User).filter(User.email == user.email).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(
            db_user.email, expires_time=access_lifetime
        )
        refresh_token = Authorize.create_refresh_token(
            db_user.email, expires_time=refresh_lifetime
        )
        response = {"access": access_token, "refresh": refresh_token}

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
