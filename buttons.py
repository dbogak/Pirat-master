from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.types.reply_keyboard import KeyboardButton

import tobase

""" start_menu = ReplyKeyboardMarkup(True, True)
start_menu.row("Проверить подпискуОплатить подписку")
start_menu.row("📝 Пояснительная записка") """


def start_menu():
    keyboard_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    keyboard_markup.insert(InlineKeyboardButton('🛍 Ассортимент', callback_data='sortament'))
    keyboard_markup.insert(InlineKeyboardButton('⚒ Инструменты', callback_data='instument'))
    keyboard_markup.insert(InlineKeyboardButton('👤 Мой профиль', callback_data='profile'))
    keyboard_markup.insert(InlineKeyboardButton('🔗 Реферальная программа', callback_data='ref_program'))
    keyboard_markup.insert(InlineKeyboardButton('✍️ Обратная связь', callback_data='ref_program'))
    keyboard_markup.insert(InlineKeyboardButton(
        '📕 Инструкции', url="https://telegra.ph/Poyasnitelnaya-zapiska-i-soglashenie-o-riskah-10-06"))
    #keyboard_markup.add(InlineKeyboardButton('📕 Инструкции', callback_data='notes'))
    return keyboard_markup



def instruments():
    keyboard_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    keyboard_markup.insert(InlineKeyboardButton('👌 Прокси чекер', callback_data='checker'))
    keyboard_markup.insert(InlineKeyboardButton('👮‍♂️ Проверка домена', callback_data='domain'))
    keyboard_markup.insert(InlineKeyboardButton('📑 WhitePage генератор', callback_data='wpage'))
    keyboard_markup.insert(InlineKeyboardButton('🏡 Главная', callback_data='cancel'))
    return keyboard_markup


def home():
    keyboard_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(InlineKeyboardButton(
        '🏠 В начало', callback_data='cancel'))
    return keyboard_markup


def ipay(amount):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(
        f'Я оплатил, проверить', callback_data=f"ipay:{amount}"))
    markup.add(InlineKeyboardButton('Отменить 💫', callback_data='cancel'))
    return markup


def pay_btn(amount, link, id_key, promo=".", subscribe_days=30):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(f'Перейти на странтцу оплаты', url=link))
    markup.add(InlineKeyboardButton('👇 - Я оплатил! Проверить',
               callback_data=f'ipay:{amount}:{id_key}:{promo}:{subscribe_days}'))
    return markup

def invite_link(link, title):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(title, url=link))
    return markup


def invite_links(buttons):
    markup = InlineKeyboardMarkup(row_width=2)
    return markup.add(*buttons)


def channels_buttons():
    channels = tobase.get_channels()
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for ch in channels:
        buttons.append(ch['title'])
    buttons = [
        InlineKeyboardButton(f'Testnet/Retrodrop',
                             url='https://t.me/+SXdH_MQxAegwYzMy'),
        InlineKeyboardButton(f'Testnet/Retrodrop chat',
                             url='https://t.me/+cWmkpUs52WYwNTdi'),
        InlineKeyboardButton(
            f'IDO/Fund Chat', url="https://t.me/+vAXlQb7T3Sw2MTIy"),
        InlineKeyboardButton(f'P2E', url='https://t.me/+Dfrtlv6Os-ZmYzc6'),
        InlineKeyboardButton(
            f'P2E Chat', url='https://t.me/+gdvY-i4mbK9hZWMy'),
        InlineKeyboardButton(f'Fund', url='https://t.me/+8HglRYy063JkODky'),
        InlineKeyboardButton(
            f'Fund Chat', url='https://t.me/+X4I4nikmHfBmZjgy'),
        InlineKeyboardButton(f'Ambassador Program',
                             url='https://t.me/+Qt7Qqwb7hFgzOTky'),
        InlineKeyboardButton(f'Полезные инструменты',
                             url='https://t.me/+Pb0jd_VzqqFkNzBi'),
        InlineKeyboardButton(
            f'Nft Chat', url='https://t.me/+ofuljqEViCY4Mzc6'),
        InlineKeyboardButton(f'Nft', url='https://t.me/+BRN_kc6xSfNjMTMy'),
        InlineKeyboardButton(
            f'Nodes Chat', url='https://t.me/+H4PrEM0zL-E2YTEy'),
        InlineKeyboardButton(f'Nodes', url='https://t.me/+PXPqxlLF7RdlNzhi'),
        InlineKeyboardButton(
            f'Trading Chat', url='https://t.me/+8hSK8crRdVliZDE6'),
        InlineKeyboardButton(f'Trading', url='https://t.me/+4CAFjYuBYBxlZTQy')
    ]
    return markup.add(*buttons)
