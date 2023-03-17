import asyncio
from asyncinit import asyncinit
from typing import List
from bs4 import BeautifulSoup
import aiohttp
from structures import MangaRaw, PictureRaw


@asyncinit
class MangaScrapper:
    """
    Provides scrapping from mintmanga.live
    """

    __url__ = 'https://mintmanga.live'
    __headers__ = {
        'User-agent': 'Mozila',
    }

    async def __init__(self, path: str):
        self.path = self._validate_path(path)

        async with aiohttp.ClientSession(self.__url__, headers=self.__headers__) as session:
            async with session.get(self.path) as resp:
                body = await resp.text()
                self._soup = BeautifulSoup(body, 'html.parser')

        self._name = None
        self._next_chapter_url = None
        self._prev_chapter_url = None
        self._pics_raw = None

    def _validate_path(self, url: str):
        if self.__url__ in url:
            return url.replace(self.__url__, '')
        elif not url.startswith('/'):
            return f'/{url}'
        return url

    @property
    def name(self):
        return self._name or self._parse_name()

    @property
    def next_chapter_url(self):
        if self._next_chapter_url is None:
            self._parse_manga_raw()
        return self._next_chapter_url

    @property
    def prev_chapter_url(self):
        if self._prev_chapter_url is None:
            self._parse_manga_raw()
        return self._next_chapter_url

    @property
    def pics_raw(self):
        if self._next_chapter_url is None:
            self._parse_manga_raw()
        return self._pics_raw

    @property
    def manga_raw(self):
        if not all([self._next_chapter_url, self._prev_chapter_url, self._pics_raw]):
            self._parse_manga_raw()
        if not self._name:
            self._parse_name()

        manga_raw = MangaRaw(
            name=self._name,
            url=self.__url__ + self.path,
            next_chapter_url=self._next_chapter_url,
            prev_chapter_url=self._prev_chapter_url,
            pics_raw=self._pics_raw
        )
        return manga_raw

    def _parse_name(self) -> str:
        name = self._soup.find('strong', class_='mobile-title').text
        self._name = name
        return name

    def _parse_manga_raw(self):
        script = self._soup.find('div',
                                 class_='reader-controller pageBlock container reader-bottom bordered-page-block') \
            .find('script', type='text/javascript')
        content = script.text
        prev_chapter_url, next_chapter_url, pics_raw = self._parse_picture_object_from_script(content)
        self._prev_chapter_url = prev_chapter_url
        self._next_chapter_url = next_chapter_url
        self._pics_raw = pics_raw

    def _parse_picture_object_from_script(self, script: str) -> tuple[str, str, List[PictureRaw]]:
        prev_link = script[script.find('var prevChapterLink = \"') + len('var prevChapterLink = \"'):]
        prev_link = prev_link[:prev_link.find('\"')]

        next_link = script[script.find('var nextChapterLink = \"') + len('var nextChapterLink = \"'):]
        next_link = next_link[:next_link.find('\"')]

        links = script[script.find('[[') + 1:]
        links = links[:links.find(']]') + 1]

        pics = []
        while links.find('[') != -1:
            sub = links[links.find('['): links.find(']') + 1]
            links = links.replace(sub, '')
            sub = sub.replace('\',\'\',\"', '')
            sub = sub.replace('[\'', '').replace('\"', '').replace(']', '')
            split = sub.split(',')
            url = split[0]
            width = int(split[1])
            height = int(split[2])
            pic_raw = PictureRaw(width, height, url)
            pics.append(pic_raw)

        return prev_link, next_link, pics
