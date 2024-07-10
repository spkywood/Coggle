#! python3
# -*- encoding: utf-8 -*-
'''
@File    : context.py
@Time    : 2024/06/28 10:55:06
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''


import contextvars
from fastapi.background import BackgroundTasks

class Context:
    USER_ID: contextvars.ContextVar[int] = contextvars.ContextVar("user_id", default=0)
    TASKS: contextvars.ContextVar[BackgroundTasks] = contextvars.ContextVar("background_task", default=None)
