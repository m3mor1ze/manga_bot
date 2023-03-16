import asyncio
from bs4 import BeautifulSoup
import aiohttp


async def scrap(url):
    async with aiohttp.ClientSession('https://mintmanga.live', headers={'User-agent': 'Mozila'}) as session:
        print(session)

        async with session.get(url) as resp:
            body = await resp.text()
            soup = BeautifulSoup(body, 'html.parser')

            # ЗДЕСЬ НАДО НАЙДИ ТЕГ img В КОТОРОМ ВСЕ ДАННЫЕ ПО КАРТИНКУ И ВЫТЯНУТЬ
            # ССЫЛКУ НА КАРТИНКУ И ЕЕ РАЗМЕРЫ
            x = soup.findAll('img', class_='manga-img_0 manga-img')

            print(x)
            print(len(x))
