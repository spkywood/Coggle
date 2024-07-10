#! python3
# -*- encoding: utf-8 -*-
'''
@File    : schemas.py
@Time    : 2024/07/04 16:06:05
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''


from datetime import datetime
from pydantic import BaseModel


class JWTPayload(BaseModel):
    user_id: int
    username: str
    exp: datetime

class LoginRequest(BaseModel):
    username: str
    password: str
    captcha_id: str
    captcha: str