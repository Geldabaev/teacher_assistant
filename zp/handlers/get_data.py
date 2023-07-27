
from aiogram import types, Dispatcher
from zp.create_bot import bot, dp
from zp.keyboards import conf_settings, other_kb, mk_confirm


async def file_excel_loader(message : types.Message):
    'для отправки файла excel'
    try:
        await message.reply_document(open('excel/write_only.xlsx', 'rb'), reply_markup=other_kb.start_kb)
    except FileNotFoundError as ex:
        await bot.send_message(message.chat.id, "Файл еще не создан!")


def register_handlers_excel(dp: Dispatcher):
    dp.register_message_handler(file_excel_loader, text='Получить отчет! 📄')

