from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import google.generativeai as genai
import asyncio
import os

TOKEN = os.getenv("TOKEN", "")
GEMINI_KEY = os.getenv("GEMINI_KEY", "")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("Сәлем! Мен 24/7 істеп тұрмын! 🔥\nСұрағыңды жаза бер!")

@dp.message(F.text)
async def ai_chat(m: types.Message):
    if m.text.startswith("/"):
        return
    await bot.send_chat_action(m.chat.id, "typing")
    try:
        prompt = f"Сен қазақша сөйлейтін көңілді жігітсің. Қысқа, брат деп сөйле. Сұрақ: {m.text}"
        res = model.generate_content(prompt)
        await m.answer(res.text)
    except Exception as e:
        await m.answer(f"Қате: {e}")

async def main():
    print("Бот іске қосылды!")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
