import sqlite3 as sq



con = sq.connect("data_zp.db")
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






# for i in range(1, 5):
#     print(i)
#     cur.execute("INSERT INTO my_groups (name_group) VALUES (?)", (f'Django{i}',))

# con.commit()

# cur.execute("INSERT INTO students (name_student, fk_students) VALUES (?, ?)", ('yunus', 2))
# cur.execute("INSERT INTO students (name_student, fk_students) VALUES (?, ?)", ('musa', 1))
# cur.execute("INSERT INTO students (name_student, fk_students) VALUES (?, ?)", ('ibragim', 1))
# cur.execute("INSERT INTO students (name_student, fk_students) VALUES (?, ?)", ('hava', 2))
# con.commit()

# print(cur.execute("SELECT * FROM my_groups").fetchall())
# print(cur.execute("SELECT * FROM students").fetchall())

# print(cur.execute("SELECT students.name_student, my_groups.name_group FROM students INNER JOIN my_groups ON my_groups.id_group=students.fk_students").fetchall())
# print(cur.execute("SELECT students.name_student, my_groups.name_group FROM students INNER JOIN my_groups ON my_groups.id_group=students.fk_students").fetchall())
#
# print(cur.execute("SELECT rowid FROM my_groups WHERE name_group = 'Django1'").fetchall()[0][0])

if None == 'yunus':
    print("***")