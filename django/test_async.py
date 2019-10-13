import asyncio
import time


async def pretty_long_function():
    await asyncio.sleep(2.0)
    return 2


async def get_item():
    await asyncio.sleep(1.0)
    return 1


async def main():
    fa = pretty_long_function()
    # this starts it immediately, otherwise it starts when actually being awaited
    fa = asyncio.ensure_future(fa)
    b = await get_item()
    a = await fa
    print(a+b)


if __name__ == "__main__":
    start = time.perf_counter()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    print('Time:', time.perf_counter() - start)
