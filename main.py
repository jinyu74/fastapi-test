from datetime import datetime, timedelta
from typing import List
from fastapi import FastAPI, HTTPException, Depends, status, Cookie, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from models import Gender, Role, User, UserOut, UserUpdateRequest, UserPayload
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWSSignatureError
import bcrypt
from pydantic import EmailStr

app = FastAPI()
security = HTTPBearer()

ALGOROTHM = "HS256"
SECRET_KEY = "efd5b699cead31f4042c56f9896d2f925fa2479320a3a5fbc5dcaf52bcd4a77e"

db: List[User] = [
    User(
        id="james.yu@vuno.co",
        first_name="James",
        last_name="Yu",
        gender=Gender.female,
        roles=[Role.student],
        password="$2b$12$oBIZlFpv95ZsSZOS1ecqTuDuZmTt5ChqeZCcDPQoqLyGkaovOhthi",
    ),
    User(
        id="nathan.drake@vuno.co",
        first_name="Nathan",
        last_name="Drake",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
        password="$2b$12$oBIZlFpv95ZsSZOS1ecqTuDuZmTt5ChqeZCcDPQoqLyGkaovOhthi",
    ),
]


async def create_asccess_token(data: User, exp: timedelta = None):
    expire = datetime.utcnow() + (exp or timedelta(minutes=5))
    user_info = UserPayload(**data.dict(), exp=expire)

    return jwt.encode(user_info.dict(), SECRET_KEY, algorithm=ALGOROTHM)


async def get_user(cred: HTTPAuthorizationCredentials = Depends(security)):
    token = cred.credentials
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, ALGOROTHM)
    except ExpiredSignatureError:
        raise HTTPException(401, "Expired")
    except JWSSignatureError:
        raise HTTPException(403, "Wrong Token")
    user_info = User(**decoded_data)

    for user in db:
        if user.id == user_info.id:
            return user

    raise HTTPException(404, "Not Found User")


@app.get("/")
async def root():
    return {"Hello": "world"}


@app.get("/api/v1/users", response_model=List[UserOut])
async def fetch_users():
    return db


@app.post("/api/v1/users", status_code=status.HTTP_201_CREATED)
async def register_user(user: User):
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user.password = hashed_password.decode()
    db.append(user)

    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: EmailStr):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(status_code=404, detail=f"user with id: {user_id} does not exists")


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: EmailStr):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
    raise HTTPException(status_code=404, detail=f"user with id: {user_id} does not exists")


@app.post("/api/v1/login")
async def issue_token(data: OAuth2PasswordRequestForm = Depends()):
    for user in db:
        if user.id == data.username:
            if bcrypt.checkpw(data.password.encode(), user.password.encode()):
                return await  (user, exp=timedelta(minutes=5))
            raise HTTPException(401)

    raise HTTPException(status_code=404, detail=f"user with id: {data.username} does not exists")


@app.get("/api/v1/users/me", response_model=UserOut)
async def get_current_user(user: dict = Depends(get_user)):
    return user


@app.get("/cookie")
async def get_cookies(ga: str = Cookie(None)):
    return {"ga": ga}


@app.get("/header")
async def get_headers(x_token: str = Header(None, title="토큰")):
    return {"X-Token": x_token}
