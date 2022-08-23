from fastapi import FastAPI
from apis import router

app = FastAPI()

app.include_router(router)
