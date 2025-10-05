import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgres://{os.getenv("POSTGRES_USER")}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv("PORT")}/{os.getenv("POSTGRES_DB")}"
print(DATABASE_URL)