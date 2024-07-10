#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   startup.py
@Time    :   2024/06/11 13:57:53
@Author  :   wangxh 
@Version :   1.0
@Email   :   longfellow.wang@gmail.com
'''



from fastapi import FastAPI
from typing import TypedDict
from httpx import AsyncClient
from fastapi.middleware import Middleware
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


from app.api import api_router
from app.core.middlewares import LoggingMiddleware, BackGroundTaskMiddleware

class State(TypedDict):
    client: AsyncClient

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    async with AsyncClient(app=app) as client:
        yield {"client": client}

def add_middlewares():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(LoggingMiddleware),
        Middleware(BackGroundTaskMiddleware),
    ]
    return middleware

def mount_app_routers(app: FastAPI, prefix: str = "/api"):
    app.include_router(api_router, prefix=prefix)


def create_app() -> FastAPI:
    app = FastAPI(
        title="API Server",
        description="settings.APP_DESCRIPTION",
        version="0.1.0",
        openapi_url="/openapi.json",
        middleware=add_middlewares(),
        lifespan=lifespan,
    )

    mount_app_routers(app)

    return app

if __name__ == '__main__':
    import uvicorn
    app = create_app()
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        loop="uvloop",
        http="httptools"
    )
    