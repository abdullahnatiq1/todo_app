from fastapi import APIRouter
from sqlmodel import Session
from db import getSession
import bcrypt



router = APIRouter(prefix="todo", tags=["Todo_App"])