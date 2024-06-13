from enum import Enum
from fastapi import FastAPI, Query, Body
from typing import Annotated

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/item/{item_id}")
async def root(item_id: str):
    return {"message": f"Hello {item_id}"}

# 路径参数

@app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# 请求参数

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# 请求提

from pydantic import BaseModel

from typing import Union

"""
FastAPI 将识别出与路径参数匹配的函数参数应从路径中获取，
        而声明为 Pydantic 模型的函数参数应从请求体中获取。
"""
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.post("/items")
async def create_item(item: Item):
    # print(item)
    # fake_items_db.append(item)

    # item_dict = item.dict() # deprecated
    item_dict = item.model_dump()
    print(item_dict)
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     # return {"item_id": item_id, **item.dict()}
#     return {"item_id": item_id, **item.model_dump()}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Union[str, None] = None):
    # result = {"item_id": item_id, **item.dict()}
    result = {"item_id": item_id, **item.model_dump()}
    if not q:
        result.update({"q": "qwer"})
    else:
        result.update({"q": q})
    return result

# 参数校验

@app.post("/add_user")
async def read_items(name: Annotated[str, Body()], 
                     passwd: Annotated[str, Body()], 
                     email: Annotated[str, Body(
                         regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                     )]):
    result = {
        "name" : name,
        "passwd" : passwd,
        "email" : email
    }
    return result

import asyncio
from sse_starlette.sse import EventSourceResponse

async def event_generator():
    # 模拟一个生成事件的异步任务
    for i in range(1, 11):
        # 生成一个事件消息
        yield {
            "event": "message",
            "data": f"Message {i}"
        }
        """
        加sleep ,否则 sse_starlette.sse 中 listen_for_disconnect 
        收不到 http.disconnect 信号。这个表现是服务端的sse传输不会结束,
        会一直传递下去（虽然客户端 close或者disconnect)。
        """
        await asyncio.sleep(1)

@app.get("/events")
async def get_events():
    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=6008)