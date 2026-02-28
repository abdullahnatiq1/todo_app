from fastapi import APIRouter, Depends, Header  # 
from sqlmodel import Session, select
from db import getSession
import bcrypt
from model import User, Todo, TodoCreate
from utils import createToken, verifyToken
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional


router = APIRouter(prefix="/todo", tags=["Todo_App"])

security = HTTPBearer()

def getCurrentUser(
    credentials: HTTPAuthorizationCredentials = Depends(security),   # jab user token k sath request bhejta hai header ko to HTTPBearer() usko automatically  credentials ma store krwa deta hai
    session: Session = Depends(getSession)) -> User:
    
    token = credentials.credentials    # credentials object hai asal token string .credentials k ander store hai or hum usko token ma store krwa raha ab 

    payload = verifyToken(token)    #  yahan token pass kr raha to check if it correct or not

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")   # agar token galat hoga to raise error 

    uUID = payload.get("sub")
    user = session.exec(select(User).where(User.uuid == uUID)).first()
    print("UUID from token", uUID)
    print("user found", user)
    if not user:
        {"message" : "User not found"}

    return user


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
    
    token = createToken(data={"sub" : user.uuid})
    
    return{"message" : "Login successful",
           "token" : token
           }


@router.post("/create")
def createTodo(todo : TodoCreate, session: Session = Depends(getSession), currentUser: User = Depends(getCurrentUser)):
    newTodo = Todo(title = todo.title, description = todo.description, user_id=currentUser.id)
    session.add(newTodo)
    session.commit()
    session.refresh(newTodo)
    return {"message": "Todo created successfully", "todo": newTodo}


@router.get("/all")
def getAllTodos(session : Session = Depends(getSession), currentUser : User = Depends(getCurrentUser)):
    todos = session.exec(select(Todo).where (Todo.user_id == currentUser.id)).all()
    return{"todos" : todos}
    

@router.patch("/update/{todoID}")   # put sara data change kr deta hai or == sirf field ko change krta haiii
def updateTodo(todoID : int, title : Optional[str] = None, description : Optional[str] = None, session : Session = Depends(getSession), currentUser : User = Depends(getCurrentUser)):
    todo = session.exec(select(Todo).where(Todo.id == todoID, Todo.user_id == currentUser.id)).first()

    if not todo:
        return{"message" : "Todo not found"}

    if title:
        todo.title = title
    if description:
        todo.description = description

    session.commit()
    session.refresh(todo)
    
    return{"message" : "Todo updated successfully","todo" : todo}

@router.delete("/delete/{todoID}")
def deleteTodo(todoID : int,session : Session = Depends(getSession), currentUser : User = Depends(getCurrentUser)):
    todo = session.exec(select(Todo).where(Todo.id == todoID, Todo.user_id == currentUser.id)).first()

    if not todo:
        return{"message" : "Todo not found"}
    
    session.delete(todo)
    session.commit()

    return{"message" : "Todo deleted successfully"}
                   