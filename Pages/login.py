
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt  


from database import User



from fastapi import HTTPException

from datetime import datetime, timedelta

# Clave secreta para firmar el JWT
SECRET_KEY = "123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

async def login_user(request_login):
    # Verifica las credenciales del usuario
    username = request_login.username
    password = request_login.password
    token = await authenticate_user(username, password)
    return {"access_token": token, "token_type": "bearer"}

async def authenticate_user(username: str, password: str):

    user = User.get_or_none(User.username == username)

    if user is None or not user.password == password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        "sub": user.username,
        "exp": datetime.utcnow() + access_token_expires,
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)

    return access_token