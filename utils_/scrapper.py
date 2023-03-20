from typing import List
from bs4 import BeautifulSoup
import aiohttp
from structures import MangaRaw, PictureRaw


class MangaScrapper:
    """
    Provides scrapping from mintmanga.live
    """
    #__base_url__ = 'https://mintmanga.live'
    __base_url__ = 'https://readmanga.live'
    __headers__ = {
        'User-agent': 'Mozila',
    }

    async def get_manga_name(self, url, bigurl) -> str: #ok
        async with aiohttp.ClientSession(bigurl, headers=self.__headers__) as session:
            async with session.get(url) as resp:
                body = await resp.text()
                soup = BeautifulSoup(body, 'html.parser')

        name = soup.find('strong', class_='mobile-title', recursive=True).text
        print(name)
        return name

    async def get_manga_raw(self, url: str) -> MangaRaw:
        async with aiohttp.ClientSession(self.__base_url__, headers=self.__headers__) as session:
            async with session.get(url) as resp:
                body = await resp.text()
                soup = BeautifulSoup(body, 'html.parser')

        script = soup.find('div',
                           class_='reader-controller pageBlock container reader-bottom bordered-page-block') \
            .find('script', type='text/javascript')
        content = script.text
        prev_chapter_url, next_chapter_url, pics_raw = self._parse_picture_object_from_script(content)

        full_url = self.__base_url__ + url
        name = soup.find('strong', class_='mobile-title').text

        manga_raw = MangaRaw(
            name=name,
            url=full_url,
            next_chapter_url=next_chapter_url,
            prev_chapter_url=prev_chapter_url,
            pics_raw=pics_raw
        )
        return manga_raw

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
            url = url.split('?')
            pic_raw = PictureRaw(width, height, url[0])
            pics.append(pic_raw)
        print(pics)
        return prev_link, next_link, pics
