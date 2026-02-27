from sqlmodel import SQLModel, Field, Relationship, Column, Integer
import uuid
from typing import Optional

class User(SQLModel, table = True):
    __tablename__ = "users"
    id : Optional[int] = Field(sa_column = Column(Integer, autoincrement = True, unique = True, primary_key = True))
    uuid : str = Field(default_factory = lambda : str (uuid.uuid4()))
    
    todos : list["Todo"] = Relationship(back_populates ="owner" )
    
    username : str
    email : str = Field(unique = True)
    password : str
    dob : str
    phoneNo : str = Field(unique = True)

class Todo(SQLModel, table = True):
    __tablename__ = "todos"
    id :Optional[int] = Field(sa_column = Column(Integer, autoincrement = True, unique = True, primary_key = True))
    
    user_id : int = Field(foreign_key = "users.id")
    
    title : str 
    description : str
    
    owner : Optional["User"] = Relationship(back_populates = "todos")

class TodoCreate(SQLModel):
    title : str
    description : str