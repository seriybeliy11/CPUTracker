from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from dash_app import dash_app
from measurements import cpu, update_msts, CPU_COUNT, ram

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Annotated

app = FastAPI()
app.mount('/dash/', WSGIMiddleware(dash_app.server))

security = HTTPBasic()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')


SECRET_KEY = '3dbc746b37592b90efe1b5b5d31adbfec98d7c390e7451a047d5bb86e9e4223b'
ALGORITHM = 'HS256'
HASHED_PASSWORD = '$2b$12$sQi32CyFD0fReswwDpssUuuw9sXVUeP.U0TH2zdmoYUkEzwWauCSG'



def verify_pwd(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)

def get_pwd_hash(pwd):
    return pwd_context.hash(pwd)

def auth_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    # global HASHED_PASSWORD

    # if not HASHED_PASSWORD:
    #     HASHED_PASSWORD = get_pwd_hash(pwd)
    #     print(HASHED_PASSWORD)

    if not verify_pwd(credentials.password, HASHED_PASSWORD):
        return False
    return credentials.username


@app.get('/cpu/')
def get_cpu(request: Request, user: Annotated[dict, Depends(auth_user)], cpu_id: int | None = None):
    
    if not user or user != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    update_msts()
    if cpu_id is not None:
        return {f'cpu{cpu_id+1}': cpu[cpu_id][-1]}
    else:
        return {f'cpu': [cpu[i][-1] for i in range(CPU_COUNT)]}
    
@app.get('/ram/')
def get_ram(
    request: Request,
    user: Annotated[dict, Depends(auth_user)]
):
    
    if not user or user != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return{f'ram': ram[0][-1]}

    
