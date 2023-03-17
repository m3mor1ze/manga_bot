from configs.config import *
from utils.scrapper import MangaScrapper
from utils.manga_telegraph import TelegraphForManga


class Supervisor:
    def __init__(self):
        self.poster = TelegraphForManga(
            author=TELEGRAPH_AUTHOR,
            access_token=TELEGRAPH_TOKEN
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
        scrapper = await MangaScrapper(url)
        manga = await self.poster.get_manga(scrapper.name)

        if manga is None:
            print('creating new post')
            manga = await self.poster.post_manga(scrapper.manga_raw)

        return manga.get('url')
