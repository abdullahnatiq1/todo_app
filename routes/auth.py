from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from model import User, SigninRequest, SignupRequest
from middleware import authMiddleware
from db import getSession
import bcrypt
from utils import createToken


router = APIRouter(prefix="/auth", tags=["Todo_app_Routes"])


@router.get("/me")
def authenticated(currentUser : User = Depends(authMiddleware)):

    return {"user" : currentUser}


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
