from aiogram import Bot, Dispatcher
from aiogram.types import Message
import configs_.config
from utils_.supervisor import Supervisor
import configs_.config

bot = Bot(token=configs_.config.TELEGRAM_TOKEN())
dp = Dispatcher(bot)
supervisor = Supervisor()

@dp.message_handler(commands=['start'])
async def start(msg: Message):
    await msg.answer('Привет!')


@dp.message_handler(content_types=['text'])
async def text(msg: Message):
    await msg.answer('Принял, жди')
    manga_tg_url = await supervisor.get_manga(msg)
    await msg.reply(manga_tg_url)
