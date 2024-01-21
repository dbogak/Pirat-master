import asyncio
from datetime import datetime, timedelta
from aiogram.dispatcher import filters

import buttons as btn
import pandas as pd
import tobase
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton
from config import ADMIN_CHANNEL, ADMINS, CHAT_ID, MAIN_PHOTO
from loader import bot, dp, set_uname
from loguru import logger
from messages import messages as msg
from .purchase import success_payment


@dp.message_handler(Command("start"))
@dp.message_handler(Command("start"), state="*")
async def start(message: types.Message):
    new_user = await tobase.new_user(message.from_user)
    if new_user:
        text = await set_uname(message.from_user)
        for admin in ADMINS.split(","):
            try:
                await bot.send_message(admin, text=text)
            except:
                pass
    await message.answer_photo(MAIN_PHOTO,
     msg.start_message(message.from_user.full_name), reply_markup=btn.start_menu())


@dp.callback_query_handler(text_contains="cancel", state="*")
async def cancell(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.reset_state()
    await call.message.answer_photo(MAIN_PHOTO,
     msg.start_message(call.from_user.full_name), reply_markup=btn.start_menu())


@dp.message_handler(Command("links"))
async def links(message: types.Message):
    await message.answer(message)
    bot_name = await bot.get_me(CHAT_ID)
    link_answer = f'https://t.me/{bot_name["username"]}/?start=amway\nhttps://t.me/{bot_name["username"]}'
    await message.answer(link_answer)   


@dp.message_handler(Command("id"))
async def test(message: types.Message, state: FSMContext):
    """ ===== Проверка получателей автосписания ===== """
    await message.answer(message.from_user.id)



@dp.message_handler(Command("usid"))
async def fuckem(message: types.Message, state: FSMContext):
    if int(message.from_user.id) != int(ADMIN_ID):
        await message.answer("Команда администратора!!!")
        return
    await message.answer("Введите id для отправки кнопок пользователю")
    #await state.update_data(user_id=message.text)
    await state.set_state("usms")


@dp.message_handler(state="usms")
async def fuckem(message: types.Message, state: FSMContext):
    user = await tobase.find_user(int(message.text))
    if user:
        await message.answer("Отправил")
    data = await state.get_data()
    await state.reset_state()
    uname = await set_uname(user)
    await success_payment(int(message.text), 100, uname, state)



@dp.message_handler(Command("send"))
async def send(message: types.message.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Это команда администратора")
        return
    await message.answer("Выбери целевую аудиторию рассылки", reply_markup=btn.admin_send())


@dp.message_handler(Command("users"))
async def uusers(message: types.message.Message):
    if int(message.from_user.id) != int(ADMIN_ID):
        await message.answer("Команда администратора!!!")
        return
    ankets = tobase.show_users()
    df = pd.DataFrame(ankets)
    df.to_excel('users.xlsx')
    with open('users.xlsx', 'rb') as file:
        await message.answer_document(file)


@dp.callback_query_handler(text_contains="CG", state="wait_msg_ghg")
async def giveme_message(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введи сообщение для промоакции")
    group = int(call.data.split(":")[1])
    await state.update_data(group=group)
    await state.set_state("send_msg_ghg")


@dp.callback_query_handler(text_contains="CG")
async def giveme_message(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введи сообщение для рассылки")
    group = int(call.data.split(":")[1])
    await state.update_data(group=group)
    await state.set_state("wait_msg")


@dp.message_handler(state="wait_msg")
async def send(message: types.message.Message, state: FSMContext):
    """ ===== Ждем сообщение и смотрим какой группе разослать ===== """
    text = message.text

    count = 0
    data = await state.get_data()
    group = int(data['group'])
    if group == 0:
        users = await tobase.show_users()
    else:
        users = await tobase.find_group_users(group)
    total = len(users)
    await state.reset_state()

    """ Test
    await message.answer(f"Получателей {total}, {group=} Сообщение\n{text}")
    return
    end test """

    for user in users:
        try:
            await bot.send_message(chat_id=user['user_id'],
                                   text=text)
            await asyncio.sleep(0.5)
            logger.info(f'{count}:{user}')
            count += 1
        except Exception as err:
            logger.error(err)
            with open('die_mather_fucker.txt', 'a') as file:
                file.write(str(user['user_id'])+'\n')
        if count % 100 == 0:
            await asyncio.sleep(60)
            await message.answer_photo(photo='https://avatars.mds.yandex.net/get-zen_doc/2480061/pub_5f91ba80b28cf0518478aed6_5f91c453b28cf051848972f9/scale_1200',
                                       caption=f"Пользователей: {total}, пока отправленно {count} сообщений \nРекламное паузо!!!")
    await message.answer(f"Пользователей: {total}, отправленно {count} сообщений")


@dp.message_handler(Command("count"))
async def send(message: types.message.Message):
    count = len(await tobase.show_users())
    await message.answer(count)


@dp.message_handler(Command("ch"))
async def send(message: types.message.Message):
    try:
        await message.answer(f"<code>{message.chat.title}: {message.chat.id}</code>")
    except: pass


@dp.message_handler(Command("subscribe"))
async def subscribe(message: types.Message):
    user_id = message.from_user.id
    date = tobase.find_subscribe(user_id)

    if not date or type(date) == bool:
        await message.answer("У Вас нет подписки")
    await message.answer(f"Ваша подписка действительна до {date.strftime('%Y-%m-%d')}")


@dp.message_handler(commands=["setpromo"])
async def command_set_promo(message: types.Message, state: FSMContext):
    """ ===== Ловим команду setpromo ===== """
    if message.from_user.id not in ADMIN_ID:
        await message.answer("Это команда администратора!")
        return
    promos = await tobase.find_promo()
    await message.answer(f"Список Промокодов\n{promos}")
    await message.answer('Присылайте новый промокод или несколько через "ЗАПЯТУЮ"\nВот так - \n<code>ИМЯПРОМОКОДА:цена_подписки:период_подписки</code>')
    await state.set_state("wait_new_promo")


@dp.message_handler(content_types="text", state="wait_new_promo")
async def wait_number(message: types.Message, state: FSMContext):
    promo_list = message.text.split(',')
    for promo in promo_list:
        try:
            name_promo, amount, subscr = promo.split(":")
            name_promo = name_promo.upper()
            amount = int(amount)
            subscr = int(subscr)
            await tobase.set_promo(name_promo, amount, subscr)
            await message.answer(f"Добавил новый промокод: {name_promo}: {amount}₽, {subscr}дней")
        except Exception as err:
            await message.answer(err)
            await message.answer('Присылайте новый промокод или несколько через "ЗАПЯТУЮ"\nВот так - \n<code>ИМЯПРОМОКОДА:цена_подписки:период_подписки</code>')

    await state.reset_state()


async def menu():

    expire_date = datetime.now() + timedelta(days=100)
    channels = tobase.get_channels()
    channels_buttons = []
    for ch in channels:
        try:
            link = await bot.create_chat_invite_link(ch["chat_id"], expire_date, member_limit=1, creates_join_request=False)
            invite_link = link.invite_link
            button = InlineKeyboardButton(ch["title"], url=invite_link)
            channels_buttons.append(button)
        except Exception as err:
            logger.debug(err)

    #await message.answer(f"Пробные кнопки", reply_markup=btn.invite_links(channels_buttons))


""" @dp.message_handler(Command("add"))
async def add_groups(message: types.Message):
    title = message.chat.full_name
    chat_id = message.chat.id
    chat_type = message.chat.type
    await message.answer(f"<code>{title}:{chat_id}</code>")
    await tobase.update_channels(dict(chat_id=chat_id, title=title, chat_type=chat_type))


@dp.message_handler(filters.ForwardedMessageFilter(True))
async def add_groups(message: types.Message):
    user_id = message.chat.id
    title = message.forward_from_chat.full_name
    chat_id = message.forward_from_chat.id
    chat_type = message.forward_from_chat.type
    await bot.send_message(user_id, f"<code>{title}:{chat_id}</code>")
    await tobase.update_channels(dict(chat_id=chat_id, title=title, chat_type=chat_type)) """