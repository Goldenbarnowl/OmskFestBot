from aiogram.dispatcher.filters.state import State, StatesGroup

class User(StatesGroup):
    agree = State()
    agree_wait = State()
    wait_name = State()

class Admin(StatesGroup):
    menu = State()
    wait_winner_count = State()
    winner_publish = State()