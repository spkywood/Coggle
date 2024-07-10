#! python3
# -*- encoding: utf-8 -*-
'''
@File    : users.py
@Time    : 2024/06/28 13:57:33
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''



import io
import base64
import random
import string
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from app.models.user import User
from redis.asyncio import Redis
from captcha.image import ImageCaptcha

from app.core.response import BaseResponse
from app.schemas.login import LoginRequest, JWTPayload
from app.core.oauth import authenticate_user, create_access_token
from settings import REDIS_HOST, REDIS_PORT, ACCESS_TOKEN_EXPIRE_MINUTES, REDIS_PASSWORD

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, password=REDIS_PASSWORD)

router = APIRouter()


@router.get("/captcha")
async def get_captcha() -> BaseResponse:
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    captcha_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    await redis.setex(captcha_id, 120, captcha_text)  # Captcha valid for 1 minutes
    image = ImageCaptcha().generate_image(captcha_text) 
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return BaseResponse(
        code=200,
        message="success",
        data={"captcha_id": captcha_id, "captcha_image": image_base64}
    )

@router.post("/users/login")
async def login(
    item: LoginRequest
) -> BaseResponse:
    """
    用户登录
    """
    captcha_text: str = await redis.get(item.captcha_id)
    if not captcha_text or captcha_text.lower() != item.captcha.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码输入错误",
        )

    user: User = await authenticate_user(item.username, item.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = JWTPayload(
        user_id=user.id,
        username=user.name,
        exp=expires
    )
    access_token = create_access_token(data=data)

    return BaseResponse(
        code=200,
        message="success",
        data = {
            "name" : user.name,
            "access_token": access_token,
            "token_type": "bearer",
        }
    )