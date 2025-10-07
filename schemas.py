import random
from pydantic import BaseModel, EmailStr, validator


class UserModel(BaseModel):
    username: str
    email: EmailStr
    photo: str | None = None
    password: str

    @validator("password")
    def check_password(cls, value: str):
        if value.isdigit():
            raise ValueError("Password must contain at least one special character")
        return value


    class Config:
        from_attributes = True




class PostModel(BaseModel):

    author_id: int
    caption: str

    class Config:
        from_attributes = True


class PostCommentModel(BaseModel):

    author_id: int
    post_id: int
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