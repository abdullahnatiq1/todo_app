from fastapi import APIRouter,Depends
from model import User, TodoCreate, Todo, UpdateTodo
from sqlmodel import Session, select
from db import getSession
from middleware import authMiddleware


router = APIRouter(prefix="/todo", tags=["Todo App CRUD"])
      
@router.get("/all")
def getAllTodos(session : Session = Depends(getSession), currentUser : User = Depends(authMiddleware)):
    todos = session.exec(select(Todo).where (Todo.user_id == currentUser.id)).all()
    return{"todos" : todos}


@router.post("/create")
def createTodo(todo : TodoCreate, session: Session = Depends(getSession), currentUser: User = Depends(authMiddleware)):
    newTodo = Todo(title = todo.title, description = todo.description, user_id=currentUser.id)
    session.add(newTodo)
    session.commit()
    session.refresh(newTodo)
    return {"message": "Todo created successfully", "todo": newTodo}


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