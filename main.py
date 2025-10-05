from fastapi import FastAPI
from routes.post import post_routes
from routes.user import auth_routes
from config import Settings
from fastapi_jwt_auth import AuthJWT

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings


app.include_router(auth_routes)
app.include_router(post_routes)
