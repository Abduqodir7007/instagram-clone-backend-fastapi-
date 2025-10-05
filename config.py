import os
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig

load_dotenv()

mail_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)


class Settings:
    authjwt_secret_key = (
        "b1fa524cf17d082ad867818eec8012325ce21108c9033ab9e4d3f058b76e65b9"
    )
