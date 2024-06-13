import aiohttp
import asyncio
import uvloop
import json
import base64
import os
import functools
from contextlib import asynccontextmanager

# session
@asynccontextmanager
async def session_scope():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        yield session

def with_session(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with session_scope() as session:
            return await func(session, *args, **kwargs)
    return wrapper


@with_session
async def fetch(session, url, item_id):
    print(id(session))
    async with session.get(url) as response:
        try:
            json_obj = json.loads(await response.text())
        except json.decoder.JSONDecodeError as e:
            print(f'Download failed - {url}')
            return
        image_str = json_obj['dataUri'].replace('data:image/jpeg;base64,', '')
        image_data = base64.b64decode(image_str)
        save_folder = dir_path = os.path.dirname(
            os.path.realpath(__file__)) + '/google_earth/'
        with open(f'{save_folder}{item_id}.jpg', 'wb') as f:
            f.write(image_data)
        print(f'Download complete - {item_id}.jpg')

async def main():
    start = 1032
    end = 1041
    for i in range(start, end + 1):
        url = f"https://www.gstatic.com/prettyearth/assets/data/v2/{i}.json"
        await fetch(url, i)



if __name__ == '__main__':
    import sys
    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    else:
        uvloop.install()
        asyncio.run(main())