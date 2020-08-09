import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, executor
from config import TOKEN, CHATS_ID, DELAY
from yummyanime_parser import YummyAnime

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Задаем уровень логов
logging.basicConfig(level=logging.INFO)

# Инициализируем парсер
parser = YummyAnime()


# Функция для отправки фото с описанием
async def send_news(img_name, title, info, link, chat_id):
    with open(f"img\\{img_name}", 'rb') as photo:
        await bot.send_photo(chat_id=chat_id,
                             photo=photo,
                             caption=f"""{title} - {info}\n\n{link}""")


# Функция для мониторинга новых новостей с указаной задержкой и отправки их в указаные чаты
async def scheduled(wait_for, chats_id):
    while True:
        all_news = parser.get_news()
        news = parser.check_news(all_news)

        for chat_id in chats_id:
            if isinstance(news, str):
                await bot.send_message(chat_id=chat_id, text=news)

            elif isinstance(news, dict):
                await send_news(img_name=news['img_name'], title=news['title'], info=news['info'], link=news['link'],
                                chat_id=chat_id)

            else:
                for new in news:
                    await send_news(img_name=new['img_name'], title=new['title'], info=new['info'], link=new['link'],
                                    chat_id=chat_id)

        images = os.listdir('img')

        for img in images:
            os.remove(os.path.join('img', img))

        await asyncio.sleep(wait_for)


if __name__ == '__main__':
    dp.loop.create_task(scheduled(DELAY, CHATS_ID))
    executor.start_polling(dispatcher=dp)
