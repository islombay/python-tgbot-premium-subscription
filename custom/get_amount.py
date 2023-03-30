from loader import db


async def get_amount(provider, currency, coins_amount):
    pricing = (await db.get_pricing_for_provider(provider))[currency]
    return pricing[coins_amount]
