#! python3
# -*- encoding: utf-8 -*-
'''
@File    : knowledge_base.py
@Time    : 2024/07/04 14:42:01
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''


from app.models.base import BaseTable

from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class KnowledgeBase(BaseTable):
    __tablename__ = "knowledge_bases"

    name: Mapped[str] = mapped_column(String(100), nullable=False, comment='知识库名称')
    hash_name: Mapped[str] = mapped_column(String(20), nullable=False, comment='知识库哈希名称')
    icon: Mapped[str] = mapped_column(String(100), nullable=False, comment='知识库图标')
    desc: Mapped[str] = mapped_column(String(200), nullable=False, comment='知识库描述')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, comment='用户ID')
    group_id: Mapped[int] = mapped_column(Integer, nullable=True, comment='团队ID')
    is_delete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True, comment='是否删除')

    user = relationship("User", back_populates="knowledge_bases")

    config = relationship('KnowledgeBaseConfig', back_populates='knowledge_base', cascade='all, delete-orphan', uselist=False)
    