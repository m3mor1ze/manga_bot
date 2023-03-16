from configs.config import *
from utils.scrapper import MangaScrapper
from utils.manga_telegraph import TelegraphForManga


class Supervisor:
    def __init__(self):
        self.scrapper = MangaScrapper()
        self.poster = TelegraphForManga(TELEGRAPH_AUTHOR, TELEGRAPH_TOKEN)

    def _parse_url(self, msg):
        return msg['text']

    # BOT USABLE API
    async def get_manga(self, msg):
        url = self._parse_url(msg)
        manga = await self.poster.get_manga(url)
        if manga is None:
            raw_manga = await self.scrapper.get_manga_raw(url)
            manga = await self.poster.post_manga(raw_manga)
        return manga['url']
