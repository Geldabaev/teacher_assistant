import time
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from zp.create_bot import bot
from zp.keyboards import other_kb
from zp.data_base import (sql_delete_group, read_sql)


id_msg_del: list = []
async def delete_group(msg: types.Message):
    # if msg.from_user.id == 5295520075:
    read = await read_sql("my_groups")
    if read:
        for ret in read:
            id_msg = await bot.send_message(msg.from_user.id, ret[1])
            id_msg_del.append(id_msg)
            id_msg = await bot.send_message(msg.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Удалить {ret[1]}', callback_data=f"del {ret[1]}")))
            id_msg_del.append(id_msg)
        id_msg = await bot.send_message(msg.from_user.id, "Удалите нужную запись", reply_markup=other_kb.cancel_mk)
        id_msg_del.append(id_msg)
    else:
        await bot.send_message(msg.from_user.id, "У вас нет ни одной группы", reply_markup=other_kb.start_kb)


async def del_callback_run(callback_query: types.CallbackQuery):
    await sql_delete_group(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f'{callback_query.data.replace("del", "")} удалена', show_alert=True)
    await bot.send_message(callback_query.from_user.id, "Главное меню", reply_markup=other_kb.start_kb)
    for i in id_msg_del:
        time.sleep(0.3)
        await i.delete()
    id_msg_del.clear()
    

def register_handlers_group_del(dp: Dispatcher):
    dp.register_message_handler(delete_group, text='Удалить группу 🛑')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
