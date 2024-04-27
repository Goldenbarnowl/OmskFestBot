from aiogram import Bot
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import logging
import os
from supabase import Client, create_client

# Загрузка переменных среды.
load_dotenv()

# Логгирование действий бота
logging.basicConfig(level=logging.INFO)

# Инициализация бота, диспетчера и хранилищаа состояний
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализация подключения к базе данных Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Создание клиента Supabase
supabase: Client = create_client(url, key)

channel_username = os.environ.get("CHANNEL_USERNAME")