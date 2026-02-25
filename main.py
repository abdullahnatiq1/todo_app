from fastapi import FastAPI
from db import createDBandTables

app = FastAPI()
@app.get("/hello")
def func(user : str):
    return

@app.on_event("startup")
def onStartup():
    createDBandTables()
