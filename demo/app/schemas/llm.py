#! python3
# -*- encoding: utf-8 -*-
'''
@File    : llm.py
@Time    : 2024/07/05 08:58:43
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''



from pydantic import BaseModel, Field

class ChatCreate(BaseModel):
    topic: str = "default"