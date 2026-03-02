from fastapi import APIRouter, Depends, Header  # 
from sqlmodel import Session, select
from db import getSession
from model import User, Todo, TodoCreate, UpdateTodo
from typing import Optional
from fastapi.responses import JSONResponse
from db import engine
from middleware import authMiddleware

router = APIRouter(prefix="/todo", tags=["Todo_App_CRUD"])





                   