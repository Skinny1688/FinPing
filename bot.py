import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from supabase import create_client, Client

# Configuration from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "8689350743:AAHSPDuul6V7FiLZcXhh5vwNfjllUEyjLNU")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://razpvgsbqsimitgaqaka.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhenB2Z3NicXNpbWl0Z2FxYWthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE1MzMzMzMsImV4cCI6MjA5NzEwOTMzM30.rveiPQfMCVFq49m1g2Mn6p-6vku2g4rZ4VKmA9RxWgk")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Bot and Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# States
class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_functionality = State()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "Привет! Я бот ФинПинг — твой финансовый пульс в Telegram.\n\n"
        "Мы скоро запускаемся! Оставь свои данные, чтобы мы могли пригласить тебя первым.\n\n"
        "Как тебя зовут и какой у тебя бизнес?"
    )
    await state.set_state(Registration.waiting_for_name)

@dp.message(Registration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        "Очень приятно! Расскажи, какой функционал для тебя наиболее важен? "
        "(Например: автозагрузка из банка, прогноз кассового разрыва, ежедневные сводки в ТГ)"
    )
    await state.set_state(Registration.waiting_for_functionality)

@dp.message(Registration.waiting_for_functionality)
async def process_functionality(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['name']
    functionality = message.text
    username = message.from_user.username
    user_id = message.from_user.id

    # Save to Supabase
    try:
        data = {
            "user_id": user_id,
            "username": username,
            "business_info": name,
            "needed_functionality": functionality
        }
        supabase.table("leads").insert(data).execute()

        await message.answer(
            "Спасибо! Я сохранил твои пожелания.\n\n"
            "Сервис ФинПинг сейчас находится в разработке. "
            "Мы обязательно уведомим тебя здесь, как только всё будет готово к запуску! 🚀"
        )
    except Exception as e:
        logging.error(f"Error saving to Supabase: {e}")
        await message.answer(
            "Произошла ошибка при сохранении данных, но мы зафиксировали твой интерес! "
            "Мы уведомим тебя о запуске. 🚀"
        )

    await state.clear()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is not set!")
        exit(1)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
