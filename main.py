from asyncscrap import scrap
import asyncio

URL = '/saga_o_vinlande__A35c96/vol1/1'

if __name__ == '__main__':
    asyncio.run(scrap(URL))