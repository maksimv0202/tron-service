from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from accounts.router import router
from utils.migrations import lifespan

app = FastAPI(
    title='Title',
    description='Description.',
    version='1.0.0',
    root_path='/api/v1',
    lifespan=lifespan
)

origins = ['http://localhost', 'http://localhost:8080']

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST', 'GET'],
    allow_headers=['*'])


app.include_router(router)

