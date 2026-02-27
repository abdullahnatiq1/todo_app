from fastapi import APIRouter, Depends, Header
from sqlmodel import Session, select
from db import getSession
import bcrypt
from model import User, Todo, TodoCreate
from utils import createToken, verifyToken
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter(prefix="/todo", tags=["Todo_App"])

security = HTTPBearer()

def getCurrentUser(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(getSession)) -> User:
    
    token = credentials.credentials

    payload = verifyToken(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    uUID = payload.get("sub")
    user = session.exec(select(User).where(User.uuid == uUID)).first()

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
    
