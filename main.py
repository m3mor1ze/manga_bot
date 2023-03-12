import requests
from aiogram import Bot, Dispatcher
from aiogram.bot import bot
from aiogram.utils import json, executor
from selenium import webdriver
from selenium.webdriver.common.by import By
from telegraph import Telegraph
from PIL import Image
import array
import validators
import os

from validators import url

Tkn = open("tokens.txt")    #gets tokens from file
API_TOKEN = Tkn.readline()
TELEGRAPH_TOKEN = Tkn.readline()
Tkn.close()

API_TOKEN = API_TOKEN[:-1]  #cuts space
TELEGRAPH_TOKEN = TELEGRAPH_TOKEN[:-1]  #cuts space

bot = Bot(token=API_TOKEN)  #bot init
dp = Dispatcher(bot)
telegraph = Telegraph(access_token=TELEGRAPH_TOKEN) #author init

def delete_from_queue():
    file = open("queue.txt", "r")
    array = []
    for line in file:
        array.append(line.strip())
    file.close()
    str = ""
    arrl = array.__len__()
    for i in range(arrl - 2):
        str = str + array[i] + "\n"
    file = open("queue.txt", "w")
    file.write(str)
    #print(array)
    return

def queue_num():
    file = open('queue.txt', 'r')
    num = 0
    while file.readline():
        num += 1

    return num

def telegraph_file_upload(path_to_file):    #uploads image on telegram server
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

def link_processing(site, chat_id):
    driver = webdriver.Firefox()
    driver.get(site)
    btn = driver.find_element(By.CSS_SELECTOR, 'button.nextButton.btn.btn-outline-primary.long')
    i = 0
    pg = driver.find_element(By.CLASS_NAME, 'pages-count')
    tmp = driver.find_element(By.CLASS_NAME, 'mobile-title')
    manga_name = tmp.text
    tmp = driver.find_element(By.CLASS_NAME, 'text-cut')
    part_name = tmp.text
    str_all = ''
    strNum = int(pg.text)

    while i != strNum:
        filename = chat_id + "--" + str(i) + ".jpg"
        img_addr = driver.find_element(By.CSS_SELECTOR, 'img#mangaPicture')
        iii = img_addr.get_attribute('src')
        p = requests.get(iii)
        out = open(filename, "wb")
        out.write(p.content)
        out.close()
        btn.click()
        i = i + 1

        upload_status = 0
        tmp_img = Image.open(filename)
        (width, height) = tmp_img.size
        if (width / height <= 20):
            if (height / width <= 20):
                while (upload_status == 0):
                    if (upload_status == 0):
                        try:
                            sgs = telegraph_file_upload(filename)
                            upload_status = 1
                            print(filename + ": uploaded successfully!")
                        except:
                            upload_status = 0
                            print(filename + ": error uploading pic!")

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
        os.remove(path)
        sgs = '<img src="' + sgs + '">'
        str_all = str_all + sgs + "\n"

    str_all = str_all + "Thanks for watching\n"

    response = telegraph.create_page(
        title=manga_name + " " + part_name,
        html_content=str_all,
        author_name="Михал Палыч Терентьев",
        return_content=False
    )

    link_to = 'https://telegra.ph/{}'.format(response['path'])
    #bot.send_message(chat_id, link_to)
    print(link_to)

    driver.close()

    return link_to

@dp.message_handler(content_types=['text']) #if bot gets text message
async def start(message):

    #queue to proceed
    chat_id = message.from_user.id
    #print("[", chat_id, "]==>", message.text)
    q = open('queue.txt', 'a')  #overwriting chat id
    q.write(str(chat_id) + '\n' + message.text + '\n')  #and link from user
    q.close()   #file closed

    num = queue_num()
    msg = 'Ваш номер в очереди: ' + str(int(num/2) - 1) + ', ожидайте!'
    await bot.send_message(chat_id, msg)
    print(msg)
    q = open('queue.txt', 'r')  #read and proceed
    while True:
        st = q.readline()
        st = st[:-1]
        chat_id = st    #gets chat_id

        st = q.readline()
        st = st[:-1]
        site = st   #gets site link


        if site != "":    #if not void
            if url(site):
                lnk = link_processing(site, chat_id)  #processing link
                delete_from_queue()
                await bot.send_message(chat_id, lnk)

        if not site:  #if void - break
            break
    q.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)