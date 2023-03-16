import asyncio
from typing import Dict
from configs.config import TELEGRAPH_TOKEN
from telegraph.aio import Telegraph
from structures import MangaRaw


class TelegraphForManga(Telegraph):
    def __init__(self, author, access_token=None, domain='telegra.ph'):
        super().__init__(access_token, domain)
        self.author = author

    # TODO: логика на данном этапе неправильная.
    #  нужно в статье хранить ссылку на оригинал манги. по ней и проводить сравнение
    async def get_manga(self, manga: str | MangaRaw) -> Dict | None:
        """
        Finds a manga from existing pages
        :param manga:
        :return: url if page exists, else None
        """
        page_list = await self.get_page_list()
        for page in page_list['pages']:
            if isinstance(manga, str) and page['title'] == manga:
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
        )
        return page


async def example():
    t = TelegraphForManga(TELEGRAPH_TOKEN)
    # print(resp)
    #
    # print('*' * 20)
    # resp = await t.get_manga('qwe')



if __name__ == '__main__':
    asyncio.run(example())
