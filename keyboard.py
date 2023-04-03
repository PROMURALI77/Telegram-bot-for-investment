from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from config import CHANNELS

main_buttons = [
    [
        KeyboardButton(text='👤 Профиль', callback_data='profile'),
    ],
    [
        KeyboardButton(text='💳 Кошелёк', callback_data='currency'),
        KeyboardButton(text='🖥 Инвестиции', callback_data='investments'),
    ],
    [
        KeyboardButton(text='🖨 Калькулятор', callback_data='calc'),
        KeyboardButton(text='🗒 Обучение', callback_data='gide'),
        KeyboardButton(text='Вип статус', callback_data='vipMain'),
    ],
    [
        KeyboardButton(text='👥 Партнерская программа', callback_data='part')
    ]
]
main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=main_buttons)

go_main = [
    [
         KeyboardButton(text='⏪ Главное меню', callback_data='to_main')
    ]
]
gm = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=go_main)


stcheck = [
    [
         KeyboardButton(text='⏪ Главное меню', callback_data='to_main')
    ],
    [
        KeyboardButton(text='🔔 Проверить платёж', callback_data='to_main')
    ]
]
st = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=stcheck)

investment_buttons = [
    [
        KeyboardButton(text='➕ Инвестировать', callback_data='balance'),
        KeyboardButton(text='➖ Собрать', callback_data='to_balance'),
    ],
    [
        KeyboardButton(text='⏪ Главное меню', callback_data='to_main')
    ]
]
investment = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=investment_buttons)

currency_buttons = [
    [
        InlineKeyboardButton(text='➕ Пополнить', callback_data='popol'),
        InlineKeyboardButton(text='➖ Вывести', callback_data='vivod'),
    ],
    [
        InlineKeyboardButton(text='⏪ Главное меню', callback_data='to_main'),
    ]
]
currency = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=currency_buttons)

investment_money_buttons = [
    [
        KeyboardButton(text='📈500', callback_data='balance'),
        KeyboardButton(text='📈1000', callback_data='balance'),
        KeyboardButton(text='📈5000', callback_data='balance'),
    ],
    [
        KeyboardButton(text='📈10000', callback_data='balance'),
        KeyboardButton(text='📈25000', callback_data='balance'),
        KeyboardButton(text='📈50000', callback_data='balance'),
    ],
    [
        KeyboardButton(text='📈100000', callback_data='balance'),
        KeyboardButton(text='📈250000', callback_data='balance'),
        KeyboardButton(text='📈500000', callback_data='balance'),
    ],
    [
        KeyboardButton(text='⏪ Главное меню', callback_data='to_main')
    ]
]
investment_money = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=investment_money_buttons)


investment_to_balance_buttons = [
    [
        KeyboardButton(text='💸500', callback_data='balance'),
        KeyboardButton(text='💸1000', callback_data='balance'),
        KeyboardButton(text='💸5000', callback_data='balance'),
    ],
    [
        KeyboardButton(text='💸10000', callback_data='balance'),
        KeyboardButton(text='💸25000', callback_data='balance'),
        KeyboardButton(text='💸50000', callback_data='balance'),
    ],
    [
        KeyboardButton(text='💸100000', callback_data='balance'),
        KeyboardButton(text='💸250000', callback_data='balance'),
        KeyboardButton(text='💸500000', callback_data='balance'),
    ],
    [
        KeyboardButton(text='⏪ Главное меню', callback_data='to_main')
    ]
]
investment_to_balance = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=investment_to_balance_buttons)


withdraw_buttons = [
    [
        KeyboardButton(text='💳 На карту', callback_data='to_card'),
        KeyboardButton(text='🥝 На QIWI', callback_data='to_qiwi'),
    ],
    [
        KeyboardButton(text='⏪ Главное меню', callback_data='to_main')
    ]
]
withdraw = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=withdraw_buttons)

adm_button = [
    [
        KeyboardButton(text='Выдать баланс', callback_data='setbalance'),
        KeyboardButton(text='Отнять баланс', callback_data = 'deletebal'),
    ],
    [
        KeyboardButton(text='⏪ Главное меню', callback_data='to_main')
    ]
]

admBtn = ReplyKeyboardMarkup(resize_keyboard=False, keyboard=adm_button)

oplata = InlineKeyboardMarkup(row_width=1)

oplataBtnfive = InlineKeyboardButton(text='500 рублей', callback_data='fivehundret')

oplata.insert(oplataBtnfive)

vipBtn = [
    [
        KeyboardButton(text='Купить вип статус', callback_data='vip')
    ],
    [
        KeyboardButton(text='⏪ Главное меню', callback_data='to_main')
    ]
]

vip = ReplyKeyboardMarkup(resize_keyboard=False, keyboard=vipBtn)

def showKanal():
    keyboard = InlineKeyboardMarkup(row_width=1)

    for channel in CHANNELS:
        btn = InlineKeyboardButton(text=channel[0], url=channel[2])
        keyboard.insert(btn)

    btnDoneSub = InlineKeyboardButton(text='Проверить подписку', callback_data='subchanneldone')
    keyboard.insert(btnDoneSub)
    return keyboard