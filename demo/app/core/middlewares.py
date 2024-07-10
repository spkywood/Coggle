#! python3
# -*- encoding: utf-8 -*-
'''
@File    : middlewares.py
@Time    : 2024/06/26 13:51:06
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''


import time
from loguru import logger
from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.task_manager import TaskManager


class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            start_time = time.time()
            await self.app(scope, receive, send)
            process_time = time.time() - start_time
            logger.info(f"Request {scope['path']} cost {process_time:.4f} seconds")
        else:
            await self.app(scope, receive, send)

class SimpleBaseMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)

        response = await self.before_request(request) or self.app
        await response(request.scope, request.receive, send)
        await self.after_request(request)

    async def before_request(self, request: Request):
        return self.app

    async def after_request(self, request: Request):
        return None


class BackGroundTaskMiddleware(SimpleBaseMiddleware):
    async def before_request(self, request):
        await TaskManager.init_tasks()

    async def after_request(self, request):
        await TaskManager.execute_tasks()
