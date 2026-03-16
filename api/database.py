from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env file automatically

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=False,    
    future=True
)