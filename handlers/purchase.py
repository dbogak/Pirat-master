from datetime import datetime, timedelta

import buttons as btn

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.utils.markdown import hcode
from config import ADMINS, CHAT_ID, WALLET_USDT, ME, TRAF_PHOTO
#from crypto.my_usdt import transactions
from img import photos as img
from loader import bot, dp, set_uname
from loguru import logger
from messages import messages as msg



async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("Не флуди :)")


@dp.callback_query_handler(text_contains="instument")
async def subscrible(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer_photo(TRAF_PHOTO, "Выберите инструмент, нажав соответствующую кнопку", reply_markup=btn.instruments())


@dp.callback_query_handler(text_contains='checker')
async def subscrible(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer(msg.proxy_checker, reply_markup=btn.home())
    await state.set_state("get_proxy")

@dp.message_handler(state="get_proxy", content_types=['any'])
async def photo(message: types.Message):
    if message.content_type =='text':
        resault = await check_one_proxy(message.text)
        if resault["status"]:
            await message.answer(msg.resault_answetr(resault, message.text), reply_markup=btn.home())
        else:
            await message.answer(f"{message.text} - не работает", reply_markup=btn.home())
    elif message.content_type == 'document':
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        resault = await check_many_proxy(file_path)




@dp.callback_query_handler(text_contains="btc")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    data = call.data.split(":")
    amount_usd = int(data[1])
    amount_days = int(data[2])
    user_id = call.from_user.id

    amount_btc = float('{:.2f}'.format(amount_usd + await tobase.get_com()))

    caption = f'🏵 Оплатите <code>{amount_btc}</code> <b>usdt</b> по адресу \n' + hcode(WALLET_USDT) +\
        '\n<b>Необходимо перевести точную сумму 💵, сгенерированную ботом. До цента - не выше, не ниже. Иначе оплата не пройдет!!!</b>\n Выберите сеть <b>Tron (TRC20)</b>\n'\
        f'<i>Вы оплачиваете 📝 подписку на {amount_days} дней</i>'


    await call.message.answer(caption, reply_markup=btn.ipay(amount_btc))
    await tobase.insert_payment(user_id, amount_btc, amount_days)
    await state.set_state("btc")
    await state.update_data(amount_btc=amount_btc, amount_days=amount_days)


@dp.callback_query_handler(text_contains="ipay", state="btc")
async def i_will_pay(call: types.CallbackQuery, state: FSMContext):
    """ ===== Проверяем оплату и сохраняем результат ===== """
    await call.answer("Проверяйте раз в 30 секунд", cache_time=20)

    uname = await set_uname(call.from_user)
    user_id = call.from_user.id
    data = await state.get_data()
    amount_btc = int(data.get("amount_btc")*1000000)
    subscrible_days = data.get("amount_days")

    trans = transactions(WALLET_USDT)
    if trans["success"]:
        data = trans["data"]
    else:
        await call.message.answer("Паламался, напиши админу!!!")
        return

    for tr in data:
        print(f'{tr["value"]} = {amount_btc}')
        if int(tr["value"]) == amount_btc:
            await success_payment(user_id, subscrible_days, uname, state)
            return

    await call.message.answer("Транзакция не найдена!")


async def success_payment(user_id, subscrible_days, uname, state):
    date = datetime.today()
    subscr_date = date + timedelta(days=int(subscrible_days))
    await tobase.update_subscription(user_id, subscr_date)
    expire_date = datetime.now() + timedelta(days=subscrible_days)


    await bot.send_message(ADMIN_ID, f"{uname} Оплатил подписку на {subscrible_days} дней")
    await bot.send_message(ME, f"{uname} Оплатил подписку на {subscrible_days} дней")
    await state.reset_state()

    expire_date = datetime.now() + timedelta(days=subscrible_days)
    channels = tobase.get_channels()
    channels_buttons = []
    for ch in channels:
        try:
            link = await bot.create_chat_invite_link(ch["chat_id"], expire_date.timestamp(), member_limit=1, creates_join_request=False)
            invite_link = link.invite_link
            button = InlineKeyboardButton(ch["title"], url=invite_link)
            channels_buttons.append(button)
        except Exception as err:
            logger.debug(err)
    await bot.send_photo(user_id,
                         photo="AgACAgIAAxkBAALiJmNF6lYwajXumaSh49uhkHq2Hy2OAAL0vzEbsvMxSsSeiM_C_2LnAQADAgADeAADKgQ",
                         caption=f"Оплата прошла успешно!\nВы подписаны до <b>{subscr_date.strftime('%Y-%m-%d')}</b>",
                         reply_markup=btn.invite_links(channels_buttons))


@dp.message_handler(content_types=["video"])
async def photo(message: types.Message):
    await message.answer(f'<b>Файл:</b> {message.video.file_name}\n<b>ID в чате:</b>\n {message.video.file_id}')


@dp.message_handler(content_types=["sticker", "photo"])
async def photo(message: types.Message):
    await message.answer(message.photo[2].file_id)
