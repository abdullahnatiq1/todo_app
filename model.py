from sqlmodel import SQLModel, Field, Relationship
import uuid
from typing import Optional

class User(SQLModel, table = True):
    __tablename__ = "users"
    id : int = Field(default = None, sa_column_kwargs = {"autoincrement" : True, "unique" : True})
    uuid : str = Field(default_factory = lambda : str (uuid.uuid4()), primary_key = True)
    
    todos : list["Todo"] = Relationship(back_populates ="owner" )
    
    username : str
    email : str = Field(unique = True)
    password : str
    dob : str
    phoneNo : int = Field(unique = True)

class Todo(SQLModel, table = True):
    __tablename__ = "todos"
    id : int = Field(default = None, sa_column_kwargs = {"autoincrement" : True, "unique" : True})
    
    user_uuid : str = Field(foreign_key = "users.uuid", primary_key = True)
    
    title : str 
    description : str
    
    owner : Optional["User"] = Relationship(back_populates = "todos")

