from aiogram import types, Dispatcher
from zp.create_bot import bot
from aiogram.utils.exceptions import MessageNotModified
from ..models import edit_msg_clicked_group, edit_msg_clicked_salary, edit_msg_clicked_back
from ..keyboards import mark_salary_mk, mk_cancel
from ..excel import main_exel, calculate_salary
from zp.keyboards import other_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State



async def start_go(msg: types.Message):
    global edit
    edit = await bot.send_message(msg.chat.id, "Добро пожаловать ! Я ваш помощник.\nЯ создан, чтобы вы не забивали свою голову излишней рутиной\nВыберите  один из вариантов ниже:", reply_markup=mark_salary_mk)


async def request_article(clb: types.CallbackQuery):
    try:
        await edit_msg_clicked_group(edit)
    except MessageNotModified:
        await clb.answer()  # убираем ожидания


async def request_article_plus(clb: types.CallbackQuery):
    try:
        salary = calculate_salary()
        await edit_msg_clicked_salary(edit, int(salary))
    except MessageNotModified:
        await clb.answer()
        # await clb.answer(text="hello")
        # await clb.message.answer(text="hello")
        # await clb.answer(text="hello", show_alert=True)


async def back_go(msg: types.Message):
    await edit_msg_clicked_back(edit)


class FSMAdditionalLesson(StatesGroup):
    student_additional = State()


async def start_fsm_get_lesson_additional(clb: types.CallbackQuery):
    x = await FSMAdditionalLesson.student_additional.set()
    await bot.send_message(clb.from_user.id, "Введите имя ученика (ков)", reply_markup=mk_cancel)


async def additional_name_student_save(msg: types.Message, state: FSMContext):
    await state.update_data(name_group=msg.text)  # сохраняем в озу
    main_exel(msg.text, 1)  # write to excel
    await msg.answer("Доп. урок записан", reply_markup=other_kb.start_kb)
    await state.finish()


def register_handlers_go(dp: Dispatcher):
    dp.register_message_handler(start_go, text='Начать ⚡')
    dp.register_callback_query_handler(back_go, text='go')
    dp.register_callback_query_handler(request_article, text='lesson')
    dp.register_callback_query_handler(request_article_plus, lambda c: c.data == 'salary')
    dp.register_callback_query_handler(start_fsm_get_lesson_additional, text='additional', state=None)
    dp.register_message_handler(additional_name_student_save, state=FSMAdditionalLesson.student_additional)
