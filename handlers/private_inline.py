from loader import bot, dp, db

from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.dispatcher.storage import FSMContext

from texts import get_lang as _
from buttons import *
from states import Navigation
from custom import get_amount

from .private import start_func, premium_func


@dp.callback_query_handler(text_startswith="lang_", state="*")
async def change_language_call(call: CallbackQuery, state: FSMContext):
    chosen_language = str(call.data).replace("lang_", "")
    await db.change_user_locale(call.from_user.id, chosen_language)

    await call.answer(await _("language_changed"), show_alert=True)
    await start_func(call.message, state)


@dp.callback_query_handler(text="buy_coins", state="*")
async def buy_coins_call(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        await _("buy_coins_call"),
        reply_markup=(await get_inline_keyboard("payment_methods", 1))
    )


@dp.callback_query_handler(text_startswith="pvia_", state='*')
async def choose_amount_of_money_to_buy(call: CallbackQuery, state: FSMContext):
    provider = call.data.replace("pvia_", "")
    await call.message.edit_text(await _("how_many_coins"))
    await call.message.edit_reply_markup(await get_inline_keyboard(f"pay_via_{provider}", 1))

    await state.update_data(provider=provider)


@dp.callback_query_handler(text_startswith="bcoins_", state="*")
async def send_invoice_to_pay(call: CallbackQuery, state: FSMContext):
    dt = (call.data.replace("bcoins_", "")).split("_")
    data = await state.get_data()

    coins_amount = dt[0]
    currency = dt[1]
    total_amount = await get_amount(data['provider'], currency, coins_amount)
    providerToken = await db.get_provider_token(data['provider'], test=True)
    labaled_price = await _("invoice_prices_labaled_price_label")

    await state.update_data(currency=currency, total_amount=total_amount,
                            coins_amount=coins_amount)

    await call.message.delete()
    await bot.send_invoice(call.from_user.id,
                           title=(await _(f"invoice_title")),
                           description=(await _("invoice_description")),
                           payload=call.from_user.id,
                           provider_token=providerToken,
                           currency=currency.upper(),
                           prices=[LabeledPrice(labaled_price, int(total_amount))],
                           start_parameter="start",
                           protect_content=True
    )


@dp.pre_checkout_query_handler(state="*")
async def process_of_pre_checkout_query(query: PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(query.id, ok=True)
    await db.add_precheckout(query)
    await state.update_data(pre_checkout_id=query.id)


@dp.callback_query_handler(text="buy_premium", state="*")
async def buy_premium_for_coins(call: CallbackQuery, state: FSMContext):
    coins_amount = await db.get_user_coins(call.from_user.id)
    coins_for_premium = await db.get_coins_for_premium()
    user_status = await db.get_user_status(call.from_user.id)

    isEnough = (coins_amount - coins_for_premium) >= 0
    if user_status != "premium":
        if isEnough:
            await db.buy_premium_for_coins(call.from_user.id)
            await call.answer("👍🏻", show_alert=True)
            await premium_func(call.message, state)
        else:
            await call.answer(await _("not_enough_funds"), show_alert=True)
    else:
        await call.answer(await _("already_a_premium"), show_alert=True)

