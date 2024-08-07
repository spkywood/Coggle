#! python3
# -*- encoding: utf-8 -*-
'''
@File    : online_model.py
@Time    : 2024/07/04 14:35:25
@Author  : longfellow
@Version : 1.0
@Email   : longfellow.wang@gmail.com
'''


from openai import OpenAI, NOT_GIVEN, AsyncOpenAI
from typing import Union, List, Dict, Optional

from app.core.singleton import Singleton


class OnlineModel(metaclass=Singleton):
    def __init__(self, api_key, base_url):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.async_client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    def invoke(self,
        messages: Union[str, List[Dict[str, str]]],
        model: str = "qwen-max",
        tools : Optional[object] = NOT_GIVEN,
        top_p: float = 0.7,
        temperature: float = 0.7,
        max_tokens = 2000,
    ):
        completion = self.client.chat.completions.create(
            model = model,
            tools = tools,
            messages = messages,
            top_p = top_p,
            temperature = temperature,
            max_tokens = max_tokens,
            stream = False
        )

        return completion.choices[0].message.model_dump()
    
    def sse_invoke(self,
        messages: Union[str, List[Dict[str, str]]],
        model: str = "qwen-max",
        tools : Optional[object] = NOT_GIVEN,
        top_p: float = 0.7,
        temperature: float = 0.7,
        max_tokens = 2000,
    ):
        completion = self.client.chat.completions.create(
            model = model,
            tools = tools,
            messages = messages,
            top_p = top_p,
            temperature = temperature,
            max_tokens = max_tokens,
            stream = True
        )

        for chunk in completion:
            yield chunk.choices[0].delta.model_dump()


    async def ainvoke(self,
        messages: Union[str, List[Dict[str, str]]],
        model: str = "qwen-max",
        tools : Optional[object] = NOT_GIVEN,
        top_p: float = 0.7,
        temperature: float = 0.7,
        max_tokens = 2000,
    ):
        completion = await self.async_client.chat.completions.create(
            model = model,
            tools = tools,
            messages = messages,
            top_p = top_p,
            temperature = temperature,
            max_tokens = max_tokens,
            stream = False
        )

        return completion.choices[0].message.model_dump()


    async def asse_invoke(self,
        messages: Union[str, List[Dict[str, str]]],
        model: str = "qwen-max",
        tools : Optional[object] = NOT_GIVEN,
        top_p: float = 0.7,
        temperature: float = 0.7,
        max_tokens = 2000,
    ):
        completion = await self.async_client.chat.completions.create(
            model = model,
            tools = tools,
            messages = messages,
            top_p = top_p,
            temperature = temperature,
            max_tokens = max_tokens,
            stream = True
        )

        async for chunk in completion:
            yield chunk.choices[0].delta.model_dump()
