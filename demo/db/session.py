#! python3
# -*- encoding: utf-8 -*-
'''
@File    : session.py
@Time    : 2024/06/26 13:40:12
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''



from functools import wraps
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from settings import SQLALCHEMY_DATABASE_URI

db_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=True,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = async_sessionmaker(
    engine=db_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@asynccontextmanager
async def session_scope():
    async with SessionLocal() as session:
        async with session.begin():
            yield session

def with_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with session_scope() as session:
            return await func(session, *args, **kwargs)
    return wrapper