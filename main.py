from fastapi import FastAPI
from routes.post import post_routes
from routes.user import auth_routes


app = FastAPI()

app.include_router(auth_routes)
app.include_router(post_routes)
