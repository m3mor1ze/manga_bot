from aiogram import Bot, Dispatcher
from aiogram.types import Message
import configs_.config
from utils_.supervisor import Supervisor
import configs_.config
import re

bot = Bot(token=configs_.config.TELEGRAM_TOKEN())
dp = Dispatcher(bot)
supervisor = Supervisor()

@dp.message_handler(commands=['start'])
async def start(msg: Message):
    await msg.answer('Привет!')
'''
@dp.message_handler(custom_filters=['text'])
async def handler(msg: Message):
    #if msg.text == ''
    if re.findall('https?://(?:[-\w.])|(?:%[\da-fA-F]{2}))+',msg.text)
'''
'''
@dp.message_handler(content_types = ['text'])
async def ans(msg: Message):
    await msg.answer('text')
'''
@dp.message_handler(content_types = ['text'])
async def text(msg: Message):

    #await msg.answer('VERS')

    await msg.answer('Принял, жди')
    links_set = msg.text
    msg2 = msg
    f_set = []
    f_set = links_set.split("\n")
    
    #print(f_set)
    for i in range(len(links_set)):
        msg2.text = f_set[i]
        manga_tg_url = await supervisor.get_manga(msg2)
        await msg.reply(manga_tg_url)