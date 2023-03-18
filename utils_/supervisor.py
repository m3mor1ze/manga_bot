from utils_.scrapper import MangaScrapper
from utils_.manga_telegraph import TelegraphForManga
from configs_.config import *


class Supervisor:
    def __init__(self):
        self.scrapper = MangaScrapper()
        self.poster = TelegraphForManga(
            author=TELEGRAPH_AUTHOR(),
            access_token=TELEGRAPH_TOKEN()
        )

    def _parse_url(self, msg):
        base_url = 'https://mintmanga.live'
        url = msg['text']
        if base_url in url:
            return url.replace(base_url, '')
        elif not url.startswith('/'):
            return f'/{url}'
        return url

    # BOT USABLE API
    async def get_manga(self, msg):
        url = self._parse_url(msg)
        print(f'processing: {url}')
        name = await self.scrapper.get_manga_name(url)
        manga = await self.poster.get_manga(name)

        if manga is None:
            print('creating new post')
            raw_manga = await self.scrapper.get_manga_raw(url)
            manga = await self.poster.post_manga(raw_manga)

        return manga.get('url')
