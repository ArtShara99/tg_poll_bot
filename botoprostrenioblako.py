import os
import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ======== ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ========
# На Railway добавляем их в Settings → Environment Variables
TOKEN = os.environ.get("TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID", "-1000000000000"))
TOPIC_ID = int(os.environ.get("TOPIC_ID", "0"))
# ======================================

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Функция отправки опроса ---
async def send_poll(question):
    await bot.send_poll(
        chat_id=CHAT_ID,
        message_thread_id=TOPIC_ID,
        question=question,
        options=["Да", "Нет"],
        is_anonymous=False
    )
    print(f"[INFO] Опрос отправлен: {question}")

# --- Планировщик ---
scheduler = AsyncIOScheduler()

def schedule_poll(question):
    global loop
    if loop is None:
        print("[ERROR] Event loop не инициализирован")
        return
    asyncio.run_coroutine_threadsafe(send_poll(question), loop)

# --- Основная функция ---
loop = None
async def main():
    global loop
    loop = asyncio.get_running_loop()

    # Расписание опросов
    scheduler.add_job(lambda: schedule_poll("Будешь ли ты на тренировке во вторник в 21:00?"),
                      'cron', day_of_week='mon', hour=18, minute=0)
    scheduler.add_job(lambda: schedule_poll("Будешь ли на тренировке в четверг в 22:00?"),
                      'cron', day_of_week='wed', hour=18, minute=0)
    scheduler.add_job(lambda: schedule_poll("Будешь ли на игре в воскресенье?"),
                      'cron', day_of_week='sat', hour=18, minute=0)

    scheduler.start()
    print("[INFO] Бот запущен ✅")

    # Запуск бота для команд (если нужны)
    await dp.start_polling(bot)

# --- Запуск ---
if __name__ == "__main__":
    asyncio.run(main())
