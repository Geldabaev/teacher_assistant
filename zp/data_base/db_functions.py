import sqlite3 as sq
from sqlite3 import OperationalError
from zp.create_bot import dp, bot
from aiogram import types


async def connection():
    con = sq.connect("data_base/data_zp.db")
    cur = con.cursor()

    cur.execute(f"""CREATE TABLE IF NOT EXISTS my_groups (
                   id_group INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   name_group TEXT NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS students (
                   id_student INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   name_student TEXT NOT NULL,
                   fk_students INTEGER REFERENCES my_groups (id_group)
        )""")

    return con, cur


async def inserting_data_db(data):
    sql_con_cur = await connection()
    sql_con_cur[1].execute("INSERT INTO my_groups (name_group) VALUES (?)", (data["name_group"], ))
    sql_con_cur[0].commit()


async def sql_delete_group(data):
    sql_con_cur = await connection()
    sql_con_cur[1].execute("""DELETE FROM my_groups WHERE name_group == ?""", (data,))
    sql_con_cur[0].commit()


async def sql_delete_student(data):
    sql_con_cur = await connection()
    sql_con_cur[1].execute("""DELETE FROM students WHERE name_student == ?""", (data,))
    sql_con_cur[0].commit()


async def sql_added_student(add_student_group, name_student):
    sql_con_cur = await connection()
    fk_rowid = sql_con_cur[1].execute(f"SELECT rowid FROM my_groups WHERE name_group = (?)", (add_student_group,)).fetchall()[0][0]
    sql_con_cur[1].execute("INSERT INTO students (name_student, fk_students) VALUES (?, ?)", (name_student, fk_rowid))
    sql_con_cur[0].commit()


async def read_sql(table_name):
    sql_con_cur = await connection()
    return sql_con_cur[1].execute(f"SELECT * FROM {table_name}").fetchall()


async def read_sql_get_rowid(name_group):
    sql_con_cur = await connection()
    return sql_con_cur[1].execute(f"SELECT id_group FROM my_groups WHERE name_group = (?)", (name_group,)).fetchall()[0][0]


async def read_sql_fk(id_group):
    sql_con_cur = await connection()
    return sql_con_cur[1].execute(f"SELECT name_student FROM students WHERE fk_students={id_group}").fetchall()


async def join_table(id_fk):
    sql_con_cur = await connection()
    return sql_con_cur[1].execute(f"SELECT students.name_student, my_groups.name_group FROM students INNER JOIN my_groups ON my_groups.id_group=students.fk_students AND my_groups.id_group = {id_fk}").fetchall()
