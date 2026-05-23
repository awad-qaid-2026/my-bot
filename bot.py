import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

# ضع الـ Token الجديد هنا بعد استخراجه من BotFather
API_TOKEN = 'YOUR_NEW_TOKEN_HERE'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("مرحباً! أنا بوت أرقام وهمية. \nملاحظة: الخدمة تتطلب ربط API مدفوع.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
