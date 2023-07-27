from aiogram import types
from ..keyboards import mark_salary_mk, mk_go, mk_groups_kb, mk_status_absent, mk_status_attend



__all__ = ["edit_msg_clicked_group", "edit_msg_clicked_salary", "edit_msg_clicked_back", "edit_status_student"]


async def edit_msg_clicked_group(msg: types.Message):
    mk_res = await mk_groups_kb()
    if mk_res['inline_keyboard'][0]:
        await msg.edit_text("Выберите группу", reply_markup=mk_res)
    else:
        await msg.edit_text("У вас нет не одной группы", reply_markup=mk_res)


async def edit_msg_clicked_salary(msg: types.Message, salary):
    await msg.edit_text(f"Итоговая зарплата: {salary}р", reply_markup=mk_go)


async def edit_msg_clicked_back(msg: types.Message):
    await msg.edit_text("Выберите  один из вариантов ниже:", reply_markup=mark_salary_mk)


counting = 0
async def edit_status_student(msg_edit: types.Message, txt_clb, txt_msg, count_student):
    global counting
    # меняет статус на противополжный тому что есть
    if txt_msg == 'присутствует ✅':
        await msg_edit[txt_clb].edit_text(msg_edit[txt_clb].text.replace("присутствует ✅", "отсутствует ❌"), reply_markup=mk_status_attend(txt_clb))
        counting += 1

    else:
        await msg_edit[txt_clb].edit_text(msg_edit[txt_clb].text.replace("отсутствует ❌", "присутствует ✅"), reply_markup=mk_status_absent(txt_clb))
        counting -= 1

    return count_student - counting
