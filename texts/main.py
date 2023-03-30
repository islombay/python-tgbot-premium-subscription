from aiogram import types
from loader import db
import datetime as dt


lang = {
    "uz": {
        "start_message": "Assalamu Alaykum",
        "settings_message": "<b>⚙Sozlamalar</b>",
        "change_language": "🚩Tilni tanlang",
        "language_changed": "Til o'zgartilindi",
        "buy_coins_call": "To'lov usulini tanlang",
        "how_many_coins": "Qancha tanga sotib olmoqchisiz?",

        "invoice_title": "Tangalar uchun to'lov",
        "invoice_description": "Tangalar sotib olish uchun pastdagi tugmani bosib, karta raqamingizni kiriting va to'lovni amalga oshiring.\n\n" + \
                               "Barcha pul o'tqazmalar xavfsiz. Telegram tomonlama amalga oshiriladi",
        "invoice_prices_labaled_price_label": "Tangalar",
        "expire_date": "Tugash sanasi:",
        "not_enough_funds": "Tangalar yetarli emas",
        "already_a_premium": "Siz premium foydalanuvchisiz.",
        "thanks_for_payment": "Ushbu botdan foydalanyotganingiz uchun rahmat.\nShu tangalar orqali 💎 Premium sotib olishingiz mumkin"
    },
    "ru": {
        "start_message": "Здравствуйте",
        "settings_message": "<b>⚙Настройки</b>",
        "change_language": "🚩Выберите язык",
        "language_changed": "Язык изменен",
        "buy_coins_call": "Выберите метод оплаты",
        "how_many_coins": "Сколько монет вы хотите купить?",
        "invoice_title": "Оплата за монеты",
        "invoice_description": "Чтобы купить монет нажмите на кнопку ниже, введиты данные карты и совершите оплату\n\n" + \
                               "Все транзакции безопасны. Они осуществляются с помощью телеграм",
        "invoice_prices_labaled_price_label": "Монеты",
        "expire_date": "Истечение:",
        "not_enough_funds": "Монет не достаточно",
        "already_a_premium": "Вы являетесь Premium ползователем",
        "thanks_for_payment": "Спасибо что пользуетесь этим ботом.\nТеперь вы можете купить 💎 Premium используя эти монеты"
    },
    "en": {
        "start_message": "Welcome",
        "settings_message": "<b>⚙Settings</b>",
        "change_language": "🚩Choose the language",
        "language_changed": "The language has been changed",
        "buy_coins_call": "Choose payment method",
        "how_many_coins": "How many coins would you like to purchase?",
        "invoice_title": "Payment for coins",
        "invoice_description": "To buy coins press on the button below, enter you credir card information and make a payment\n\n" + \
                               "All transactions are safe. They are made by Telegram.",
        "invoice_prices_labaled_price_label": "Coins",
        "expire_date": "Expire date:",
        "not_enough_funds": "Coins are not enough",
        "already_a_premium": "You are already a premium user",
        "thanks_for_payment": "Thank you for using us.\nNow you can buy 💎 Premium using this coins"
    }
}

lang_formattable = {
    "uz": {
        "premium_message": "📊 Sizning statusingiz: {}\n\n{} tanga evaziga 💎 Premium ga aylaning",
        "balance_message": "🪙 Balans: {} tanga\nTanga sotib olishni unutmang"
    },
    "ru": {
        "premium_message": "📊 Ваш статус: {}\n\nПолучите 💎 Premium за {} монет",
        "balance_message": "🪙 Баланс: {} coins\nНе забывайте покупать монеты"
    },
    "en": {
        "premium_message": "📊 Your status: {}\n\nBecome 💎 Premium for {} coins",
        "balance_message": "🪙 Balance: {} coins\nDo not forget to buy coins"
    }
}


async def get_formattable_lang(text, locale, user: types.User):
    respond = lang_formattable[locale][text]
    if text == "premium_message":
        user_status = await db.get_user_status(user.id)
        if user_status == "premium":
            exp = await db.get_expire_date(user.id)
            exp = dt.datetime.strptime(str(exp), "%Y-%m-%d %H:%M:%S.%f")
            exp = exp.strftime("%d/%m/%Y")
            user_status += f"\n{lang[locale]['expire_date']}: {exp}"
        respond = respond.format(
            user_status, await db.get_coins_for_premium()
        )
    elif text == "balance_message":
        respond = respond.format(
            await db.get_user_coins(user.id)
        )

    return respond


async def get_lang(text, formattable: [bool, int] = False):
    user = types.User.get_current()
    user_locale = await db.get_user_locale(user.id)

    if not bool(formattable):
        return lang[user_locale][text]
    return await get_formattable_lang(text, user_locale, user)

