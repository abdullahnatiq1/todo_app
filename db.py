import os 
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from model import User, Todo

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file. Check your configuration")

engine = create_engine(DATABASE_URL, echo = True)

def createDBandTables():
    """
    Initializes the database scheme based on your SQLModel classes
    """
    SQLModel.metadata.create_all(engine)

def getSession():
    """
    Provides a database session to your routes and ensures it closes after use
    """
    with Session(engine) as session:
        yield session
