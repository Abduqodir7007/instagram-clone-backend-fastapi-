from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import session, engine
from schemas import PostModel, PostCommentModel
from fastapi_jwt_auth import AuthJWT
from models import Post, PostComment, bearer_scheme


session = session(bind=engine)
post_routes = APIRouter(prefix="/post")


@post_routes.post("/create", status_code=status.HTTP_201_CREATED, dependencies=[Depends(bearer_scheme)])
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

    posts = session.query(Post).all()
    response = jsonable_encoder(posts)
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
