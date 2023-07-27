from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from zp.data_base import read_sql

__all__ = ["mark_salary_mk", "ReplyKeyboardMarkup", "mk_groups_kb", "mk_go", "mk_cancel", "start_kb", "cancel_mk"]

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
conf_btn = KeyboardButton("Настроить 🛠")
run_btn = KeyboardButton("Начать ⚡")
getdoc_btn = KeyboardButton("Получить отчет! 📄")
start_kb.add(run_btn).add(conf_btn).add(getdoc_btn)

mark_salary_mk = InlineKeyboardMarkup(row_width=2)
kb_mark_salary = [InlineKeyboardButton(text="Урок 📚", callback_data="lesson"), InlineKeyboardButton(text="Доп. урок 📝", callback_data='additional')]
mark_salary_mk.row(*kb_mark_salary).add(InlineKeyboardButton(text="ЗП 💰", callback_data='salary'))


mk_go = InlineKeyboardMarkup(row_width=1)
kb_zp = InlineKeyboardButton(text="Назад", callback_data="go")
mk_go.add(kb_zp)


async def mk_groups_kb():
    read = await read_sql('my_groups')
    groups_inline = []
    if read:
        for ret in read:
            groups_inline.append(InlineKeyboardButton(text=ret[1], callback_data=f"output {ret[0]}"))  # указываем id группы, чтобы выводить потом студентов по их id группы ret[0]
    mk_groups = InlineKeyboardMarkup(row_width=2)
    InlineKeyboardButton(text="Назад", callback_data="lesson")
    # mk_groups.row(*groups_inline).add(kb_zp)
    for i in groups_inline:
        mk_groups.add(i)
    mk_groups.add(kb_zp)
    return mk_groups


mk_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Отмена")


ready_mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
ready_kb = KeyboardButton("Готово")
cancel_kb = KeyboardButton("Отмена")
ready_mk.add(ready_kb).add(cancel_kb)


cancel_mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_kb_one = KeyboardButton("Отмена")
cancel_mk.add(cancel_kb_one)
