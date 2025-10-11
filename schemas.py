import random
from pydantic import BaseModel, EmailStr, field_validator
from models import User, CommentLike


class UserModel(BaseModel):
    username: str
    email: EmailStr
    photo: str | None = None
    password: str

    @field_validator("password")
    def check_password(cls, value: str):
        if value.isdigit():
            raise ValueError("Password must contain at least one special character")
        return value

    class Config:
        from_attributes = True


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserResponseModel(BaseModel):
    id: int
    username: str
    email: EmailStr
    photo: str | None = None

    class Config:
        from_attributes = True


class PostModel(BaseModel):
    author_id: int
    caption: str

    class Config:
        from_attributes = True


class PostResponseModel(BaseModel):
    id: int
    caption: str
    author: UserResponseModel
    likes_count: int | None = None


class PostCommentModel(BaseModel):

    author_id: int
    parent_id: int | None = None
    comment: str

    class Config:
        from_attributes = True


class PostLikeModel(BaseModel):

    author_id: int
    post_id: int

    class Config:
        from_attributes = True


class CommentLikeModel(BaseModel):

    author_id: int
    comment_id: int

    class Config:
        from_attributes = True


class CodeModel(BaseModel):
    code: int

    class Config:
        from_attributes = True
