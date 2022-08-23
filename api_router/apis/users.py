from fastapi import APIRouter


router = APIRouter()

fake_users = [{"user_name": "John"}, {"user_name": "Nathan"}, {"user_name": "Joel"}]


@router.get("/")
async def read_user(skip: int = 0, limit: int = 10):
    return fake_users[skip : skip + limit]
