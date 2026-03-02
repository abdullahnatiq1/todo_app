from fastapi import FastAPI
from db import createDBandTables, reset_database
from routes1 import router as user_router
# from middleware import authMiddleware
from fastapi.openapi.utils import get_openapi
from routes import auth_router
from routes import todo_router

app = FastAPI()

@app.on_event("startup")
def onStartup():
    createDBandTables()
    #reset_database()

# app.middleware("http")(authMiddleware)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(todo_router)


def customOpenAPI():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema =get_openapi(
        title= "Todo App",
        version= "1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type" : "http",
            "scheme" : "Bearer",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = customOpenAPI

