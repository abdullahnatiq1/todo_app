from jose import jwt 
from datetime import timedelta, datetime

SECRET_KEY = "your-secret-key"
algorithm = "HS256"

def createToken(data : dict):
    expire = datetime.utcnow() + timedelta(hours = 24)
    data.update({"exp" : expire})
    token = jwt.encode(data, SECRET_KEY, algorithm=algorithm)
    return token
