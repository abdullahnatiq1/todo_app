from fastapi import APIRouter, Depends, Header  # 
from sqlmodel import Session, select
from db import getSession
import bcrypt
from model import User, Todo, TodoCreate, SigninRequest, SignupRequest, UpdateTodo
from utils import createToken
from typing import Optional
from fastapi.responses import JSONResponse
from db import engine
from middleware import authMiddleware


router = APIRouter(prefix="/todo", tags=["Todo_App"])
      
@router.post("/signup")
def signUp(SignupRequest: SignupRequest,  session : Session = Depends(getSession)):
    print("debudding signup request")
    print(SignupRequest)
    existingUser = session.exec(select(User).where (User.email == SignupRequest.email)).first()
    if existingUser:
        return {"message" : "User already exists with this email. Please Login"}
    
    hashedPassword = bcrypt.hashpw(SignupRequest.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    newUser = User(username = SignupRequest.username, email = SignupRequest.email, password = hashedPassword, dob = SignupRequest.dob, phoneNo = SignupRequest.phoneNo,)
    session.add(newUser)
    session.commit()
    session.refresh(newUser)

    return{"Message" : "User created successfully"}


@router.post("/signin")
def signIn(signInRequest: SigninRequest, session : Session = Depends(getSession)): # request: Request
    user = session.exec(select(User).where (User.email == signInRequest.email)).first()
    
    if not user:
        return{"message" : "Email not found"}
    
    passwordMatch = bcrypt.checkpw(signInRequest.password.encode('utf-8'), user.password.encode('utf-8'))
    if not passwordMatch:
        return{"message" : "Invalid password"}
    
    token = createToken(data={"sub" : user.uuid})
    
    return{"message" : "Login successful",
           "token" : token
           }


@router.post("/create")
def createTodo(todo : TodoCreate, session: Session = Depends(getSession), currentUser: User = Depends(authMiddleware)):
    newTodo = Todo(title = todo.title, description = todo.description, user_id=currentUser.id)
    session.add(newTodo)
    session.commit()
    session.refresh(newTodo)
    return {"message": "Todo created successfully", "todo": newTodo}


@router.get("/all")
def getAllTodos(session : Session = Depends(getSession), currentUser : User = Depends(authMiddleware)):
    todos = session.exec(select(Todo).where (Todo.user_id == currentUser.id)).all()
    return{"todos" : todos}
    

@router.patch("/update")   # put sara data change kr deta hai or == sirf field ko change krta haiii
def updateTodo(todoID : int, updateTodo : UpdateTodo, session : Session = Depends(getSession), currentUser : User = Depends(authMiddleware)):
    todo = session.exec(select(Todo).where(Todo.id == todoID, Todo.user_id == currentUser.id)).first()

    if not todo:
        return{"message" : "Todo not found"}

    if updateTodo.title:
        todo.title = updateTodo.title
    if updateTodo.description:
        todo.description = updateTodo.description

    session.commit()
    session.refresh(todo)
    
    return{"message" : "Todo updated successfully","todo" : todo}

@router.delete("/delete/{todoID}")
def deleteTodo(todoID : int,session : Session = Depends(getSession), currentUser : User = Depends(authMiddleware)):
    todo = session.exec(select(Todo).where(Todo.id == todoID, Todo.user_id == currentUser.id)).first()

    if not todo:
        return{"message" : "Todo not found"}
    
    session.delete(todo)
    session.commit()

    return{"message" : "Todo deleted successfully"}

@router.get("/auth/me")
def authenticated(currentUser : User = Depends(authMiddleware)):
    # if not User:
    #     return{"message" :"User not found"}


    return {"user" : currentUser}
                   