""" Для работы Базы данных скачать ее и установить все по дефолту
Ссылка на скачивание https://drive.google.com/file/d/1kvmRCtW4ogS0Hx41Ol_fZKImo08yzquf/view?usp=sharing """

import calendar
from handlers.commands import subscribe
import ssl
from datetime import datetime, timedelta

import pymongo
from config import MONGO_URL


client = pymongo.MongoClient(MONGO_URL)

Users = client['FRIGATE']['Users']

async def die(user_id): Users.find_one_and_delete({'user_id': user_id})


async def new_user(user):
    """ ==== База пользователей ==== """
    existed_user = Users.find_one({'user_id': user.id})
    if not existed_user:
        new_user = {
            "user_id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "group": 0,
            "kiked": True,
            "subscribtion": datetime.now(),
            "date": datetime.today().strftime("%d-%m-%y %H:%M")
        }
        Users.insert_one(new_user, session=None)
        return new_user


async def find_user(user_id: int): return Users.find_one(
    {'user_id': user_id}, {'_id': 0})


def find_usr(user_id): return Users.find_one({'user_id': user_id}, {'_id': 0})


def show_users(): return list(Users.find({}, {'_id': 0}))

users = show_users()
for user in users:
    Users.update_one({"user_id": user["user_id"]}, {"$set":{"kicked": False}})


async def show_kicked_users(): return list(Users.find({"kicked": True}, {'_id': 0}))


async def update_subscription(user_id, date):
    Users.update_one({"user_id": user_id},
                     {'$set': {"subscribtion": date, "kicked": True, "group": 1}})


async def auto_update_subscription(user_id):
    today = datetime.today()
    days = calendar.monthrange(today.year, today.month)[1]
    next_month_date = today + timedelta(days=days)
    Users.update_one({"user_id": user_id}, {
                     '$set': {"subscribtion": next_month_date}})


def find_subscribe(user_id):
    try:
        subscr = Users.find_one({"user_id": user_id})["subscribtion"]
    except:
        subscr = datetime.today()
    return subscr


async def are_subscribe(user_id):
    now = datetime.now()
    time_subscribe = find_subscribe(user_id)

    deadline = time_subscribe
    if now > deadline:

        return False, time_subscribe
    elif now.day == deadline.day and now.month == deadline.month and now.year == deadline.year:

        return True, time_subscribe
    else:
        period = deadline - now
        print(f"Осталось {period.days} дней")
        return True, time_subscribe


async def del_dead_user(user_id): Users.find_one_and_delete(
    {"user_id": user_id})