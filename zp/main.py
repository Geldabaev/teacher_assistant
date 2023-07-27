from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
    print("Бот вышел в онлайн")


from zp.handlers import *

register_handlers_other(dp)
register_handlers_student_del(dp)
register_handlers_group_del(dp)
register_handlers_student_added(dp)
register_handlers_groups_added(dp)
register_handlers_go(dp)
register_handlers_output_students(dp)
register_handlers_excel(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
