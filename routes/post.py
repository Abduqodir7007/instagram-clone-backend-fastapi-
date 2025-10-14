from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import SessionLocal
from schemas import PostModel, PostCommentModel, PostResponseModel, PostLikeModel
from fastapi_jwt_auth import AuthJWT
from models import Post, PostComment, PostLike, User, CommentLike, bearer_scheme
from sqlalchemy import func
from sqlalchemy.orm import selectinload


session = SessionLocal()
post_routes = APIRouter(prefix="/post")


@post_routes.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(bearer_scheme)],
)
async def create_post(post: PostModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    new_post = Post(**post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    data = {
        "id": new_post.id,
        "caption": new_post.caption,
        "author": {
            "id": new_post.author.id,
            "username": new_post.author.username,
            "photo": new_post.author.photo,
        },
    }
    response = jsonable_encoder(data)
    return {"message": "Post created successfully", "response": response}


@post_routes.get("/", status_code=status.HTTP_200_OK)
async def get_posts(Authorize: AuthJWT = Depends(), limit: int = 100):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    post_likes = (
        session.query(Post, func.count(PostLike.id).label("likes_count"))
        .outerjoin(PostLike, PostLike.post_id == Post.id)
        .options(selectinload(Post.author))
        .group_by(Post.id)
        .all()
    )
    result = []
    for post, likes_count in post_likes:

        data = post.__dict__

        data["likes_count"] = likes_count

        result.append(PostResponseModel(**data))

    response = jsonable_encoder(result)
    return {"posts": response}


@post_routes.post("/{post_id}/comment", status_code=status.HTTP_200_OK)
async def create_comment(
    post_id: int, comment: PostCommentModel, Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    post = session.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = PostComment(**comment.model_dump(), post_id=post_id)

    session.add(new_comment)
    session.commit()

    return {"message": "Comment added successfully", "comment": new_comment}

@post_routes.get("/{post_id}/comments", status_code=status.HTTP_200_OK)
async def get_comments(post_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    post = session.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comments = session.query(PostComment).filter(PostComment.post_id == post_id).all()
    print(comments)
    return {"comments": comments}

@post_routes.post("/{post_id}/create-delete-like")
async def create_delete_like(post_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    email = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.email == email).first()

    post_like = session.query(PostLike).filter(PostLike.post_id == post_id).first()

    if post_like is None:
        new_post_like = PostLike(author_id=user.id, post_id=post_id)
        session.add(new_post_like)
        session.commit()
        return {"message": "Post liked successfully"}

    session.delete(post_like)
    session.commit()

    return {"message": "Post unliked successfully"}


@post_routes.post("comment/{comment_id}/create-delete-like")
async def create_delete_comment_like(comment_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    email = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.email == email).first()

    comment_like = (
        session.query(CommentLike).filter(CommentLike.comment_id == comment_id).first()
    )

    if comment_like is None:
        new_comment_like = CommentLike(author_id=user.id, comment_id=comment_id)
        session.add(new_comment_like)
        session.commit()
        return {"message": "Comment liked successfully"}

    session.delete(comment_like)
    session.commit()

    return {"message": "Comment unliked successfully"}
