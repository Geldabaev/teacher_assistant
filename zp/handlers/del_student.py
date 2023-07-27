from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types, Dispatcher
from zp.create_bot import bot
from zp.keyboards import other_kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from zp.data_base import (sql_delete_student, read_sql, read_sql_get_rowid, read_sql_fk)


class FSMAddedDelStudent(StatesGroup):
    get_name = State()
    del_end = State()


async def start_fsm_del_student(msg: types.Message, state: FSMContext):
    # if msg.from_user.id == 5295520075:
    await state.update_data(name_student=msg.text)  # сохраняем в озу
    read = await read_sql("my_groups")
    if read:
        kb_list = []
        for ret in read:
            kb_list.append(KeyboardButton(ret[1]))
        await bot.send_message(msg.from_user.id, "Выберите нужную группу",
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(*kb_list).add(other_kb.cancel_kb))
        await FSMAddedDelStudent.get_name.set()

    else:
        await bot.send_message(msg.from_user.id, "У вас нет ни одной группы, чтобы удалять ученика",
                               reply_markup=other_kb.start_kb)
        await state.finish()


async def del_student_name(msg: types.Message, state: FSMContext):
    await state.update_data(name_group=msg.text)  # сохраняем в озу
    data: dict = await state.get_data()
    id_group: int = await read_sql_get_rowid(data['name_group'])
    read: list = await read_sql_fk(id_group)
    if read:
        kb_list = []
        for ret in read:
            kb_list.append(KeyboardButton(ret[0]))
        await bot.send_message(msg.from_user.id, "Кого удаляем?", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(*kb_list).add(other_kb.cancel_kb))
        await FSMAddedDelStudent.next()
    else:
        await bot.send_message(msg.from_user.id, "У вас нет ни одного ученика для удаления в этой группе",
                               reply_markup=other_kb.start_kb)
        await state.finish()


async def student_del_end(msg: types.Message, state: FSMContext):
    # if msg.from_user.id == 5295520075:
    await state.update_data(name_student=msg.text)
    data = await state.get_data()  # достаем из озу
    await sql_delete_student(data['name_student'])

    await bot.send_message(msg.chat.id, f'Ученик удален из группы {data["name_group"]}', reply_markup=other_kb.start_kb)
    await state.finish()


def register_handlers_student_del(dp: Dispatcher):
    dp.register_message_handler(start_fsm_del_student, lambda message: message.text == "Удалить ученика 🗑", state=None)
    dp.register_message_handler(del_student_name, state=FSMAddedDelStudent.get_name)
    dp.register_message_handler(student_del_end, state=FSMAddedDelStudent.del_end)
