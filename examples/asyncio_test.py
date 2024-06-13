"""
    异步IO ，协程
"""
import time
import asyncio
import uvloop

async def download(n: int) -> None:
    print(f"start download... {n}")
    await asyncio.sleep(n)
    print(f"finished download... {n}")

async def main():
    s1 = time.perf_counter()
    coro = []
    for i in [10, 9, 5]:
        co = asyncio.create_task(download(i))
        coro.append(co)


    """
    协程等待：
        
    """
    print(coro)
    for i in coro:
        await i

    print(f"cost time {time.perf_counter() - s1}")
    

if __name__ == '__main__':
    uvloop.run(main())
    