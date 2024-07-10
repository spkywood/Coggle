#! python3
# -*- encoding: utf-8 -*-
'''
@File    : llms.py
@Time    : 2024/07/05 08:53:37
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''


import uuid
import json
from sse_starlette.sse import EventSourceResponse
from loguru import logger
from fastapi import APIRouter, Depends

from app.core.oauth import get_current_user
from app.models.user import User
from app.schemas.llm import ChatCreate

router = APIRouter()


@router.post("/chat/sessions", summary="创建会话", include_in_schema=True)
async def create_chat(
    item: ChatCreate,
    user: User = Depends(get_current_user)
):
    pass