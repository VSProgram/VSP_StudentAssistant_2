import asyncio #им      x   портыxч ч   питона
import os

from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher,F, types #импорты фреймворка
from dotenv import find_dotenv, load_dotenv

from handlers.user_private import user_private_router #остальные импорты
from handlers.admin_private.admin_private import admin_router
from handlers.admin_private.admin_private_lectures import admin_router_2
from handlers.admin_private.admin_private_practice import admin_router_3
from handlers.admin_private.admin_private_record import admin_router_4
from handlers.admin_private.admin_private_other_notes import admin_router_5
load_dotenv(find_dotenv()) #загрузить переменную окружения(найти переменну.)
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher() #отлавливает обновления

bot.my_admins_list = [5540384350]

dp.include_router(user_private_router)
dp.include_router(admin_router)
dp.include_router(admin_router_2)
dp.include_router(admin_router_3)
dp.include_router(admin_router_4)
dp.include_router(admin_router_5)





async def main():
    await bot.delete_webhook(drop_pending_updates=True) #сбрасывает ожидающие обновленя
    await dp.start_polling(bot,allowed_updates=['message, edited_updates, callback_query'])

asyncio.run(main())