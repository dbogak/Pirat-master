def start_message(name):
    return f""" Привет <b>{name}</b>!\n\n👋🏻 Приветствуем вас в самом лучшем интернет-магазине прокси серверов!

👇 Для навигации по боту используйте клавиатуру ниже!

👨🏻‍🦰 Aдминистратор бота @cashriser"""

ex_note="https://telegra.ph/Poyasnitelnaya-zapiska-i-soglashenie-o-riskah-10-06"


def ref_programm(link, reffers): return f""" 
🔗 Реферальная програма

Вы получаете 10% от покупок людей, которые придут в наш бот по вашей специальной ссылке!

⚠️ Ваша ссылка для заработка:
{link}

Вы пригласили: 0 чел. """

proxy_checker = "Пришлите проксик в таком виде:\n<b>IP:PORT:USERNAME:PASSWORD</b> или <b>IP:PORT</b>\nТак же можно прислать тхт файл с толпой проксей, по одному в каждой строчке"

def resault_answetr(r, proxy):
    
    answer = f""" 
{proxy}

Тип прокси: {r['type']}
Время ответа: {r['time_response']}
Анонимность: {r['anonymity']}
Страна: {r['country']} """ 
    return answer