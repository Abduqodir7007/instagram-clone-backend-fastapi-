from fastapi import FastAPI
from config import Settings
from fastapi_jwt_auth import AuthJWT
from routes.user import auth_routes
from routes.post import post_routes

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_routes)
app.include_router(post_routes)
