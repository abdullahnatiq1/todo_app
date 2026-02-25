from fastapi import FastAPI


app = FastAPI()
@app.get("/hello")
def func(user : str):
    return