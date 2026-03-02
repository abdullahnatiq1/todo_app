from fastapi import Request, HTTPException
from fastapi.responses import Response
from utils import verifyToken
from sqlmodel import Session, select
from model import User
from db import engine


#ye humne public route is liya banaya hai ta k iski authorization na ho saka bcz we don't need that
publicRoutes = ["/todo/signup","/todo/signin", "/docs","/openapi.json"]

async def authMiddleware(request : Request):
    # if request.url.path in publicRoutes:
    #     return await call_next(request)

    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail = {"message" : "Token missing or invalid format"})
    
    token = token.split(" ")[1]

    payload = verifyToken(token)
    if not payload:
        raise HTTPException(status_code=401, detail = {"message" : "Invalid or expired token"})
    
    uuid = payload.get("sub")

    with Session(engine) as session:
        user = session.exec(select(User).where (User.uuid == uuid)).first()
    
    if not user:
        raise HTTPException(status_code=401, detail = {"message" : "User not found"})
    
    # request.state.user = user
    # return await call_next(request)

    return user

    