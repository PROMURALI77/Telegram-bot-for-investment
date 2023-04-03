import re

import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType
from aiogram.types import InputFile

from db import Database
import config
import keyboard 

import datetime

from aiogram.contrib.fsm_storage.memory import MemoryStorage


from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from utils import get_investment_text

from datetime import timedelta


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database("database.db")
now = datetime.datetime.now()

class Form(StatesGroup):
    vivod = State()
    menu = State()
    popol = State()
    invest = State()
    calc = State()
    addb = State()
    admPass = State()
    oplata = State()

async def on_startup(_):
    print('bot online')

KASSA = '' #Payment key

async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type != 'private':
        return
    if not db.user_exists(message.from_user.id):
        start_command = message.text 
        referrer_id = str(start_command[7:])
        if str(referrer_id) != "":
            if str(referrer_id) != str(message.from_user.id):
                db.add_user(message.from_user.id, referrer_id)
                try:
                    await bot.send_message(referrer_id, "По вашей ссылке зарегестрировался новый пользователь!")
                except:
                    pass
            else:
                await bot.send_message(message.from_user.id, "Вы зарегестрировались по ссылке!")
        else:
            db.add_user(message.from_user.id)
        if await check_sub_channels(config.CHANNELS, message.from_user.id):
            await bot.send_message(message.from_user.id, f"| Добро пожаловать на EXODUS |, выбирайте кнопку из меню", reply_markup=keyboard.main)
        else:
            await bot.delete_message(message.from_user.id)
            await bot.send_message(message.from_user.id, config.NOT_SUB_MESSAGE, reply_markup=keyboard.showKanal())

