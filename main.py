from asyncscrap import MangaScrapper
import asyncio

async def example():
    ls = MangaScrapper()
    res = await ls.ge_manga_raw('/saga_o_vinlande__A35c96/vol1/1#page=5')
    print(res)

if __name__ == '__main__':
    asyncio.run(example())
