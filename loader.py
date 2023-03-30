import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from dbs import DataBase

load_dotenv()

db = DataBase("test_db")

storage = MongoStorage(host='localhost', port=27017, db_name='db_name')

bot = Bot(os.getenv("BOT_TOKEN"), parse_mode="html")
dp = Dispatcher(bot, storage=storage)

dev_admin = os.getenv("DEV_ADMIN")
