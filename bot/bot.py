from aiogram import Bot, Dispatcher
from aiogram.types import Message
from utils.supervisor import Supervisor
import configs.config

bot = Bot(token=configs.config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)
supervisor = Supervisor()

@dp.message_handler(commands=['start'])
async def start(msg: Message):
    await msg.answer('zdarova')


@dp.message_handler(content_types=['text'])
async def text(msg: Message):
    await msg.answer(f'prinyal zapros: {msg}')
    manga_tg_url = await supervisor.get_manga(msg)
    await msg.reply(manga_tg_url)
