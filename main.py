import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
import sys
from os import getenv
from typing import Any, Dict
import bot
import sqlite3
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, block INTEGER);""")
conn.commit()


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6571705606:AAH94j0JwRKGu0YeXkeXur4L6jGgNB7_wDo", parse_mode='html')
# Диспетчер
dp = Dispatcher()


@dp.message( F.text == "📦 Товары")
async def cmd_random(message: types.Message):
    def get_keyboard():
        buttons = [
            [
                types.InlineKeyboardButton(text="⭐ Портфолио", url="https://t.me/erick_des"),
                types.InlineKeyboardButton(text="🔶 Сделать заказ", callback_data="make_order"),

            ],
            [types.InlineKeyboardButton(text="🛡 Техническая поддержка(offline)", callback_data="support")]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    await message.answer(
        "⭐ Выбери то, что тебя интересует и нажми на кнопку ниже.",
        reply_markup=get_keyboard()
    )

@dp.message( F.text == "📱 Профиль")
async def cmd_random(message: types.Message):

    await message.answer(
        "⭐├ Пока в разработке :)")

@dp.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery):
    def get_keyboard():
        buttons = [
            [
                types.InlineKeyboardButton(text="⭐ Портфолио", url="https://t.me/erick_des"),
                types.InlineKeyboardButton(text="🔶 Сделать заказ", callback_data="make_order"),

            ],
            [types.InlineKeyboardButton(text="🛡 Техническая поддержка(offline)", callback_data="support")]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    await callback.message.edit_text(
        "⭐ Выбери то, что тебя интересует и нажми на кнопку ниже.",
        reply_markup=get_keyboard()
    )
@dp.message(Command("start"))
async def cmd_random(message: types.Message):

    def get_keyboard():
        buttons = [
            [
                types.KeyboardButton(text="📱 Профиль"),
                types.KeyboardButton(text="📦 Товары")

            ],
            [types.KeyboardButton(text="🔰 F.A.Q")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True,)
        return keyboard

    await message.answer(
        "⭐ Приветствую, дорогой друг! Этот бот - мой обитель. Здесь ты можешь найти всю интересующую тебя информацию. Для навигации по боты воспользуйся кнопками ниже.",
        reply_markup=get_keyboard()
    )


@dp.callback_query(F.data == "make_order")
async def send_random_value(callback: types.CallbackQuery):
    def get_keyboard():
        buttons = [

            [types.InlineKeyboardButton(text="🌄 Оформление", callback_data="design")],

            [types.InlineKeyboardButton(text="🖥 Монтаж видероликов", callback_data="design")],

            [types.InlineKeyboardButton(text="🎆 Анимация", callback_data="design")],

            [types.InlineKeyboardButton(text="⚙ 3D оформление", callback_data="design")],

            [types.InlineKeyboardButton(text="💼 UI/UX макетирование", callback_data="design")],
            [types.InlineKeyboardButton(text="Вернутся назад", callback_data="back")],

        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    await  callback.message.edit_text('<b>Выберите из списка интересующий товар. Если их несколько - напишите об этом в тз</b>',
                                  reply_markup=get_keyboard())


@dp.callback_query(F.data == "design")
async def send_random_value(callback: types.CallbackQuery):
    def get_keyboard():
        buttons = [

            [types.InlineKeyboardButton(text="Заполнить техническое задание", callback_data="descr_order")],

        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    await  callback.message.edit_text(
        '♻ При заполнении технического задания, старайтесь максимально подробно описать ваши пожелания к дизайну/оформлению.'
        '\n\n<b>❗ Нажимая кнопку ниже, вы автоматически соглашаетесь с правилами студии.</b>',
        reply_markup=get_keyboard())


class iio(StatesGroup):
    descr = State()


@dp.callback_query(F.data == "descr_order")
async def get_order_descr(callback: types.CallbackQuery, state: FSMContext) -> None:
    def get_keyboard():
        buttons = [

            [types.InlineKeyboardButton(text="Отменить", callback_data="descr_order_cancel")],

        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    await state.set_state(iio.descr)
    await  callback.message.edit_text(
        'Напишите и отправьте техническое задание, оно автоматически будет отправлено на обработку менеджеру. Как только Ваш'
        ' заказ будет принят в обработку, Вам придёт оповощение с дальнейшими указаниями и контактами для связи.',
        reply_markup=get_keyboard())

@dp.callback_query(F.data == "descr_order_cancel")
async def get_order_descr(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    def get_keyboard():
        buttons = [

            [types.InlineKeyboardButton(text="🌄 Оформление", callback_data="design")],

            [types.InlineKeyboardButton(text="🖥 Монтаж видероликов", callback_data="design")],

            [types.InlineKeyboardButton(text="🎆 Анимация", callback_data="design")],

            [types.InlineKeyboardButton(text="⚙ 3D оформление", callback_data="design")],

            [types.InlineKeyboardButton(text="💼 UI/UX макетирование", callback_data="design")],
            [types.InlineKeyboardButton(text="Вернутся назад", callback_data="back")],

        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    await  callback.message.edit_text('<b>Вы отменили заказ\n\nВыберите из списка интересующий товар. Если их несколько - напишите об этом в тз</b>',
                                  reply_markup=get_keyboard())

@dp.message(iio.descr)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(descr=message.text)
    await state.clear()

    def get_keyboard():
        buttons = [
            [types.InlineKeyboardButton(text="Обработать", callback_data="allow_order")],
            [types.InlineKeyboardButton(text="Отказ", callback_data="cancel_new_ord")],


        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await message.reply(f"<b>Ожидайте, Ваш заказ успешно оформлен и ожидает подтверждения</b>")

    await bot.send_message(-4118194438,f"{message.text},\n\n@{message.from_user.username} ")
    await bot.send_message(-4118194438,
                           f"{message.from_user.id}",
                           reply_markup=get_keyboard())

@dp.callback_query(F.data == "cancel_new_ord")
async def allow_order_descr(callback: types.CallbackQuery,):
    await callback.message.answer(
        '<b>❌ Дизайнер отклонил Ваш заказ. Это могло произойти по ряду следующих причин:\n\n1.Вы неправильно составили ТЗ\n2.Возможно, мы еще не можем выполнить такой заказ\n3.Дизайнер неактивен</b>')
    await bot.send_message(callback.message.text, '<b>❌ Дизайнер отклонил Ваш заказ. Это могло произойти по ряду следующих причин:\n\n1.Вы неправильно составили ТЗ\n2.Возможно, мы еще не можем выполнить такой заказ\n3.Дизайнер неактивен</b>')


@dp.callback_query(F.data == "allow_order")
async def allow_order_descr(callback: types.CallbackQuery,):
    await callback.message.answer(
        '<b>✅ Ваш заказ принят в обработку, ожидайте пока с Вами свяжется дизайнер</b>')
    await bot.send_message(callback.message.text, '<b>✅ Ваш заказ принят в обработку, ожидайте пока с Вами свяжется дизайнер</b>')
    


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
