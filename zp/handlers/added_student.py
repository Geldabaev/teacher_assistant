from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from zp.create_bot import bot
from zp.keyboards import other_kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from zp.data_base import (read_sql, sql_added_student)


class FSMAddedStudent(StatesGroup):
    name_student_to_group = State()
    save_student = State()


async def start_fsm_student(msg: types.Message):
    # if msg.from_user.id == 5295520075:
    read = await read_sql('my_groups')
    if read:
        kb_list = []
        for ret in read:
            kb_list.append(KeyboardButton(ret[1]))
        await bot.send_message(msg.from_user.id, "Выберите нужную группу",
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(*kb_list).add(other_kb.cancel_kb))
        await FSMAddedStudent.name_student_to_group.set()

    else:
        await bot.send_message(msg.from_user.id, "У вас нет ни одной группы для добавления ученика",
                               reply_markup=other_kb.start_kb)


async def name_student_save(msg: types.Message, state: FSMContext):
    await state.update_data(name_group=msg.text)  # сохраняем в озу
    await msg.answer("Введите Ф.И. ученика", reply_markup=ReplyKeyboardRemove())
    await FSMAddedStudent.next()


async def save_student_end(msg: types.Message, state: FSMContext):
    # if msg.from_user.id == 5295520075:
    await state.update_data(name_student=msg.text)
    data = await state.get_data()  # достаем из озу
    await sql_added_student(data['name_group'], data['name_student'])
    await bot.send_message(msg.chat.id, 'Ученик добавлен в группу', reply_markup=other_kb.start_kb)
    await state.finish()


def register_handlers_student_added(dp: Dispatcher):
    dp.register_message_handler(start_fsm_student, lambda message: message.text == "Добавить ученика 👤", state=None)
    dp.register_message_handler(name_student_save, state=FSMAddedStudent.name_student_to_group)
    dp.register_message_handler(save_student_end, state=FSMAddedStudent.save_student)
