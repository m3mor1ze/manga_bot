from typing import Dict
from telegraph.aio import Telegraph
from structures import MangaRaw


class TelegraphForManga(Telegraph):
    """
    Extends Telegraph interface.
    Provides working with manga using MangaRaw structure
    """
    def __init__(self, author, author_url=None, access_token=None, domain='telegra.ph'):
        super().__init__(access_token, domain)
        self.author = author
        self.author_url = author_url

    async def get_manga(self, name: str) -> Dict | None:
        """
        Finds a manga from existing pages
        :param name:
        :return: url if page exists, else None
        """
        page_list = await self.get_page_list()
        for page in page_list['pages']:
            if isinstance(name, str) and page['title'] == name:
                return page
        return None

    async def post_manga(self, manga_raw: MangaRaw) -> Dict:
        """
        Creates manga page
        :param manga_raw:
        :return: telegraph url
        """
        tagged_pics = [f'<img src={x.pic_url}>' for x in manga_raw.pics_raw]
        html = '\n'.join(tagged_pics)

        page = await self.create_page(
            title=manga_raw.name,
            html_content=html,
            author_name=self.author,
            author_url=self.author_url,
        )
        return page
