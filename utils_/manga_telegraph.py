import os
from typing import Dict
from telegraph.aio import Telegraph
from structures import MangaRaw
import requests
from aiogram.utils import json

def telegraph_file_upload(path_to_file):  # uploads image on telegram server
    file_types = {'gif': 'image/gif', 'jpeg': 'image/jpeg', 'jpg': 'image/jpg', 'png': 'image/png', 'mp4': 'video/mp4'}
    file_ext = path_to_file.split('.')[-1]
    if file_ext in file_types:
        file_type = file_types[file_ext]
    else:
        return f'error, {file_ext}-file can not be proccessed'
    with open(path_to_file, 'rb') as f:
        url = 'https://telegra.ph/upload'
        response = requests.post(url, files={'file': ('file', f, file_type)}, timeout=999)
    telegraph_url = json.loads(response.content)
    telegraph_url = telegraph_url[0]['src']
    telegraph_url = f'https://telegra.ph{telegraph_url}'

    return telegraph_url

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
                return None
        return None

    async def post_manga(self, manga_raw: MangaRaw, chat_id) -> Dict:
        """
        Creates manga page
        :param manga_raw:
        :return: telegraph url
        """
        tagged_pics = [f'<img src={x.pic_url}>' for x in manga_raw.pics_raw]
        #print(tagged_pics)
        #comment code below to post raw non-telegraph pics
        #---------------------------------------------------------------------------------------------------------------
        '''
        num = 0
        for x in manga_raw.pics_raw:
            filename = str(chat_id) + "--" + str(num) + ".jpg"
            p = requests.get(x.pic_url)
            print("chat_id = ",chat_id)
            print(filename)
            out = open(filename, "wb")
            out.write(p.content)
            out.close()
            #---------------------------------------
            upload_status = 0

            if (x.width / x.height <= 20):
                if (x.height / x.width <= 20):
                    while (upload_status == 0):
                        if (upload_status == 0):
                            try:
                                sgs = telegraph_file_upload(filename)
                                upload_status = 1
                                print(filename + ": uploaded successfully!")
                            except:
                                upload_status = 0

                                print(filename + ": error uploading pic!")

            path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), filename)
            os.remove(path)
            sgs = '<img src="' + sgs + '">'
            #print(sgs)
            tagged_pics[num] = sgs
            num += 1
            #str_all = str_all + sgs + "\n"
            #---------------------------------------------------------------------------------------------------------------
        '''
        html = '\n'.join(tagged_pics)

        page = await self.create_page(
            title=manga_raw.name,
            html_content=html,
            author_name=self.author,
            author_url=self.author_url,
        )
        return page

    async def post_mobile(self, manga_raw: MangaRaw, chat_id) -> Dict:
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

    async def post_pc(self, manga_raw: MangaRaw, chat_id) -> Dict:
        """
                Creates manga page
                :param manga_raw:
                :return: telegraph url
                """
        tagged_pics = [f'<img src={x.pic_url}>' for x in manga_raw.pics_raw]
        # print(tagged_pics)
        # comment code below to post raw non-telegraph pics
        # ---------------------------------------------------------------------------------------------------------------
        # '''
        num = 0
        for x in manga_raw.pics_raw:
            filename = str(chat_id) + "--" + str(num) + ".jpg"
            p = requests.get(x.pic_url)
            print("chat_id = ", chat_id)
            print(filename)
            out = open(filename, "wb")
            out.write(p.content)
            out.close()
            # ---------------------------------------
            upload_status = 0

            if (x.width / x.height <= 20):
                if (x.height / x.width <= 20):
                    while (upload_status == 0):
                        if (upload_status == 0):
                            try:
                                sgs = telegraph_file_upload(filename)
                                upload_status = 1
                                print(filename + ": uploaded successfully!")
                            except:
                                upload_status = 0

                                print(filename + ": error uploading pic!")

            path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), filename)
            os.remove(path)
            sgs = '<img src="' + sgs + '">'
            # print(sgs)
            tagged_pics[num] = sgs
            num += 1
            # str_all = str_all + sgs + "\n"
            # ---------------------------------------------------------------------------------------------------------------
        # '''
        html = '\n'.join(tagged_pics)

        page = await self.create_page(
            title=manga_raw.name,
            html_content=html,
            author_name=self.author,
            author_url=self.author_url,
        )
        return page