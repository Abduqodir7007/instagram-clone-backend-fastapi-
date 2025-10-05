from fastapi import APIRouter
from database import session

post_routes = APIRouter(
    prefix='/post'
)

