from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup
import aiohttp


@dataclass
class PictureRaw:
    width: int
    height: int
    pic_url: str


@dataclass
class MangaRaw:
    name: str
    url: str
    length: int
    pics_raw: List[PictureRaw]


class MangaScrapper:
    """
    Provides interface for getting list of picture links
    """

    __base_url__ = 'https://mintmanga.live'
    __headers__ = {
        'User-agent': 'Mozila',
        'Content-disposition': 'attachment',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    async def ge_manga_raw(self, url: str) -> MangaRaw:
        async with aiohttp.ClientSession(self.__base_url__, headers=self.__headers__) as session:
            async with session.get(url) as resp:
                body = await resp.text()
                soup = BeautifulSoup(body, 'html.parser')

        script = soup.find('div',
                           class_='reader-controller pageBlock container reader-bottom bordered-page-block') \
            .find('script', type='text/javascript')

        content = script.text
        manga_raw = self.parse_picture_object_from_script(content)
        return manga_raw

    def parse_picture_object_from_script(self, script: str) -> MangaRaw:
        return script
