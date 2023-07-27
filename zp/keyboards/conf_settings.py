from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btn_add_del_group = [KeyboardButton('Добавить группу 👥'), KeyboardButton('Удалить группу 🛑')]
btn_add_del_student = [KeyboardButton('Добавить ученика 👤'), KeyboardButton('Удалить ученика 🗑')]
markup_add_del = ReplyKeyboardMarkup(resize_keyboard=True)
markup_add_del.row(*btn_add_del_group).row(*btn_add_del_student)


kb_confirm = KeyboardButton("Подтвердить")
kb_keep = KeyboardButton("Отмена")
mk_confirm = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(kb_confirm).add(kb_keep)


def mk_status_attend(kb_text):
    "функция кнопка для изменения текст сообщении и кнопки на новый"
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text="Присутствует " + kb_text + "✔", callback_data=f"status {kb_text}"))


def mk_status_absent(kb_text):
    "функция кнопка для изменения текст сообщении и кнопки на новый"
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text="Отсутствует " + kb_text + "✖", callback_data=f"status {kb_text}"))
