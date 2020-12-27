import sqlite3


class Base_date:  # класс для работы с бд
    def __init__(self, title):
        self.title = title

    def select(self, res, table, uslov=None, z=None,
               dr=[]):  # метод получения данных из бд
        con = sqlite3.connect(self.title)
        cur = con.cursor()
        if uslov is not None:
            result = cur.execute(f'''SELECT {", ".join(res)} FROM {table}
    WHERE {f" {uslov} ".join([f"""{z[i]} = '{z[i + 1]}'""" for i in range(0, len(z), 2)] + dr)}''').fetchall()
        else:
            result = cur.execute(f'''SELECT {", ".join(res)} FROM {table}''').fetchall()
        con.close()
        return result

    def delete(self, table, uslov, z, dr=[]):  # метод удаления данных из бд
        con = sqlite3.connect(self.title)
        cur = con.cursor()
        cur.execute(
            f"""DELETE from {table} where {f" {uslov} ".join([f'''{z[i]} = "{z[i + 1]}"''' for i in range(0, len(z), 2)] + dr)}""")
        con.commit()
        con.close()

    def insert(self, table, res, z):  # метод дополнения данных в бд
        con = sqlite3.connect(self.title)
        cur = con.cursor()
        cur.execute(
            f"""INSERT INTO {table}({str(res)}) VALUES ({', '.join(['?' for _ in range(len(z))])})""",
            z)
        con.commit()
        con.close()

    def create(self):  # метод создания и заполнения тестового пользователя в бд
        con = sqlite3.connect(self.title)
        cur = con.cursor()
        cur.execute("""CREATE TABLE Users (
            Id                INTEGER PRIMARY KEY
                                      NOT NULL
                                      UNIQUE
                                      CHECK (Id > 0),
            Name              TEXT,
            Registration_date TIME,
            Login             STRING  UNIQUE,
            Password          STRING  UNIQUE);""")
        cur.execute("""CREATE TABLE Once (
            Id      INTEGER REFERENCES users (Id) ON DELETE CASCADE
                                                  ON UPDATE CASCADE,
            Date    STRING,
            [Begin] STRING,
            [End]   STRING,
            Event   TEXT,
            Image   BLOB);""")
        cur.execute("""CREATE TABLE Every_year (
            Id      INTEGER REFERENCES users (Id) ON DELETE CASCADE
                                                  ON UPDATE CASCADE,
            Month   STRING,
            Day     STRING,
            [Begin] STRING,
            [End]   STRING,
            Event   TEXT,
            Image   BLOB);""")
        cur.execute("""CREATE TABLE Every_week (
            Id      INTEGER REFERENCES users (Id) ON DELETE CASCADE
                                                  ON UPDATE CASCADE,
            Day     STRING,
            [Begin] STRING,
            [End]   STRING,
            Event   TEXT,
            Image   BLOB);""")
        cur.execute("""CREATE TABLE Every_month (
            Id      INTEGER REFERENCES users (Id) ON DELETE CASCADE
                                                  ON UPDATE CASCADE,
            Day     STRING,
            [Begin] STRING,
            [End]   STRING,
            Event   TEXT,
            Image   BLOB);""")
        cur.execute("""CREATE TABLE Every_day (
            Id      INTEGER REFERENCES users (Id) ON DELETE CASCADE
                                                  ON UPDATE CASCADE,
            [Begin] STRING,
            [End]   STRING,
            Event   TEXT,
            Image   BLOB);""")
        con.commit()
        cur.execute(
            f"""INSERT INTO users(name, login, password, Registration_date) VALUES('Artem', '32', '32', '2020-10-31')""")
        cur.execute(
            f"""INSERT INTO once(id, date, begin, end, event) VALUES(1, '2020-11-13', '12-0', '17-0', 'Зашита проектов по PyQt5')""")
        cur.execute(
            f"""INSERT INTO every_day(id, begin, end, event) VALUES(1, '8-0', '8-20', 'Зарядка')""")
        cur.execute(
            f"""INSERT INTO every_day(id, begin, end, event) VALUES(1, '8-20', '8-40', 'Завтрак')""")
        cur.execute(
            f"""INSERT INTO every_day(id, begin, end, event) VALUES(1, '13-20', '13-45', 'Обед')""")
        try:  # добавление события с картинкой
            cur.execute(
                f"""INSERT INTO every_day(id, begin, end, event, image) VALUES (?, ?, ?, ?, ?)""",
                [1, '13-45', '18-0', 'Программирование',
                 open('config/python.png', 'rb').read()])
        except FileNotFoundError:  # если картинка не найдена
            cur.execute(
                f"""INSERT INTO every_day(id, begin, end, event) VALUES (?, ?, ?, ?)""",
                [1, '13-45', '18-0', 'Программирование'])
        cur.execute(
            f"""INSERT INTO every_day(id, begin, end, event) VALUES(1, '18-0', '18-20', 'Ужин')""")
        cur.execute(
            f"""INSERT INTO every_week(id, day, begin, end, event) VALUES(1, '5, 6', '10-0', '10-30', 'Убираюсь')""")
        cur.execute(
            f"""INSERT INTO every_year(id, month, day, begin, end, event) VALUES(1, '4', '17', '0-0', '23-59', 'Мой день рождения!!!')""")
        con.commit()
