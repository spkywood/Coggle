#! python3
# -*- encoding: utf-8 -*-
'''
@File    : guide.py
@Time    : 2024/06/11 15:57:20
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''


from app.models.base import BaseTable
import enum

from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import (
    relationship, mapped_column, Mapped
)

class QAType(enum.Enum):
    LLM = "LLM"
    RAG = "RAG"
    TOOL = "TOOL"


class Guide(BaseTable):
    __tablename__ = "guides"

    content: Mapped[str] = mapped_column(String(2000))
    qa_type: Mapped[QAType] = mapped_column(Enum(QAType), nullable=False, default=QAType.LLM)
