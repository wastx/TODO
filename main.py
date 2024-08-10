from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from todo.routers import router

app = FastAPI()

app.include_router(router)
app.mount('/static', StaticFiles(directory='todo/static'), name='static')

