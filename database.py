from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv("PORT")}/{os.getenv("POSTGRES_DB")}"

engine = create_engine(DATABASE_URL)

session = sessionmaker(bind=engine)

Base = declarative_base()
