from fastapi import FastAPI
from db import createDBandTables, reset_database
from routes import router as user_router

app = FastAPI()
@app.get("/hello")
def func(user : str):
    return

@app.on_event("startup")
def onStartup():
    createDBandTables()
    # reset_database()


app.include_router(user_router)
