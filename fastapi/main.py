import time
from starlette.types import ASGIApp, Receive, Scope, Send

class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            start_time = time.time()
            await self.app(scope, receive, send)
            process_time = time.time() - start_time
            logger.info(f"Request processed in {process_time:.4f} seconds")
        else:
            await self.app(scope, receive, send)

from loguru import logger

# 增加生命周期管理事件

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, TypedDict, cast
from fastapi import FastAPI, Request, Header
from httpx import AsyncClient

class State(TypedDict):
    client: AsyncClient

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    async with AsyncClient(app=app) as client:
        yield {"client": client}

app = FastAPI(lifespan=lifespan)

# 添加自定义中间件
app.add_middleware(LoggingMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.get("/lifespan")
async def read_root(request: Request) -> dict[str, Any]:
    logger.info(request.headers)
    base_url = f"http://{request.client.host}:{request.url.port}"
    client = cast(AsyncClient, request.state.client)
    response = await client.get(base_url)
    # return response.json()
    return {'user-agent' : request.headers.get('user-agent')}

@app.get("/items/")
async def read_items(
    user_agent: str = Header(None),
    host: str = Header(None),
    connection: str = Header(None),
    accept: str = Header(None),
    accept_language: str = Header(None),
    accept_encoding: str = Header(None),
):
    return {
        "user-agent": user_agent,
        "host": host,
        "connection": connection,
        "accept": accept,
        "accept-language": accept_language,
        "accept-encoding": accept_encoding
    }


if __name__ == "__main__":
    import uvicorn

    # 使用uvloop作为事件循环 
    # httptools作为HTTP服务器
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        loop="uvloop",
        http="httptools"
    )