import os, shutil
from fastapi import APIRouter, File, UploadFile, Depends
from models import User
from database import session

image_route = APIRouter(prefix="/upload")

UPLOAD_PATH = "user_images"
os.makedirs(UPLOAD_PATH, exist_ok=True)


@image_route.post("/{user_id}")
async def upload_image(
    user_id: int,
    file: UploadFile = File(...),
):
    if not file.content_type.endswith((".jpg", ".jpeg", ".png")):
        return {"Error": "You should upload an image"}

    file_path = os.path.join(UPLOAD_PATH, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    db_user = session.query(User).filter(User.id == user_id).first()
    db_user.image = file_path
    session.commit()
    session.refresh()

    return 