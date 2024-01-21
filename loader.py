import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

async def set_uname(user):
    if 'username' in user and user['username'] and user['username'] != 'null':
        username = f"@{user['username']}"
    else:
        if 'full_name' in user:
            username = f"{user['full_name']}"
        else:
            if 'first_name' in user:
                username = f"{user['first_name']}"
            else:
                username = "безымянный"
    try:        
        username = f"{username}({user['user_id']})"
    except Exception as err:
        username = f"{username}({user['id']})"
        

    return username


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )


class Vars:
    amounts_list: list
    pay_users: dict
