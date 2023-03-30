from .models import User, Settings

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dateutil.relativedelta import relativedelta


# MongoDB
class Mongodb:
    def __init__(self, dbName, host=None, port=None):
        self.host = host if host else "localhost"
        self.port = port if port else 27017
        self.dbName = dbName

        self.client = AsyncIOMotorClient(host, port)

        self.db = self.client[self.dbName]
        self.users = self.db.users
        self.settings = self.db.settings
        self.payment_methods = self.db.payment_methods
        self.pre_checkout = self.db.pre_checkouts
        self.successful_payments = self.db.successful_payments

    async def _get_user(self, user_id):
        document = await self.users.find_one({"user_id": user_id})
        if document:
            return User(document)
        return document

    async def _user_exists(self, user_id):
        result = await self._get_user(user_id)
        return bool(result)

    async def add_user(self, user_id, locale="en", status="user", expire_date=None, check_id=None):
        _user_exists = await self._user_exists(user_id)
        if not _user_exists:
            document = {
                "user_id": int(user_id),
                "locale": locale,
                "status": status,
                "expire_date": expire_date if expire_date else datetime.now(),
                "check_id": [],
                "coins": 0
            }
            result = await self.users.insert_one(document)
            return bool(result.inserted_id)
        return False

    async def get_user(self, user_id):
        document = await self.users.find_one({"user_id": user_id})
        if document:
            return User(document)
        return document

    async def get_users(self):
        docs_list = []
        async for doc in self.users.find():
            docs_list.append(User(doc))

        return docs_list

    async def get_user_locale(self, user_id):
        _exist = await self._user_exists(user_id)
        if _exist:
            user = await self.get_user(user_id)
            return user.locale
        else:
            await self.add_user(user_id)
            await self.get_user_locale(user_id)
        raise Exception

    async def change_user_locale(self, user_id, locale):
        _exist = await self._user_exists(user_id)
        if _exist:
            _user_locale = await self.get_user_locale(user_id)
            if _user_locale != locale:
                await self.users.update_one({"user_id": user_id}, {"$set": {"locale": locale}})
                
    async def get_user_status(self, user_id):
        _exist = await self._user_exists(user_id)
        if _exist:
            user = await self.get_user(user_id)
            return user.status
        return None

    async def is_premium_user(self, user_id):
        cstatus = await self.get_user_status(user_id)
        if cstatus:
            return cstatus == "premium"
        return None

    async def get_user_coins(self, user_id):
        user = await self.get_user(user_id)
        if user:
            return user.coins
        return None

    async def get_coins_for_premium(self):
        result = Settings(await self.settings.find_one({"coins_for_premium": {"$gt": 0}}))
        return result.coins_for_premium

    async def get_payment_methods(self):
        documents = self.payment_methods.find()
        all = await documents.to_list(length=50)
        return all

    async def get_payment_method_currency(self, name):
        document = await self.payment_methods.find_one({"name": name})
        return document.currencies

    async def get_pricing_for_provider(self, provider):
        coins_cost = await self.payment_methods.find_one({"name":provider})
        pricing = coins_cost['cost']
        return pricing

    async def get_provider_token(self, provider_name, test=False):
        document = await self.payment_methods.find_one({"name": provider_name})
        if test:
            return document['token_test']
        return document['token_live']

    async def add_precheckout(self, tg_msg):
        new_msg = tg_msg
        new_msg['date_of_query'] = (datetime.now()).isoformat()
        await self.pre_checkout.insert_one(dict(new_msg))

    async def add_coins(self, user_id, amount):
        user = await self.get_user(user_id)
        await self.users.update_one({"user_id": user_id}, {"$set": {"coins": (int(user.coins) + int(amount))}})

    async def add_check_id(self, user_id, pre_checkout_id, coins_amount):
        user = await self.get_user(user_id)
        now = (datetime.now()).isoformat()

        new_list = user.check_id
        new_list.append({"pre_check_id": pre_checkout_id,
                         "date_of_add": now,
                         "coins_amount": coins_amount})

        await self.users.update_one({"user_id": user_id}, {"$set": {"check_id": new_list}})

    async def add_successful_payment(self, tg_msg, query_id, from_dev):
        new_msg = tg_msg
        new_msg['pre_checkout_id'] = query_id
        new_msg['date_of_it'] = (datetime.now()).isoformat()
        new_msg['from_dev'] = from_dev
        await self.successful_payments.insert_one(dict(new_msg))

    async def buy_premium_for_coins(self, user_id):
        user = await self.get_user(user_id)
        coins_amount = user.coins
        needed = await self.get_coins_for_premium()
        expire_date = datetime.now() + relativedelta(months=1)
        await self.users.update_one({"user_id": user_id}, {"$set": {
            "coins": int(coins_amount) - int(needed),
            "status": "premium",
            "expire_date": expire_date}})

    async def get_expire_date(self, user_id):
        user = await self.get_user(user_id)
        if user:
            return user.expire_date

    async def get_premium_back(self, user_id):
        user = await self.get_user(user_id)
        if user:
            await self.users.update_one({"user_id": user_id},
                                        {"$set": {
                                            "status": "user"
                                        }})


async def main():

    db_mongo = Mongodb(dbName="test_db")
    await db_mongo.add_check_id(10, "34322353")

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())