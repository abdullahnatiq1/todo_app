from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db import getSession
import bcrypt
from model import User


router = APIRouter(prefix="/todo", tags=["Todo_App"])


@router.post("/signup")
def signUp(username : str, email : str, password : str, dob : str, phoneNo : int, session : Session = Depends(getSession)):
    
    existingUser = session.exec(select(User).where (User.email == email)).first()
    if existingUser:
        return {"message" : "User already exists with this email. Please Login"}
    
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    newUser = User(username = username, email = email, password = hashedPassword, dob = dob, phoneNo = phoneNo,)
    session.add(newUser)
    session.commit()
    session.refresh(newUser)

    return{"Message" : "User created successfully"}


@router.post("/signin")
def signIn(email : str, password : str, session : Session = Depends(getSession)):
    user = session.exec(select(User).where (User.email == email)).first()

    if not user:
        return{"message" : "Email not found"}
    
    passwordMatch = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    if not passwordMatch:
        return{"message" : "Invalid password"}
    
    return{"message" : "Login successful"}

