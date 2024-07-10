#! python3
# -*- encoding: utf-8 -*-
'''
@File    : background_task.py
@Time    : 2024/06/28 10:58:02
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''

from app.core.context import Context
from fastapi.background import BackgroundTasks

class TaskManager:
    """后台任务管理"""

    @classmethod
    async def init_tasks(cls):
        """实例化后台任务，并设置到上下文"""
        tasks = BackgroundTasks()
        Context.TASKS.set(tasks)

    @classmethod
    async def get_tasks(cls):
        """从上下文中获取后台任务实例"""
        return Context.TASKS.get()

    @classmethod
    async def add_task(cls, func, *args, **kwargs):
        """添加后台任务"""
        tasks = await cls.get_tasks()
        tasks.add_task(func, *args, **kwargs)

    @classmethod
    async def execute_tasks(cls):
        """执行后台任务，一般是请求结果返回之后执行"""
        bg_tasks = await cls.get_tasks()
        if bg_tasks.tasks:
            await bg_tasks()
