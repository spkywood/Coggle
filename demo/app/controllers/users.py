#! python3
# -*- encoding: utf-8 -*-
'''
@File    : users.py
@Time    : 2024/07/04 15:46:01
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''


from sqlalchemy import and_
from sqlalchemy.future import select

from app.models.user import User
from db.session import with_session

@with_session
async def query_user_with_name(session, name):
    query = await session.execute(select(User).where(User.name == name))
    user = query.scalar_one_or_none()
    
    return user