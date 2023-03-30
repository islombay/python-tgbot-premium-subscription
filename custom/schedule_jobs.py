from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import db
import datetime

scheduler = AsyncIOScheduler()


def schedule_jobs():
    scheduler.add_job(chekc_expire_date, "interval", days=5)
    scheduler.start()


async def chekc_expire_date():
    users = await db.get_users()
    for user in users:
        status = user.status
        if status == "premium":
            exp = (user.expire_date).timestamp()
            now = datetime.datetime.now().timestamp()

            difference = now - exp
            if difference > 0:
                await db.get_premium_back(user.user_id)
