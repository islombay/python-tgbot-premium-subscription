from loader import dp, db

from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from texts import get_lang as _
from buttons import *
from states import Navigation


@dp.message_handler(commands='start', state="*")
async def start_func(msg: Message, state: FSMContext):
    await db.add_user(msg.from_user.id)
    await msg.answer(await _("start_message"),
                     reply_markup=(await get_keyboard("start_message")))

    await Navigation.menu.set()


# Settings button
@dp.message_handler(Text(get_array("settings")), state=Navigation.menu)
async def settings_func(msg: Message, state: FSMContext):
    await msg.answer(await _("settings_message"),
                     reply_markup=(await get_keyboard("settings_message")))

    await Navigation.settings.set()
    await state.update_data(last_action="menu")


@dp.message_handler(Text(get_array("language")), state=Navigation.settings)
async def change_language(msg: Message):
    await msg.answer(await _("change_language"),
                     reply_markup=(await get_inline_keyboard("change_language_message")))
# -------------------------------------------------------------


# Premium button
@dp.message_handler(Text(get_array("premium")), state=Navigation.menu)
async def premium_func(msg: Message, state: FSMContext):
    markup = None if (await db.is_premium_user(msg.from_user.id)) else await get_inline_keyboard("buy_premium")
    await msg.answer(await _("premium_message", 1), reply_markup=markup)
# -------------------------------------------------------------


# Balance button
@dp.message_handler(Text(get_array("balance")), state=Navigation.menu)
async def balance_func(msg: Message, state: FSMContext):
    await msg.answer(await _("balance_message", 1), reply_markup=(await get_inline_keyboard("buy_coins")))


# -------------------------------------------------------------

# Payment message
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state="*")
async def successful_payment_done(msg: Message, state: FSMContext):
    data = await state.get_data()
    await db.add_check_id(msg.from_user.id, data['pre_checkout_id'], data['coins_amount'])

    from_dev_information = {"coins_amount": data['coins_amount'], "provider": data['provider']}
    await db.add_successful_payment(msg.successful_payment, data['pre_checkout_id'], from_dev_information)
    await db.add_coins(msg.from_user.id, data['coins_amount'])
    await msg.answer(await _("thanks_for_payment"))


# Back Button everywhere
@dp.message_handler(Text(get_array("menu_back")), state=[Navigation.settings, Navigation.balance])
async def back_func(msg: Message, state: FSMContext):
    last_action = (await state.get_data())['last_action']
    if last_action == "menu":
        await start_func(msg, state)