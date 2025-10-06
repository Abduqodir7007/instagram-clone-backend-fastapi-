import random
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True)
    photo = Column(String, nullable=True)
    posts = relationship("Post", back_populates="author")
    comments = relationship("PostComment")

    def generate_code(self):
        code = "".join([str(random.randint(0, 100) % 10) for _ in range(5)])
        return code


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    caption = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship(User, back_populates="posts")
    
    likes = relationship("PostLike")


class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)

    comment = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship(User, back_populates="comments")
    post = relationship(Post)
    
    likes = relationship("CommentLike")


class PostLike(Base):
    __tablename__ = "post_likes"

    id = Column(Integer, primary_key=True, autoincrement=True)

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship(User)
    
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship(Post, back_populates="likes")
    


class CommentLike(Base):
    __tablename__ = "comment_likes"

    id = Column(Integer, primary_key=True, autoincrement=True)

    author_id = Column(Integer, ForeignKey("users.id"))
    comment_id = Column(Integer, ForeignKey("post_comments.id"))
    author = relationship(User)
    comment = relationship(PostComment, back_populates="likes")
