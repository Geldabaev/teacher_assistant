from aiogram.dispatcher.filters import Text
from zp.keyboards import conf_settings, other_kb
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from zp.create_bot import bot


async def start(msg: types.Message):
    await bot.send_message(msg.chat.id, "Чем могу помочь? 🔥", reply_markup=other_kb.start_kb)


async def settings(msg: types.Message):
    await bot.send_message(msg.chat.id, "что именно хотите? 💁‍♂️", reply_markup=conf_settings.markup_add_del)


# Выход из состояний где бы не находились
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.chat.id, 'Главное меню', reply_markup=other_kb.start_kb)


async def cancel_no_fsm(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Главное меню', reply_markup=other_kb.start_kb)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(cancel_handler, state="*", commands='Отмена')
    dp.register_message_handler(cancel_no_fsm, text='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(settings, text="Настроить 🛠")
