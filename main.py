from aiogram import executor, Bot, Dispatcher
from loader import dev_admin

from custom import schedule_jobs


async def startup_function(dp):
    await dp.bot.send_message(dev_admin, "Bot started")


async def shutdown_function(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await dp.bot.close()

if __name__ == "__main__":
    from handlers import dp

    schedule_jobs()

    executor.start_polling(dp, on_startup=startup_function, on_shutdown=shutdown_function)