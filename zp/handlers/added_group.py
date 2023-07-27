import time
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from zp.create_bot import bot, dp
from zp.keyboards import conf_settings, other_kb, mk_confirm
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from zp.data_base import (inserting_data_db, sql_delete_group, sql_delete_student, read_sql,
                          sql_added_student, read_sql_get_rowid, read_sql_fk)


class FSMAddedGroup(StatesGroup):
    name_group = State()
    save_group = State()
    end = State()


async def start_fsm(msg: types.Message):
    # if msg.from_user.id == 5295520075:
    await FSMAddedGroup.name_group.set()
    await msg.answer("Введите название группы", reply_markup=other_kb.cancel_mk)
    await FSMAddedGroup.next()


async def name_group_save(msg: types.Message, state: FSMContext):
    # if msg.from_user.id == 5295520075:
    await state.update_data(name_group=msg.text)  # сохраняем в озу
    await bot.send_message(msg.chat.id, "Подтвердите", reply_markup=mk_confirm)
    await FSMAddedGroup.next()


async def save_group_end(msg: types.Message, state: FSMContext):
    # if msg.from_user.id == 5295520075:
    if msg.text == 'Подтвердить':
        data = await state.get_data()  # достаем из озу
        await inserting_data_db(data)
        await bot.send_message(msg.chat.id, "Сохранено", reply_markup=other_kb.start_kb)
        await state.finish()


def register_handlers_groups_added(dp: Dispatcher):
    dp.register_message_handler(start_fsm, lambda message: message.text == "Добавить группу 👥", state=None)
    dp.register_message_handler(name_group_save, state=FSMAddedGroup.save_group)
    dp.register_message_handler(save_group_end, state=FSMAddedGroup.end)
