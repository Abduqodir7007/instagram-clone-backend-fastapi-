from fastapi_mail import ConnectionConfig
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


mail_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM", os.getenv("MAIL_USERNAME")),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "b1fa524cf17d082ad867818eec8012325ce21108c9033ab9e4d3f058b76e65b9"
    )
