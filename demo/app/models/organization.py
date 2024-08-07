#! python3
# -*- encoding: utf-8 -*-
'''
@File    : origanization.py
@Time    : 2024/06/13 17:53:54
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''


from app.models.base import BaseTable

from sqlalchemy import String
from sqlalchemy.orm import (
    relationship, mapped_column, Mapped
)

class Organization(BaseTable):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    