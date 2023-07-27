import time
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from zp.create_bot import bot
from zp.keyboards import other_kb
from zp.data_base import (sql_delete_group, read_sql, read_sql_fk, join_table)
from ..models import edit_status_student
from ..excel import main_exel


id_msg_del = []
async def output_students_group(callback_query: types.CallbackQuery):
    global msg_edit, name_group
    name_group_and_students = await join_table(callback_query.data.replace("output ", ""))
    if name_group_and_students:
        msg_edit = {}  # ключ текст сообщения, значения id сообщения, что по значению редактировать сообщения
        for ret in name_group_and_students:
            id_msg = await bot.send_message(callback_query.from_user.id, text=ret[0].title() + "\nСтатус: присутствует ✅", reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text=f'Отсутствует {ret[0].title()} ✖', callback_data=f"status {ret[0].title()}")))
            msg_edit[ret[0].title()] = id_msg
        name_group = ret[1]
        await bot.send_message(callback_query.from_user.id, f"Ученики группы {ret[1]} ☝", reply_markup=other_kb.ready_mk)
    else:
        await bot.send_message(callback_query.from_user.id, "У вас нет ни одного ученика в этой группе", reply_markup=ReplyKeyboardRemove())


async def absent_attend_student(clb: types.CallbackQuery):
    global count_student
    "рекция на кнопки отсутсвует (присутсвует)"
    txt_msg = clb.message.text.split(":")[1].strip()
    txt_clb = clb.data.replace("status", "").strip().title()  # берем текст с кнопки, убирая лишнее
    count_student = await edit_status_student(msg_edit, txt_clb, txt_msg, len(msg_edit))


async def ready_to_write_exel(msg: types.callback_query):
    try:
        # сохраняет полученные данные в excel
        main_exel(name_group, count_student)
    except NameError:  # если статус студента не меняли
        count_student = len(msg_edit)
        main_exel(name_group, count_student)

    await msg.answer("Данные сохранены!", reply_markup=other_kb.start_kb)


def register_handlers_output_students(dp: Dispatcher):
    dp.register_callback_query_handler(output_students_group, lambda x: x.data and x.data.startswith('output '))
    dp.register_callback_query_handler(absent_attend_student, lambda x: x.data and x.data.startswith('status '))
    dp.register_message_handler(ready_to_write_exel, text='Готово')
