from aiogram import types
from aiogram.types import ReplyKeyboardMarkup as kmarkup,\
    KeyboardButton as btn

from loader import db

tfb = {
    "uz": {
        "balance": "Balans", "premium":"💎Premium",
        "settings": "⚙Sozlamalar", "language": "🚩Til",
        "menu_back": "◀Menyu"
    },
    "ru": {
        "balance": "Баланс", "premium": "💎Premium",
        "settings": "⚙Настройки", "language": "🚩Язык",
        "menu_back": "◀Меню"
    },
    "en": {
        "balance": "Balance", "premium": "💎Premium",
        "settings": "⚙Settings", "language": "🚩Language",
        "menu_back": "◀Menu"
    },
}


markup = {
    "uz": {
        "start_message": kmarkup(resize_keyboard=True).add(
            btn(tfb['uz']['balance']), btn(tfb['uz']['premium'])
        ).add(btn(tfb['uz']['settings'])),

        "settings_message": kmarkup(resize_keyboard=True).add(
            btn(tfb['uz']['language'])
        ).add(btn(tfb['uz']['menu_back']))
    },
    "ru": {
        "start_message": kmarkup(resize_keyboard=True).add(
            btn(tfb['ru']['balance']), btn(tfb['ru']['premium'])
        ).add(btn(tfb['ru']['settings'])),

        "settings_message": kmarkup(resize_keyboard=True).add(
            btn(tfb['ru']['language'])
        ).add(btn(tfb['ru']['menu_back']))
    },
    "en": {
        "start_message": kmarkup(resize_keyboard=True).add(
            btn(tfb['en']['balance']), btn(tfb['en']['premium'])
        ).add(btn(tfb['en']['settings'])),

        "settings_message": kmarkup(resize_keyboard=True).add(
            btn(tfb['en']['language'])
        ).add(btn(tfb['en']['menu_back']))
    }
}


async def get_keyboard(keyboards_text):
    user = types.User.get_current()
    user_locale = await db.get_user_locale(user.id)

    return markup[user_locale][keyboards_text]


def get_array(text):
    return [i[text] for i in tfb.values()]