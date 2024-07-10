from redis.asyncio import Redis

import unittest
from unittest import TestCase

redis = Redis(host='localhost', port=6379, password='qsearch123', db=0)

async def taskLock(lock_name, redis):
    async with redis.lock(lock_name, timeout=10):
        print(f"Task started with lock: {lock_name}")
        # 模拟任务执行
        await asyncio.sleep(3)
        print(f"Task finished with lock: {lock_name}")

async def main():
    ping = await redis.ping()
    print(ping)

    hashname = await redis.hget('hashname', 'field')
    print(hashname)

    # 启动多个任务，尝试获取同一个锁
    tasks = [taskLock("lockname", redis) for _ in range(3)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # 异步 main 函数
    import sys
    import asyncio
    if sys.version_info < (3, 10):
        loop = asyncio.get_event_loop()
    else:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
    
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(main())