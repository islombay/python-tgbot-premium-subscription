from aiogram import types
from aiogram.types import InlineKeyboardMarkup as kmarkup,\
    InlineKeyboardButton as btn

from loader import db

tfb = {
    "uz": {
    },
    "ru": {
    },
    "en": {
    },
}

# INLINE
markup = {
    "uz": {
        "change_language_message": kmarkup().add(btn("🇺🇿O'zbek", callback_data="lang_uz"))
            .add(btn("🇷🇺Русский", callback_data="lang_ru"))
            .add(btn("🏴󠁧󠁢󠁥󠁮󠁧󠁿English", callback_data="lang_en")),

        "buy_premium": kmarkup().add(
            btn("💎 Premium sotib olish", callback_data="buy_premium")
        ),

        "buy_coins": kmarkup().add(
            btn("Tanga sotib olish", callback_data="buy_coins")
        )
    },
    "ru": {
        "change_language_message": kmarkup().add(btn("🇺🇿O'zbek", callback_data="lang_uz"))
            .add(btn("🇷🇺Русский", callback_data="lang_ru"))
            .add(btn("🏴󠁧󠁢󠁥󠁮󠁧󠁿English", callback_data="lang_en")),

        "buy_premium": kmarkup().add(
            btn("Купить 💎 Premium", callback_data="buy_premium")
        ),

        "buy_coins": kmarkup().add(
            btn("Купить монеты", callback_data="buy_coins")
        )
    },
    "en": {
        "change_language_message": kmarkup().add(btn("🇺🇿O'zbek", callback_data="lang_uz"))
            .add(btn("🇷🇺Русский", callback_data="lang_ru"))
            .add(btn("🏴󠁧󠁢󠁥󠁮󠁧󠁿English", callback_data="lang_en")),

        "buy_premium": kmarkup().add(
            btn("Buy 💎 Premium", callback_data="buy_premium")
        ),

        "buy_coins": kmarkup().add(
            btn("Buy Coins", callback_data="buy_coins")
        )
    }
}

markup_f = {
    "uz": {

    },
    "ru": {

    },
    "en": {

    }
}


async def format_price(value, currency):
    if currency == "uzs" or currency == "rub":
        index = 0
        new_value = ""
        # 1 000 000,00
        isComma = True
        for e in str(value)[::-1]:
            # print(new_value, index, e)
            index += 1
            new_value += e
            if index == 2 and isComma:
                new_value += ','
                isComma = False
                index = 0

            if index == 3 and not isComma:
                new_value += " "
                index = 0
            # print(new_value, index, e)

        return new_value[::-1]
    return value


async def get_inline_keyboard_formattable(txt, user, locale):
    if txt == "payment_methods":
        methods_list = await db.get_payment_methods()
        k = kmarkup()
        for method in methods_list:
            k.add(btn(method['title'], callback_data=f"pvia_{method['name']}"))

        return k

    elif "pay_via_" in txt:
        provider = txt.replace("pay_via_","")
        pricing = await db.get_pricing_for_provider(provider)
        currency_names = {"uzs": "so'm", "usd": "dollars", "rub": "рубль"}
        k = kmarkup()
        for currency in pricing:
            for key, value in pricing[currency].items():
                k.add(btn(f"{key} = {await format_price(value, currency)} {currency_names[currency]}", callback_data=f"bcoins_{key}_{currency}"))

        return k


async def get_inline_keyboard(keyboards_text, is_format: [bool, int] =False):
    user = types.User.get_current()
    user_locale = await db.get_user_locale(user.id)

    if not is_format:
        return markup[user_locale][keyboards_text]
    return await get_inline_keyboard_formattable(keyboards_text, user, user_locale)