@dp.callback_query_handler(text='subchanneldone')
async def subchanneldone(message : types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if await check_sub_channels(config.CHANNELS, message.from_user.id):
        await bot.send_message(message.from_user.id, f"| Добро пожаловать на EXODUS |, выбирайте кнопку из меню", reply_markup=keyboard.main)
    else:
            await bot.send_message(message.from_user.id, config.NOT_SUB_MESSAGE, reply_markup=keyboard.showKanal())

#Стата Юзера

@dp.message_handler(Text("👤 Профиль"))
async def profile(message: types.Message, state: FSMContext):
    if db.check_vip(message.from_user.id):
         await bot.send_message(message.from_user.id,text=f"🤖 Ваш ID: {message.from_user.id}\n🌟 Статус: Вип пользователь\n💳 Ваш Баланс: {db.user_balance(message.from_user.id)}₽\n👥 Партнёров: {db.count_reeferals(message.from_user.id)} чел.", reply_markup=keyboard.main)
    else:
        await bot.send_message(message.from_user.id,text=f"🤖 Ваш ID: {message.from_user.id}\n💳 Ваш Баланс: {db.user_balance(message.from_user.id)}₽\n👥 Партнёров: {db.count_reeferals(message.from_user.id)} чел.", reply_markup=keyboard.main)
  
@dp.message_handler(Text("🗒 Обучение"))
async def profile(message: types.Message):
    await bot.send_message(message.from_user.id,text=f"🗒 Перейдя по данной ссылке, Вы сможете ознакомиться с информацией о работе с нашем сервисом.\n\n----", reply_markup=keyboard.main)

#Калькулятор инвестиций

@dp.message_handler(Text("🖨 Калькулятор"))
async def profiler(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id,text=f"💱 Введите вложения для рассчёта Вашей прибыли.", reply_markup=keyboard.gm)
    await state.set_state(Form.calc)


@dp.message_handler(state=Form.calc)
async def profile(message: types.Message, state: FSMContext):
    money = message.text
    if money.isdigit():
        if round(int(money)) < 50001:
            day = round((int(money) / 100) * 3.2)
            month = round((int(money) / 100) * 3.2 * 30)
            year = round((int(money) / 100) * 3.2 * 365)
            await state.finish()
            await bot.send_message(message.from_user.id,text=f"💱 В данном разделе вы сумеете рассчитать вашу прибыль, от суммы вашей инвестиции в наш проект:\n\n💵 Ваша инвестиция: {money}₽\n\n◼️ Прибыль в сутки: {day}₽\n◼️ Прибыль в месяц: {month}₽\n◼️ Прибыль в год: {year}₽", reply_markup=keyboard.main)
        else:
            await bot.send_message(message.from_user.id,text=f"⛔ Вы превысили максимальную сумму инвестиции в 50.000₽", reply_markup=keyboard.gm)
    else:
        if message.text == "⏪ Главное меню":
            await state.finish()
            await bot.send_message(message.from_user.id,text=f"⏪ Вы вернулись в главное меню.", reply_markup=keyboard.main)
        else:
            await bot.send_message(message.from_user.id,text=f"⛔ Вы ввели некорректное значение.", reply_markup=keyboard.gm)

#Финансовая статистика юзера

@dp.message_handler(Text("💳 Кошелёк"))
async def balance(message: types.Message):
    await bot.send_message(message.from_user.id, f"🤖 Ваш ID: {message.from_user.id}\n💳 Ваш Баланс: {db.user_balance(message.from_user.id)}₽\n\n🔔 Ниже вы можете провести манипуляции с своим кошельком", reply_markup=keyboard.currency)

@dp.message_handler(Text("➕ Пополнить"))
async def balancer(message: types.Message, state=FSMContext):
    await bot.send_message(message.from_user.id, text=f"Выбирайте кнопку с суммой", reply_markup=keyboard.oplata)

#Пополнение баланса

@dp.callback_query_handler(text='fivehundret')
async def payfivehant(call : types.CallbackQuery):
    await bot.send_invoice(chat_id=call.from_user.id, title='Пополение баланса', description="100", payload="fivehundret", provider_token=KASSA, currency='RUB', start_parameter= "balance", prices=[{"label": "Руб", "amount": 50000}])

@dp.pre_checkout_query_handler()
async def oplataaa(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def oplataqweqwe(message: types.Message):
    if message.successful_payment.invoice_payload == 'fivehundret':
        await bot.send_message(message.from_user.id, f"Оплата прошла успешно!")
        db.set_balance(message.from_user.id, balance =+ 500)

#Заявка на вывод

@dp.message_handler(Text("➖ Вывести"))
async def lol(message: types.Message, state: FSMContext):
    await state.set_state(Form.vivod)
    await bot.send_message(message.from_user.id, text=f"◼️ Введите сумму, которую хотите вывести со своего баланса.", reply_markup=keyboard.gm)


@dp.message_handler(state=Form.vivod)
async def get_addrebar(message: types.Message, state: FSMContext):
    user_balance = db.user_balance(message.from_user.id)
    if message.text.isdigit(): 
        if int(message.text) < 100:
             await bot.send_message(message.from_user.id,text=f"⛔ Минимальная сумма для вывода - 100 рублей.", reply_markup=keyboard.gm)
        else:
            if user_balance < int(message.text):
                await bot.send_message(message.from_user.id,text=f"⛔ На вашем счету недостаточно средств", reply_markup=keyboard.gm)
                return
            if db.check_vip(message.from_user.id):
                await bot.send_message(message.from_user.id, f"Заявка на вывод была создана её номер: {random.randint(1,1000)}, этот номер отправьте агенту поддержки: @exudusp")
                await state.finish()
            else:
                await bot.send_message(message.from_user.id,text=f"⛔ Для вывода средств обратитесь в агенту поддержки: @exudusp", reply_markup=keyboard.main)
                await state.finish()
                
    else: 
        if message.text == "⏪ Главное меню":
            await bot.send_message(message.from_user.id,text=f"⏪ Вы вернулись в главное меню.", reply_markup=keyboard.main)
            await state.finish()
        if message.text != "⏪ Главное меню":
            await bot.send_message(message.from_user.id,text=f"⛔ Вы ввели некорректное значение.", reply_markup=keyboard.gm)


#Инвестеции

@dp.message_handler(Text("➕ Инвестировать"))
async def balance(message: types.Message, state: FSMContext):
    await state.set_state(Form.invest)
    await bot.send_message(message.from_user.id, text=f"◼️ Введите сумму, которую хотите инвестировать.", reply_markup=keyboard.gm)

#Ссылка на парнёрку

@dp.message_handler(Text("👥 Партнерская программа"))
async def balfdsnce(message: types.Message):
    await bot.send_message(message.from_user.id, text=f"В данном сегменте EXODUS мы поднимем тему заработка без вложений.\n\n👥 На данный момент действует партнерская программа 'EXODUS FRIENDS' - приведи друзей, или же просто рекламируй наш проект на различных платформах и получай 10% от депозита партнеров на счет для вывода!\n\nПосле того, как твой партнер перейдет по твоей ссылке или пополнит инвестиционный счет тебе придет уведомление.\n\nДля того, что бы партнера засчитало, нужно что бы он перешел по твоей партнерской ссылке - https://t.me/{config.BOT_NICKNAME}?start={message.from_user.id}", reply_markup=keyboard.main)

@dp.message_handler(state=Form.invest)
async def get_addrefdsfds(message: types.Message, state: FSMContext):
    user_balance = db.user_balance(message.from_user.id)
    if message.text.isdigit(): 
        if int(message.text) < 100:
             await bot.send_message(message.from_user.id,text=f"⛔ Минимальная сумма для инвестиции - 100 рублей.", reply_markup=keyboard.gm)
        else:
            if user_balance < int(message.text):
                await bot.send_message(message.from_user.id,text=f"⛔ На вашем счету недостаточно средств", reply_markup=keyboard.gm)
                return

            await state.finish()
            await bot.send_message(message.from_user.id,text=f"✅ Вы успешно инвестировали {int(message.text)} рублей", reply_markup=keyboard.main)
            db.add_invest(message.from_user.id, int(message.text))
            db.set_balance(message.from_user.id, int(message.text))
    else: 
        if message.text == "⏪ Главное меню":
            await bot.send_message(message.from_user.id,text=f"⏪ Вы вернулись в главное меню.", reply_markup=keyboard.main)
            await state.finish()
        if message.text != "⏪ Главное меню":
            await bot.send_message(message.from_user.id,text=f"⛔ Вы ввели некорректное значение.", reply_markup=keyboard.gm)

#Вывод на баланс инвестиции

@dp.message_handler(Text("➖ Собрать"))
async def balance(message: types.Message):
    all_cash, investment_text = get_investment_text(db.user_invests(message.from_user.id))
    money = db.all_invests(message.from_user.id)
    user_balance = db.user_balance(message.from_user.id)

    if money > 0:
        await bot.send_message(message.from_user.id, text=f"✅ Вы успешно получили на счёт {money + all_cash}₽", reply_markup=keyboard.investment)
    else:
        return await bot.send_message(message.from_user.id, text=f"⛔ На вашем инвестиционном счету недостаточно средств", reply_markup=keyboard.investment)

    db.set_balance(message.from_user.id, money+all_cash)
    db.dell_invests(message.from_id)

#Стата инвестиций(Юзера)

@dp.message_handler(Text("🖥 Инвестиции"))
async def investments(message: types.Message):
    all_cash, investment_text = get_investment_text(db.user_invests(message.from_user.id))
    cash = round(all_cash)
    money = round(db.all_invests(message.from_user.id))
    if money == 'NULL':
        money = 0
    await bot.send_message(message.from_user.id, f"Открывайте свой вклад ниже, а после получайте прибыль с него и собирайте её в данном разделе: \n\n🖨 Процент от вклада: 3.2%\n⏱ Время доходности: 24 часa\n📅 Срок вклада: Пожизненно\n\n💳 Ваш вклад: {money}₽\n💵 Накопление: {cash}₽\n\n⏱ Время до сбора средств: 0:00:00", reply_markup=keyboard.investment)


@dp.message_handler(Text("🏦 Перевести на баланс"))
async def to_balance(message: types.Message):
    all_cash, investment_text = get_investment_text(db.user_invests(message.from_user.id))
    await message.reply(f"Ваш доход с инвестиций: {all_cash} руб.\n\n", reply_markup=keyboard.investment_to_balance)


@dp.message_handler(regexp=r"^💸\d+$")
async def invest_sum(message: types.Message):
    cash = int(re.findall(r"(\d+)", message.text)[0])
    investment_sum, invest_text = get_investment_text(db.user_invests(message.from_user.id))

    if cash > investment_sum:
        return await message.reply(f"Вы ещё не заработали эту сумму. Доступно для перевода: {investment_sum} руб.")
    
    db.add_invest(message.from_user.id, "-" + cash)

    await message.reply(f"Вы перевели {cash} руб. на основной баланс."
                        f"На вашем инвестиционном балансе осталось: {investment_sum - cash}")


@dp.message_handler(Text("📈 Инвестировать"))
async def invest(message: types.Message):
    await message.reply("💵 Выберите сумму", reply_markup=keyboard.investment_money)


@dp.message_handler(regexp=r"^📈\d+$")
async def invest_sum(message: types.Message):
    cash = int(re.findall(r"(\d+)", message.text)[0])
    user_balance = db.user_balance(message.from_user.id)

    if cash > user_balance:
        return await message.reply(f"На балансе недостаточно денег. Пополните баланс на {cash - user_balance} руб.")
    
    db.set_balance(message.from_user.id, user_balance=user_balance-cash)
    db.add_invest(message.from_user.id, cash)

    await message.reply(f"Вы инвестировали {cash} руб. На вашем балансе осталось: {user_balance - cash}")


@dp.message_handler(Text("💸 Вывод"))
async def withdraw(message: types.Message):
    await message.reply("💸 Вывод средств", reply_markup=keyboard.withdraw)


@dp.message_handler(Text("⏪ Главное меню"))
async def to_main(message: types.Message, state: FSMContext):
   await bot.send_message(message.from_user.id,text=f"⏪ Вы успешно вернулись в главное меню.", reply_markup=keyboard.main)
   await state.finish()
        
#Админские команды        

@dp.message_handler(commands="addbalance")
async def addbalance(message: types.Message):
    if db.check_adm(message.from_user.id):
        args = message.text.split()
        db.set_balance(args[1], args[2]) # user id, money
        await bot.send_message(message.from_user.id, text=f"✅ Вы успешно пополнили баланс.\nUID » {args[1]}\nПополнение » {args[2]}", reply_markup=keyboard.gm)
    else:
        await bot.send_message(message.from_user.id, f"Доступно только администратору.")

@dp.message_handler(commands='awaybalance')
async def awaybalance(message : types.Message):
    if db.check_adm(message.from_user.id):
        args = message.text.split()
        db.awaybalance(args[1], args[2])
        await bot.send_message(message.from_user.id, text=f"✅ Вы успешно отняли баланс.\nUID » {args[1]}\n Забрали » {args[2]}", reply_markup=keyboard.gm)
    else:
        await bot.send_message(message.from_user.id, f"Доступно только администратору.")

@dp.message_handler(commands="setbalance")
async def balancefdr(message: types.Message):
    if db.check_adm(message.from_user.id):
        args = message.text.split()
        db.set_balance(args[1], args[2])
        await bot.send_message(message.from_user.id, text=f"✅ Вы успешно установили новое значение баланса.\nUID » {args[1]}\nБаланс » {args[2]}", reply_markup=keyboard.gm)
    else:
        await bot.send_message(message.from_user.id, f"Доступно только администратору.")

@dp.message_handler(commands=['stats'])
async def stats(message : types.Message):
    if db.check_adm(message.from_user.id):
        args = message.text.split()
        db.user_balance(args[1])
        await bot.send_message(message.from_user.id, f"Баланс: {db.user_balance(args[1])} Руб.")
    else:
        await bot.send_message(message.from_user.id, f"Доступно только администратору.")

#запаролена инструкция к админке

@dp.message_handler(commands=['adm'])
async def admstart(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Введите пароль к админке.')
    await state.set_state(Form.admPass)

@dp.message_handler(state = Form.admPass)
async def password(message: types.Message, state: FSMContext):
    if message.text.isdigit(): 
        if int(message.text) == 2121:
                if db.check_adm(message.from_user.id):
                    await bot.send_message(message.from_user.id,text=f"Авторизованы, как администратор\n\n Чтобы посмотреть баланс пользователя пропишите /stats ID (/stats 4358734)\n\nЧтобы выдать баланс исполдьзуйте: /setbalance ID пользователя и кол-во денег(/setbalance 656545654 12000000).\n\n Чтобы выдать баланс пользователю(с рефералом) используйте /addbalance ID usera кол-во денег. \n\n Чтобы забрать деньги у пользователя введите /awaybalance ID Кол-во денег.\n\n\n ВНИМАНИЕ \n\n\n ПЕРЕД ТЕМ, КАК СПИСАТЬ ДЕНЬГИ У ПОЛЬЗОВАТЕЛЯ ПОСМОТРИТЕ БАЛАНС, ДАБЫ НЕ СОЗДАТЬ ПРОБЛЕМ! \n\n Все команды используем строго по форме. И вне этого справочника. ", reply_markup=keyboard.gm)
                else:
                    await bot.send_message(message.from_user.id, f"Доступно только администратору. Это справочник, уведомите руководителя.")
                    await state.finish()
    else: 
        if message.text== "⏪ Главное меню":
            await state.finish()
            await bot.send_message(message.from_user.id,text=f"⏪ Вы вернулись в главное меню.", reply_markup=keyboard.main)

@dp.message_handler(Text('Вип статус'))
async def vipMain(message: types.Message):
    await bot.send_message(message.from_user.id, f"🤩 Вип статус включает в себя:\n🕶 Уникальный префикс\n💰 Вывод быстрее обычного времени\n👫 Вип-чат\n\n💸 Цена 500 руб.", reply_markup=keyboard.vip)

@dp.message_handler(Text('Купить вип статус'))
async def buyvip(message: types.Message):
    priceVip = 500
    if priceVip > db.user_balance(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Недостаточно средств на балансе.', reply_markup=keyboard.main)
    elif db.check_vip(message.from_user.id) == 1:
        await bot.send_message(message.from_user.id, "У вас уже есть вип-статус")
    else:
        await bot.send_message(message.from_user.id, f"Вам выдана випка на аккаунт, спасибо.")
        db.awaybalance(message.from_user.id, 500)
        db.vip(message.from_user.id, +1)
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
