import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Настройка логов и бота
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_data = {}

# Обработка старта
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer("Привет, ты попал на регистрацию РП проекта Oblivion RP\n\nНапиши своё ФИО (РП):")
    user_data[message.from_user.id] = {}

# Шаги анкеты
@dp.message_handler(lambda message: message.from_user.id in user_data and 'fio' not in user_data[message.from_user.id])
async def get_fio(message: types.Message):
    user_data[message.from_user.id]['fio'] = message.text
    await message.answer("Сколько тебе лет (реальный возраст)?")

@dp.message_handler(lambda message: message.from_user.id in user_data and 'age' not in user_data[message.from_user.id])
async def get_age(message: types.Message):
    user_data[message.from_user.id]['age'] = message.text
    await message.answer("Что такое Metagaming?")

@dp.message_handler(lambda message: message.from_user.id in user_data and 'mg' not in user_data[message.from_user.id])
async def get_mg(message: types.Message):
    user_data[message.from_user.id]['mg'] = message.text
    await message.answer("На каких РП проектах ты еще играл(а)?")

@dp.message_handler(lambda message: message.from_user.id in user_data and 'rp_history' not in user_data[message.from_user.id])
async def get_rp_history(message: types.Message):
    user_data[message.from_user.id]['rp_history'] = message.text
    data = user_data[message.from_user.id]

    # Формируем анкету и отправляем админу
    summary = f"📨 Новая анкета:\n\n" \
              f"👤 ФИО (РП): {data['fio']}\n" \
              f"🎂 Возраст: {data['age']}\n" \
              f"📘 Metagaming: {data['mg']}\n" \
              f"🕹️ РП-опыт: {data['rp_history']}"
    
    await bot.send_message(ADMIN_ID, summary)
    await message.answer("✅ Спасибо! Твоя анкета отправлена на рассмотрение.", reply_markup=ReplyKeyboardRemove())
    user_data.pop(message.from_user.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

