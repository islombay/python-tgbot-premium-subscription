from aiogram.dispatcher.filters.state import State, StatesGroup


class Navigation(StatesGroup):
    menu = State()
    settings = State()
    balance = State()
    premium = State()
