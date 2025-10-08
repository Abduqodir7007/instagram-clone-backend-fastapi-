from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import session
from schemas import PostModel
from fastapi_jwt_auth import AuthJWT


post_routes = APIRouter(prefix="/post")


@post_routes.get("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    new_post = PostModel(**post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return {"message": "Post created successfully", "post": new_post}


@post_routes.get("/", status_code=status.HTTP_200_OK)
async def get_posts(Authorize: AuthJWT = Depends(), limit: int = 100):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    posts = session.query(PostModel).all()
    response = jsonable_encoder(posts)
    return {"posts": response}
